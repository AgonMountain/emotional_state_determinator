import cv2
import mediapipe as mp
import numpy


class MediaPipeDetector:

    def __init__(self, min_detection_confidence=0.5):
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_drawing_styles = mp.solutions.drawing_styles
        self.__mp_holistic = mp.solutions.holistic

        self.__holistic = self.__mp_holistic.Holistic(static_image_mode=True, model_complexity=2, enable_segmentation=True,
                                                      min_detection_confidence=min_detection_confidence)

    def __convert_hand_keypoints(self, hand_landmark, image_width, image_height, prefix=''):
        if prefix != '':
            prefix = prefix.lower() + '_'

        mark = self.__mp_holistic.HandLandmark
        hands_key_points = {prefix + 'wrist': [hand_landmark[mark.WRIST].x, hand_landmark[mark.WRIST].y],
                           prefix + 'thumb_finger_cmc': [hand_landmark[mark.THUMB_CMC].x, hand_landmark[mark.THUMB_CMC].y],
                           prefix + 'thumb_finger_mcp': [hand_landmark[mark.THUMB_MCP].x, hand_landmark[mark.THUMB_MCP].y],
                           prefix + 'thumb_finger_ip': [hand_landmark[mark.THUMB_IP].x, hand_landmark[mark.THUMB_IP].y],
                           prefix + 'thumb_finger_tip': [hand_landmark[mark.THUMB_TIP].x, hand_landmark[mark.THUMB_TIP].y],
                           prefix + 'index_finger_mcp': [hand_landmark[mark.INDEX_FINGER_MCP].x, hand_landmark[mark.INDEX_FINGER_MCP].y],
                           prefix + 'index_finger_pip': [hand_landmark[mark.INDEX_FINGER_PIP].x, hand_landmark[mark.INDEX_FINGER_PIP].y],
                           prefix + 'index_finger_dip': [hand_landmark[mark.INDEX_FINGER_DIP].x, hand_landmark[mark.INDEX_FINGER_DIP].y],
                           prefix + 'index_finger_tip': [hand_landmark[mark.INDEX_FINGER_TIP].x, hand_landmark[mark.INDEX_FINGER_TIP].y],
                           prefix + 'middle_finger_mcp': [hand_landmark[mark.MIDDLE_FINGER_MCP].x, hand_landmark[mark.MIDDLE_FINGER_MCP].y],
                           prefix + 'middle_finger_pip': [hand_landmark[mark.MIDDLE_FINGER_PIP].x, hand_landmark[mark.MIDDLE_FINGER_PIP].y],
                           prefix + 'middle_finger_dip': [hand_landmark[mark.MIDDLE_FINGER_DIP].x, hand_landmark[mark.MIDDLE_FINGER_DIP].y],
                           prefix + 'middle_finger_tip': [hand_landmark[mark.MIDDLE_FINGER_TIP].x, hand_landmark[mark.MIDDLE_FINGER_TIP].y],
                           prefix + 'ring_finger_mcp': [hand_landmark[mark.RING_FINGER_MCP].x, hand_landmark[mark.RING_FINGER_MCP].y],
                           prefix + 'ring_finger_pip': [hand_landmark[mark.RING_FINGER_PIP].x, hand_landmark[mark.RING_FINGER_PIP].y],
                           prefix + 'ring_finger_dip': [hand_landmark[mark.RING_FINGER_DIP].x, hand_landmark[mark.RING_FINGER_DIP].y],
                           prefix + 'ring_finger_tip': [hand_landmark[mark.RING_FINGER_TIP].x, hand_landmark[mark.RING_FINGER_TIP].y],
                           prefix + 'pinky_finger_mcp': [hand_landmark[mark.PINKY_MCP].x, hand_landmark[mark.PINKY_MCP].y],
                           prefix + 'pinky_finger_pip': [hand_landmark[mark.PINKY_PIP].x, hand_landmark[mark.PINKY_PIP].y],
                           prefix + 'pinky_finger_dip': [hand_landmark[mark.PINKY_DIP].x, hand_landmark[mark.PINKY_DIP].y],
                           prefix + 'pinky_finger_tip': [hand_landmark[mark.PINKY_TIP].x, hand_landmark[mark.PINKY_TIP].y]}

        out = {}
        for key, val in hands_key_points.items():
            out[key] = [round(val[0]*image_width, 2), round(val[1]*image_height, 2)]

        return out

    def __convert_body_keypoints(self, body_landmark, image_width, image_height):
        mark = self.__mp_holistic.PoseLandmark
        body_key_points = {'nose': [body_landmark[mark.NOSE].x, body_landmark[mark.NOSE].y],
                           'right_eye': [body_landmark[mark.RIGHT_EYE].x, body_landmark[mark.RIGHT_EYE].y],
                           'left_eye': [body_landmark[mark.LEFT_EYE].x, body_landmark[mark.LEFT_EYE].y],
                           'left_mouth': [body_landmark[mark.MOUTH_LEFT].x, body_landmark[mark.MOUTH_LEFT].y],
                           'left_ear': [body_landmark[mark.LEFT_EAR].x, body_landmark[mark.LEFT_EAR].y],
                           'left_shoulder': [body_landmark[mark.LEFT_SHOULDER].x, body_landmark[mark.LEFT_SHOULDER].y],
                           'left_elbow': [body_landmark[mark.LEFT_ELBOW].x, body_landmark[mark.LEFT_ELBOW].y],
                           'left_wrist': [body_landmark[mark.LEFT_WRIST].x, body_landmark[mark.LEFT_WRIST].y],
                           'left_hip': [body_landmark[mark.LEFT_HIP].x, body_landmark[mark.LEFT_HIP].y],
                           'left_knee': [body_landmark[mark.LEFT_KNEE].x, body_landmark[mark.LEFT_KNEE].y],
                           'left_ankle': [body_landmark[mark.LEFT_ANKLE].x, body_landmark[mark.LEFT_ANKLE].y],
                           'right_mouth': [body_landmark[mark.MOUTH_RIGHT].x, body_landmark[mark.MOUTH_RIGHT].y],
                           'right_ear': [body_landmark[mark.RIGHT_EAR].x, body_landmark[mark.RIGHT_EAR].y],
                           'right_shoulder': [body_landmark[mark.RIGHT_SHOULDER].x, body_landmark[mark.RIGHT_SHOULDER].y],
                           'right_elbow': [body_landmark[mark.RIGHT_ELBOW].x, body_landmark[mark.RIGHT_ELBOW].y],
                           'right_wrist': [body_landmark[mark.RIGHT_WRIST].x, body_landmark[mark.RIGHT_WRIST].y],
                           'right_hip': [body_landmark[mark.RIGHT_HIP].x, body_landmark[mark.RIGHT_HIP].y],
                           'right_knee': [body_landmark[mark.RIGHT_KNEE].x, body_landmark[mark.RIGHT_KNEE].y],
                           'right_ankle': [body_landmark[mark.RIGHT_ANKLE].x, body_landmark[mark.RIGHT_ANKLE].y]}

        out = {}
        for key, val in body_key_points.items():
            out[key] = [round(val[0]*image_width, 2), round(val[1]*image_height, 2)]

        return out

    def detect_pose(self, pil_image):
        nparray_image = numpy.array(pil_image)
        image_height, image_width, _ = nparray_image.shape
        results = self.__holistic.process(cv2.cvtColor(nparray_image, cv2.COLOR_BGR2RGB))

        out = {}
        if results.pose_landmarks:
            out['body'] = self.__convert_body_keypoints(results.pose_landmarks.landmark, image_width, image_height)
        if results.right_hand_landmarks:
            out['right_hand'] = self.__convert_hand_keypoints(results.right_hand_landmarks.landmark, image_width, image_height, '')
        if results.left_hand_landmarks:
            out['left_hand'] = self.__convert_hand_keypoints(results.left_hand_landmarks.landmark, image_width, image_height, '')

        return out
