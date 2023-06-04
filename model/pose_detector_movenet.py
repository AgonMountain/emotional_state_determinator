import datetime

import PIL.Image
import tensorflow as tf
import numpy as np
import cv2

from config.config import movenet_model_path


class MoveNetDetector:

    def __init__(self, min_detection_confidence=0.5):
        self.interpreter = tf.lite.Interpreter(model_path=movenet_model_path)
        self.interpreter.allocate_tensors()
        self.min_detection_confidence = min_detection_confidence

        self.KEYPOINT_DICT = {
            'left_shoulder': 5,
            'right_shoulder': 6,
            'left_elbow': 7,
            'right_elbow': 8,
            'left_wrist': 9,
            'right_wrist': 10,
            'left_hip': 11,
            'right_hip': 12,
            'left_knee': 13,
            'right_knee': 14,
            'left_ankle': 15,
            'right_ankle': 16
        }

    def movenet(self, input_image):
        input_image = tf.cast(input_image, dtype=tf.uint8)
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        self.interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])
        return keypoints_with_scores

    def get_affine_transform_to_fixed_sizes_with_padding(self, size, new_sizes):
        width, height = new_sizes
        scale = min(height / float(size[1]), width / float(size[0]))
        M = np.float32([[scale, 0, 0], [0, scale, 0]])
        M[0][2] = (width - scale * size[0]) / 2
        M[1][2] = (height - scale * size[1]) / 2
        return M

    def __get_center_of(self, p1, p2):
        x_min = min(p1[0], p2[0])
        x_max = max(p1[0], p2[0])
        y_min = min(p1[1], p2[1])
        y_max = max(p1[1], p2[1])
        return ((x_min + (x_max - x_min) / 2), y_min + ((y_max - y_min) / 2))

    def __convert_body_keypoints(self, keypoints_with_scores):
        dict = {}
        for k, v in self.KEYPOINT_DICT.items():
            if keypoints_with_scores[v][2] >= self.min_detection_confidence:
                dict[k] = (round(keypoints_with_scores[v][1], 2), round(keypoints_with_scores[v][0], 2))

        if keypoints_with_scores[5][2] >= self.min_detection_confidence and \
                keypoints_with_scores[6][2] >= self.min_detection_confidence:
            dict['center_shoulder'] = self.__get_center_of((round(keypoints_with_scores[5][1], 2), round(keypoints_with_scores[5][0], 2)),
                                                           (round(keypoints_with_scores[6][1], 2), round(keypoints_with_scores[6][0], 2)))

        if keypoints_with_scores[11][2] >= self.min_detection_confidence and \
                keypoints_with_scores[12][2] >= self.min_detection_confidence:
            dict['center_hip'] = self.__get_center_of((round(keypoints_with_scores[11][1], 2), round(keypoints_with_scores[11][0], 2)),
                                                      (round(keypoints_with_scores[12][1], 2), round(keypoints_with_scores[12][0], 2)),)
        return dict

    def detect_pose(self, pil_image):
        # Reshape image
        img = np.array(pil_image.convert('RGB'))    # .convert('RGB') -> tf dont like png file ithk, jpeg and wepb - is ok, idk
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192, 192)
        input_image = tf.cast(img, dtype=tf.float32)

        # Setup input and output
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Make predictions
        self.interpreter.set_tensor(input_details[0]["index"], np.array(input_image).astype(np.uint8))
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]["index"])[0, 0]

        orig_w, orig_h = np.array(pil_image).shape[:2]
        M = self.get_affine_transform_to_fixed_sizes_with_padding((orig_w, orig_h), (192, 192))
        # M has shape 2x3 but we need square matrix when finding an inverse
        M = np.vstack((M, [0, 0, 1]))
        M_inv = np.linalg.inv(M)[:2]
        xy_keypoints = keypoints_with_scores[:, :2] * 192
        xy_keypoints = cv2.transform(np.array([xy_keypoints]), M_inv)[0]
        keypoints_with_scores = np.hstack((xy_keypoints, keypoints_with_scores[:, 2:]))

        result = self.__convert_body_keypoints(keypoints_with_scores)
        print(f'{self.__get_actual_date_time()} MoveNet Detector: {result}')
        return result

    def __get_actual_date_time(self):
        return '{date:%d-%m-%Y %H:%M:%S}'.format(date=datetime.datetime.now())