import numpy
from PIL import Image
import subprocess
import json

from config.config import openpose_img_out, openpose_json_out, openpose_img_input, openpose_demo, openpose_folder


class OpenPoseDetector:
    
    def __init__(self, min_detection_confidence=0.2):
        self.temporary_file_name = '\\image.png'
        self.temporary_output_img_file_name = '\\image_rendered.png'
        self.temporary_output_json_file_name = '\\image_keypoints.json'
        self.min_detection_confidence = min_detection_confidence

    def __load_img_to_local_folder(self, image):
        img = numpy.array(image)
        result = Image.fromarray(img)
        result.save(openpose_img_input + self.temporary_file_name)

    def __get_json(self):
        with open(openpose_json_out + self.temporary_output_json_file_name) as f:
            json_data = json.load(f)
            for d in json_data['people']:
                # TODO если нет руки, проверить
                pose_keypoints_2d = d['pose_keypoints_2d']
                hand_right_keypoints_2d = d['hand_right_keypoints_2d']
                hand_left_keypoints_2d = d['hand_left_keypoints_2d']
                return pose_keypoints_2d, hand_right_keypoints_2d, hand_left_keypoints_2d

    def __convert_hand_keypoints(self, hand, min_accuracy, prefix=''):
        body_key_points = {'wrist': 0,
                           'thumb_finger_cmc': 1, 'thumb_finger_mcp': 2, 'thumb_finger_ip': 3, 'thumb_finger_tip': 4,
                           'index_finger_mcp': 5, 'index_finger_pip': 6, 'index_finger_dip': 7, 'index_finger_tip': 8,
                           'middle_finger_mcp': 9, 'middle_finger_pip': 10, 'middle_finger_dip': 11, 'middle_finger_tip': 12,
                           'ring_finger_mcp': 13, 'ring_finger_pip': 14, 'ring_finger_dip': 15, 'ring_finger_tip': 16,
                           'pinky_finger_mcp': 17, 'pinky_finger_pip': 18, 'pinky_finger_dip': 19, 'pinky_finger_tip': 20}
        if prefix != '':
            prefix = prefix.lower() + '_'
        out = {}
        for key, val in body_key_points.items():
            val = val * 3
            if hand[val + 2] >= min_accuracy and \
                    (hand[val] and hand[val + 1] and hand[val + 2]):    # x0, y0, a0 -> kp doesnt exist:
                out[prefix + key] = [hand[val], hand[val + 1]]
        return out

    def __convert_body_keypoints(self, body, min_accuracy):
        body_key_points = {'nose': 0,
                           'left_shoulder': 5, 'left_elbow': 6, 'left_wrist': 7,
                           'left_hip': 12, 'left_knee':13, 'left_ankle': 14,
                           'right_shoulder': 2, 'right_elbow': 3, 'right_wrist': 4,
                           'right_hip': 9, 'right_knee': 10, 'right_ankle': 11,
                           'right_ear': 17, 'left_ear': 18,
                           'right_eye': 15, 'left_eye': 16}
        out = {}
        for key, val in body_key_points.items():
            val = val * 3
            if body[val + 2] >= min_accuracy and \
                    (body[val] and body[val + 1] and body[val + 2]):    # x0, y0, a0 -> kp doesnt exist
                out[key] = [body[val], body[val + 1]]
        return out

    def detect(self, image):
        self.__load_img_to_local_folder(image)
        subprocess.call([openpose_demo,
                         '--image_dir', openpose_img_input,
                         '--write_json', openpose_json_out,
                         # '--write_images', openpose_img_out,
                         '--net_resolution', '-1x128',
                         '--number_people_max', '1',
                         '--hand'
                         ],
                        cwd=openpose_folder)

        pose_keypoints_2d, hand_right_keypoints_2d, hand_left_keypoints_2d = self.__get_json()
        return {'body': self.__convert_body_keypoints(pose_keypoints_2d, self.min_detection_confidence),
                'right_hand': self.__convert_hand_keypoints(hand_right_keypoints_2d, self.min_detection_confidence, ''),
                'left_hand': self.__convert_hand_keypoints(hand_left_keypoints_2d, self.min_detection_confidence, '')}
