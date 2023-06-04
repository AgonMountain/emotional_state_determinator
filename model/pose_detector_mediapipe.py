import datetime

import cv2
import mediapipe as mp
import numpy


class MediaPipeHolisticDetector:

    def __init__(self, min_detection_confidence=0.5):
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_drawing_styles = mp.solutions.drawing_styles
        self.__mp_holistic = mp.solutions.holistic
        self.__holistic = self.__mp_holistic.Holistic(static_image_mode=True,
                                                      model_complexity=2,
                                                      enable_segmentation=True,
                                                      min_detection_confidence=min_detection_confidence)

    def __get_center_of(self, p1, p2):
        x_min = min(p1[0], p2[0])
        x_max = max(p1[0], p2[0])
        y_min = min(p1[1], p2[1])
        y_max = max(p1[1], p2[1])
        return ((x_min + (x_max - x_min) / 2), y_min + ((y_max - y_min) / 2))

    def __convert_body_keypoints(self, landmarks, image_width, image_height):
        out = None

        if landmarks:
            landmark = landmarks.landmark

            mark = self.__mp_holistic.PoseLandmark
            body_key_points = \
                {'left_shoulder': (landmark[mark.LEFT_SHOULDER].x, landmark[mark.LEFT_SHOULDER].y),
                 'left_elbow': (landmark[mark.LEFT_ELBOW].x, landmark[mark.LEFT_ELBOW].y),
                 'left_wrist': (landmark[mark.LEFT_WRIST].x, landmark[mark.LEFT_WRIST].y),
                 'left_hip': (landmark[mark.LEFT_HIP].x, landmark[mark.LEFT_HIP].y),
                 'left_knee': (landmark[mark.LEFT_KNEE].x, landmark[mark.LEFT_KNEE].y),
                 'left_ankle': (landmark[mark.LEFT_ANKLE].x, landmark[mark.LEFT_ANKLE].y),
                 'right_shoulder': (landmark[mark.RIGHT_SHOULDER].x, landmark[mark.RIGHT_SHOULDER].y),
                 'right_elbow': (landmark[mark.RIGHT_ELBOW].x, landmark[mark.RIGHT_ELBOW].y),
                 'right_wrist': (landmark[mark.RIGHT_WRIST].x, landmark[mark.RIGHT_WRIST].y),
                 'right_hip': (landmark[mark.RIGHT_HIP].x, landmark[mark.RIGHT_HIP].y),
                 'right_knee': (landmark[mark.RIGHT_KNEE].x, landmark[mark.RIGHT_KNEE].y),
                 'right_ankle': (landmark[mark.RIGHT_ANKLE].x, landmark[mark.RIGHT_ANKLE].y),
                 'right_hand': self.__get_center_of((landmark[mark.RIGHT_INDEX].x, landmark[mark.RIGHT_INDEX].y),
                                              (landmark[mark.RIGHT_PINKY].x, landmark[mark.RIGHT_PINKY].y)),
                 'left_hand': self.__get_center_of((landmark[mark.LEFT_INDEX].x, landmark[mark.LEFT_INDEX].y),
                                                    (landmark[mark.LEFT_PINKY].x, landmark[mark.LEFT_PINKY].y)),
                 'right_foot': self.__get_center_of((landmark[mark.RIGHT_HEEL].x, landmark[mark.RIGHT_HEEL].y),
                                                    (landmark[mark.RIGHT_FOOT_INDEX].x, landmark[mark.RIGHT_FOOT_INDEX].y)),
                 'left_foot': self.__get_center_of((landmark[mark.LEFT_HEEL].x, landmark[mark.LEFT_HEEL].y),
                                                   (landmark[mark.LEFT_FOOT_INDEX].x, landmark[mark.LEFT_FOOT_INDEX].y)),
                 'center_shoulder': self.__get_center_of((landmark[mark.LEFT_SHOULDER].x, landmark[mark.LEFT_SHOULDER].y),
                                                   (landmark[mark.RIGHT_SHOULDER].x, landmark[mark.RIGHT_SHOULDER].y)),
                 'center_hip': self.__get_center_of((landmark[mark.LEFT_HIP].x, landmark[mark.LEFT_HIP].y),
                                                    (landmark[mark.RIGHT_HIP].x, landmark[mark.RIGHT_HIP].y))}
            out = {}
            for key, val in body_key_points.items():
                x = round(val[0] * image_width, 2)
                y = round(val[1] * image_height, 2)
                # проверка, является то точка предсказанной (находится за пределами изображения)
                if (image_width >= x >= 0) and (image_height >= y >= 0):
                    out[key] = (x, y)

        return out

    def detect_pose(self, pil_image):
        nparray_image = numpy.array(pil_image)
        image_height, image_width, _ = nparray_image.shape
        results = self.__holistic.process(cv2.cvtColor(nparray_image, cv2.COLOR_BGR2RGB))

        result = self.__convert_body_keypoints(results.pose_landmarks, image_width, image_height)
        print(f'{self.__get_actual_date_time()} MediaPipe Detector: {result}')
        return result

    def __get_actual_date_time(self):
        return '{date:%d-%m-%Y %H:%M:%S}'.format(date=datetime.datetime.now())