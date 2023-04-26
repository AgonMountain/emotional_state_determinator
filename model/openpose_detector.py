import subprocess
import json
from config.config import openpose_json_out, openpose_img_input, openpose_demo, openpose_folder


class OpenPoseDetector:
    
    def __init__(self, min_detection_confidence=0.3):
        self.__temporary_file_name = '\\image.png'
        self.__temporary_output_json_file_name = '\\image_keypoints.json'
        self.__min_detection_confidence = min_detection_confidence

    def __get_json(self):
        with open(openpose_json_out + self.__temporary_output_json_file_name) as f:
            json_data = json.load(f)
            for d in json_data['people']:
                body = d['pose_keypoints_2d'] if 'pose_keypoints_2d' in d else None
                right_hand = d['hand_right_keypoints_2d'] if 'hand_right_keypoints_2d' in d else None
                left_hand = d['hand_left_keypoints_2d'] if 'hand_left_keypoints_2d' in d else None

        return body, right_hand, left_hand

    def __load_img_to_local_folder(self, pil_image):
        pil_image.save(openpose_img_input + self.__temporary_file_name)

    def __convert_hand_keypoints(self, hand, min_accuracy):
        body_key_points = {'wrist': 0,
                           'thumb_finger_cmc': 1, 'thumb_finger_mcp': 2, 'thumb_finger_ip': 3, 'thumb_finger_tip': 4,
                           'index_finger_mcp': 5, 'index_finger_pip': 6, 'index_finger_dip': 7, 'index_finger_tip': 8,
                           'middle_finger_mcp': 9, 'middle_finger_pip': 10, 'middle_finger_dip': 11, 'middle_finger_tip': 12,
                           'ring_finger_mcp': 13, 'ring_finger_pip': 14, 'ring_finger_dip': 15, 'ring_finger_tip': 16,
                           'pinky_finger_mcp': 17, 'pinky_finger_pip': 18, 'pinky_finger_dip': 19, 'pinky_finger_tip': 20}
        out = {}
        for key, val in body_key_points.items():
            val = val * 3
            if hand[val + 2] >= min_accuracy and (hand[val] and hand[val + 1] and hand[val + 2]):
                # x0, y0, a0 -> kp doesnt exist:
                out[key] = [round(hand[val], 2), round(hand[val + 1], 2)]
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
            if body[val + 2] >= min_accuracy and (body[val] and body[val + 1] and body[val + 2]):
                # x0, y0, a0 -> kp doesnt exist
                out[key] = [round(body[val], 2), round(body[val + 1], 2)]
        return out

    def detect_pose(self, pil_image):
        self.__load_img_to_local_folder(pil_image)
        subprocess.call([openpose_demo,
                         '--image_dir', openpose_img_input,
                         '--write_json', openpose_json_out,
                         '--net_resolution', '-1x128',
                         '--number_people_max', '1',
                         '--hand',
                         '--display', '0',
                         '--render_pose', '0',
                         ],
                        cwd=openpose_folder)

        body, right_hand, left_hand = self.__get_json()
        return {'body': self.__convert_body_keypoints(body, self.__min_detection_confidence),
                'right_hand': self.__convert_hand_keypoints(right_hand, self.__min_detection_confidence),
                'left_hand': self.__convert_hand_keypoints(left_hand, self.__min_detection_confidence)}
