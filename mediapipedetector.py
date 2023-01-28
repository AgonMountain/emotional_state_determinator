import math
import cv2
import mediapipe as mp


class MediaPipeDetector():

    def __init__(self, static_image_mode):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=static_image_mode,
                                      min_detection_confidence=0.4,
                                      model_complexity=2)
        self.mp_pose_drawing = mp.solutions.drawing_utils

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode,
                                         max_num_hands=2,
                                         min_detection_confidence=0.4)
        self.mp_hands_drawing = mp.solutions.drawing_utils

    def resize(self, image):

        DESIRED_HEIGHT = 640
        DESIRED_WIDTH = 960

        h, w = image.shape[:2]
        if h < w:
            img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h / (w / DESIRED_WIDTH))))
        else:
            img = cv2.resize(image, (math.floor(w / (h / DESIRED_HEIGHT)), DESIRED_HEIGHT))

        return img

    def calculate_angle(self, landmark1, landmark2, landmark3):

        x1, y1, _ = landmark1
        x2, y2, _ = landmark2
        x3, y3, _ = landmark3
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            # angle += 360
            angle *= -1
        return angle

    def ccw(self, A, B, C):
        a_x, a_y, _ = A
        b_x, b_y, _ = B
        c_x, c_y, _ = C
        return (c_y - a_y) * (b_x - a_x) > (b_y - a_y) * (c_x - a_x)

    def is_crossing_vectors(self, vec1_point1, vec1_point2, vec2_point1, vec2_point2):
        return self.ccw(vec1_point1, vec2_point1, vec2_point2) != self.ccw(vec1_point2, vec2_point1, vec2_point2) and \
                self.ccw(vec1_point1, vec1_point2, vec2_point1) != self.ccw(vec1_point1, vec1_point2, vec2_point2)

    def get_pose_angle(self, landmarks):
        if landmarks:
            left_elbow_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                                      landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                                      landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])

            right_elbow_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                       landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                                       landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value])

            left_shoulder_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                                         landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                                         landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value])

            right_shoulder_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                          landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                          landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value])

            left_knee_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                                     landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                                     landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

            right_knee_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                      landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                      landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value])

            right_hip_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                     landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                     landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value])

            left_hip_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                                    landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                                    landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value])

            return {'left_elbow_angle': left_elbow_angle,
                    'right_elbow_angle': right_elbow_angle,
                    'left_shoulder_angle': left_shoulder_angle,
                    'right_shoulder_angle': right_shoulder_angle,
                    'left_knee_angle': left_knee_angle,
                    'right_knee_angle': right_knee_angle,
                    'right_hip_angle': right_hip_angle,
                    'left_hip_angle': left_hip_angle}

    def get_pose_crossing(self, landmarks):

        if landmarks:
            crossing_forearm = self.is_crossing_vectors(landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                                         landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value],
                                                         landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                                         landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])

            crossing_shin = self.is_crossing_vectors(landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                      landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                                      landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                                      landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

            crossing_hip = self.is_crossing_vectors(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                     landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                     landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                                     landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value])

            crossing_ship_hip = self.is_crossing_vectors(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                          landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                                          landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                                          landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]) or \
                                        self.is_crossing_vectors(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                          landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                          landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                                          landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

            return {'crossing_forearm': crossing_forearm,
                    'crossing_shin': crossing_shin,
                    'crossing_hip': crossing_hip,
                    'crossing_ship_hip': crossing_ship_hip}

    def detect_pose(self, image):

        # copy_image = self.resize(image.copy())
        copy_image = image.copy()

        results = self.pose.process(copy_image)
        # height, width, _ = copy_image.shape
        # landmarks = []

        if results.pose_landmarks:
            self.mp_pose_drawing.draw_landmarks(image=copy_image,
                                                landmark_list=results.pose_landmarks,
                                                connections=self.mp_pose.POSE_CONNECTIONS)
            # for landmark in results.pose_landmarks.landmark:
            #     landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

        return copy_image

    def detect_hands(self, image):

        # copy_image = cv2.flip(image.copy(), 1)
        # results = self.hands.process(cv2.flip(cv2.cvtColor(copy_image, cv2.COLOR_BGR2RGB), 1))

        # copy_image = self.resize(image.copy())
        copy_image = image.copy()

        results = self.hands.process(copy_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_hands_drawing.draw_landmarks(copy_image,
                                                     hand_landmarks,
                                                     self.mp_hands.HAND_CONNECTIONS)

        return copy_image




# class Determinator():
#
#
#
#
#
# def classifyPose(mp_pose, landmarks, output_image, display=False):
#
#     label = 'Unknown Pose'
#     color = (0, 0, 255)
#
#     angels = getPoseAngle(mp_pose, landmarks)
#     crossings = getPoseCrossing(mp_pose, landmarks)
#
#     left_elbow_angle = angels['left_elbow_angle']
#     right_elbow_angle = angels['right_elbow_angle']
#     left_shoulder_angle = angels['left_shoulder_angle']
#     right_shoulder_angle = angels['right_shoulder_angle']
#     left_knee_angle = angels['left_knee_angle']
#     right_knee_angle = angels['right_knee_angle']
#
#     crossing_forearm = crossings['crossing_forearm']
#     crossing_shin = crossings['crossing_shin']
#     crossing_hip = crossings['crossing_hip']
#     crossing_ship_hip = crossings['crossing_ship_hip']
#
#     if crossing_forearm and \
#             (left_elbow_angle > 25 and left_elbow_angle < 65) and \
#             (right_elbow_angle > 25 and right_elbow_angle < 65) and \
#             (left_shoulder_angle > 0 and left_shoulder_angle < 25) and \
#             (right_shoulder_angle > 0 and right_shoulder_angle < 25):
#         label = 'Negative'
#
#     if label != 'Unknown Pose':
#         color = (0, 255, 0)
#
#     cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
#
#     if display:
#         plt.figure(figsize=[10,10])
#         plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
#
#     else:
#         return output_image, label