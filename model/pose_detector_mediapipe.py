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

    def __convert_hand_keypoints(self, landmarks, image_width, image_height):
        out = None

        if landmarks:
            landmark = landmarks.landmark

            mark = self.__mp_holistic.HandLandmark
            hands_key_points = \
                {'wrist': (landmark[mark.WRIST].x, landmark[mark.WRIST].y),
                 'thumb_finger_cmc': (landmark[mark.THUMB_CMC].x, landmark[mark.THUMB_CMC].y),
                 'thumb_finger_mcp': (landmark[mark.THUMB_MCP].x, landmark[mark.THUMB_MCP].y),
                 'thumb_finger_ip': (landmark[mark.THUMB_IP].x, landmark[mark.THUMB_IP].y),
                 'thumb_finger_tip': (landmark[mark.THUMB_TIP].x, landmark[mark.THUMB_TIP].y),
                 'index_finger_mcp': (landmark[mark.INDEX_FINGER_MCP].x, landmark[mark.INDEX_FINGER_MCP].y),
                 'index_finger_pip': (landmark[mark.INDEX_FINGER_PIP].x, landmark[mark.INDEX_FINGER_PIP].y),
                 'index_finger_dip': (landmark[mark.INDEX_FINGER_DIP].x, landmark[mark.INDEX_FINGER_DIP].y),
                 'index_finger_tip': (landmark[mark.INDEX_FINGER_TIP].x, landmark[mark.INDEX_FINGER_TIP].y),
                 'middle_finger_mcp': (landmark[mark.MIDDLE_FINGER_MCP].x, landmark[mark.MIDDLE_FINGER_MCP].y),
                 'middle_finger_pip': (landmark[mark.MIDDLE_FINGER_PIP].x, landmark[mark.MIDDLE_FINGER_PIP].y),
                 'middle_finger_dip': (landmark[mark.MIDDLE_FINGER_DIP].x, landmark[mark.MIDDLE_FINGER_DIP].y),
                 'middle_finger_tip': (landmark[mark.MIDDLE_FINGER_TIP].x, landmark[mark.MIDDLE_FINGER_TIP].y),
                 'ring_finger_mcp': (landmark[mark.RING_FINGER_MCP].x, landmark[mark.RING_FINGER_MCP].y),
                 'ring_finger_pip': (landmark[mark.RING_FINGER_PIP].x, landmark[mark.RING_FINGER_PIP].y),
                 'ring_finger_dip': (landmark[mark.RING_FINGER_DIP].x, landmark[mark.RING_FINGER_DIP].y),
                 'ring_finger_tip': (landmark[mark.RING_FINGER_TIP].x, landmark[mark.RING_FINGER_TIP].y),
                 'pinky_finger_mcp': (landmark[mark.PINKY_MCP].x, landmark[mark.PINKY_MCP].y),
                 'pinky_finger_pip': (landmark[mark.PINKY_PIP].x, landmark[mark.PINKY_PIP].y),
                 'pinky_finger_dip': (landmark[mark.PINKY_DIP].x, landmark[mark.PINKY_DIP].y),
                 'pinky_finger_tip': (landmark[mark.PINKY_TIP].x, landmark[mark.PINKY_TIP].y)}
            out = {}
            for key, val in hands_key_points.items():
                x = round(val[0]*image_width, 2)
                y = round(val[1]*image_height, 2)
                # проверка, является то точка предсказанной (находится за пределами изображения)
                if (image_width >= x >= 0) and (image_height >= y >= 0):
                    out[key] = (x, y)

        return out

    def __convert_body_keypoints(self, landmarks, image_width, image_height):
        out = None

        if landmarks:
            landmark = landmarks.landmark

            mark = self.__mp_holistic.PoseLandmark
            body_key_points = \
                {'nose': (landmark[mark.NOSE].x, landmark[mark.NOSE].y),
                 'left_eye': (landmark[mark.LEFT_EYE].x, landmark[mark.LEFT_EYE].y),
                 'left_mouth': (landmark[mark.MOUTH_LEFT].x, landmark[mark.MOUTH_LEFT].y),
                 'left_ear': (landmark[mark.LEFT_EAR].x, landmark[mark.LEFT_EAR].y),
                 'left_shoulder': (landmark[mark.LEFT_SHOULDER].x, landmark[mark.LEFT_SHOULDER].y),
                 'left_elbow': (landmark[mark.LEFT_ELBOW].x, landmark[mark.LEFT_ELBOW].y),
                 'left_wrist': (landmark[mark.LEFT_WRIST].x, landmark[mark.LEFT_WRIST].y),
                 'left_hip': (landmark[mark.LEFT_HIP].x, landmark[mark.LEFT_HIP].y),
                 'left_knee': (landmark[mark.LEFT_KNEE].x, landmark[mark.LEFT_KNEE].y),
                 'left_ankle': (landmark[mark.LEFT_ANKLE].x, landmark[mark.LEFT_ANKLE].y),
                 'right_eye': (landmark[mark.RIGHT_EYE].x, landmark[mark.RIGHT_EYE].y),
                 'right_mouth': (landmark[mark.MOUTH_RIGHT].x, landmark[mark.MOUTH_RIGHT].y),
                 'right_ear': (landmark[mark.RIGHT_EAR].x, landmark[mark.RIGHT_EAR].y),
                 'right_shoulder': (landmark[mark.RIGHT_SHOULDER].x, landmark[mark.RIGHT_SHOULDER].y),
                 'right_elbow': (landmark[mark.RIGHT_ELBOW].x, landmark[mark.RIGHT_ELBOW].y),
                 'right_wrist': (landmark[mark.RIGHT_WRIST].x, landmark[mark.RIGHT_WRIST].y),
                 'right_hip': (landmark[mark.RIGHT_HIP].x, landmark[mark.RIGHT_HIP].y),
                 'right_knee': (landmark[mark.RIGHT_KNEE].x, landmark[mark.RIGHT_KNEE].y),
                 'right_ankle': (landmark[mark.RIGHT_ANKLE].x, landmark[mark.RIGHT_ANKLE].y)}
            out = {}
            for key, val in body_key_points.items():
                x = round(val[0] * image_width, 2)
                y = round(val[1] * image_height, 2)
                # проверка, является то точка предсказанной (находится за пределами изображения)
                if (image_width >= x >= 0) and (image_height >= y >= 0):
                    out[key] = (x, y)

        return out

    def __reset_wrist(self, pose):
        if pose['right_hand'] is not None and 'wrist' in pose['right_hand']:
            pose['body']['right_wrist'] = pose['right_hand']['wrist']
        if pose['left_hand'] is not None and 'wrist' in pose['left_hand']:
            pose['body']['left_wrist'] = pose['left_hand']['wrist']
        if pose['right_hand'] is not None and 'right_wrist' in pose['body']:
            pose['right_hand']['wrist'] = pose['body']['right_wrist']
        if pose['left_hand'] is not None and 'left_wrist' in pose['body']:
            pose['left_hand']['wrist'] = pose['body']['left_wrist']
        return pose

    def detect_pose(self, pil_image):
        nparray_image = numpy.array(pil_image)
        image_height, image_width, _ = nparray_image.shape
        results = self.__holistic.process(cv2.cvtColor(nparray_image, cv2.COLOR_BGR2RGB))

        pose = {'body': self.__convert_body_keypoints(results.pose_landmarks, image_width, image_height),
                'right_hand': self.__convert_hand_keypoints(results.right_hand_landmarks, image_width, image_height),
                'left_hand': self.__convert_hand_keypoints(results.left_hand_landmarks, image_width, image_height)}

        pose = self.__reset_wrist(pose)

        return pose
