
import cv2
import mediapipe as mp


class MediaPipeDetector():

    def __init__(self, static_image_mode):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=static_image_mode, min_detection_confidence=0.4, model_complexity=2)
        self.mp_pose_drawing = mp.solutions.drawing_utils

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode, max_num_hands=2, min_detection_confidence=0.4)
        self.mp_hands_drawing = mp.solutions.drawing_utils

    def get_mp_pose(self):
        return self.mp_pose

    def get_mp_hands(self):
        return self.mp_hands

    def detect_pose(self, image):
        copy_image = image.copy()

        results = self.pose.process(copy_image)
        height, width, _ = copy_image.shape
        landmarks = []

        if results.pose_landmarks:
            self.mp_pose_drawing.draw_landmarks(image=copy_image, landmark_list=results.pose_landmarks, connections=self.mp_pose.POSE_CONNECTIONS)
            for landmark in results.pose_landmarks.landmark:
                landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

        return copy_image, landmarks

    def detect_hands(self, image):

        # copy_image = cv2.flip(image.copy(), 1)
        # results = self.hands.process(cv2.flip(cv2.cvtColor(copy_image, cv2.COLOR_BGR2RGB), 1))

        # copy_image = self.resize(image.copy())
        copy_image = image.copy()

        results = self.hands.process(copy_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_hands_drawing.draw_landmarks(copy_image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return copy_image, results.multi_hand_landmarks
