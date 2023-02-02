import math
import cv2

class EmotionalStateDeterminator():

    def __init__(self, detector):
        self.detector = detector

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

    def get_pose_angle(self, mp_pose, landmarks):
        if landmarks:
            left_elbow_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

            right_elbow_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

            left_shoulder_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

            right_shoulder_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

            left_knee_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

            right_knee_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

            right_hip_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])

            left_hip_angle = self.calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

            return {'left_elbow_angle': left_elbow_angle,
                    'right_elbow_angle': right_elbow_angle,
                    'left_shoulder_angle': left_shoulder_angle,
                    'right_shoulder_angle': right_shoulder_angle,
                    'left_knee_angle': left_knee_angle,
                    'right_knee_angle': right_knee_angle,
                    'right_hip_angle': right_hip_angle,
                    'left_hip_angle': left_hip_angle}

    def get_pose_crossing(self, mp_pose, landmarks):

        if landmarks:
            crossing_forearm = self.is_crossing_vectors(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value],
                                                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

            crossing_shin = self.is_crossing_vectors(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

            crossing_hip = self.is_crossing_vectors(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                     landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

            crossing_ship_hip = self.is_crossing_vectors(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                          landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]) or \
                                        self.is_crossing_vectors(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

            return {'crossing_forearm': crossing_forearm,
                    'crossing_shin': crossing_shin,
                    'crossing_hip': crossing_hip,
                    'crossing_ship_hip': crossing_ship_hip}

    def classify_pose(self, img_array):

        img_array, hands_landmarks = self.detector.detect_hands(img_array)
        img_array, body_landmarks = self.detector.detect_pose(img_array)
        mp_pose = self.detector.get_mp_pose()

        label = 'Unknown Pose'
        color = (0, 0, 255)

        angels = self.get_pose_angle(mp_pose, body_landmarks)
        crossings = self.get_pose_crossing(mp_pose, body_landmarks)

        left_elbow_angle = angels['left_elbow_angle']
        right_elbow_angle = angels['right_elbow_angle']
        left_shoulder_angle = angels['left_shoulder_angle']
        right_shoulder_angle = angels['right_shoulder_angle']
        left_knee_angle = angels['left_knee_angle']
        right_knee_angle = angels['right_knee_angle']

        crossing_forearm = crossings['crossing_forearm']
        crossing_shin = crossings['crossing_shin']
        crossing_hip = crossings['crossing_hip']
        crossing_ship_hip = crossings['crossing_ship_hip']

        if crossing_forearm and \
                (left_elbow_angle > 25 and left_elbow_angle < 65) and \
                (right_elbow_angle > 25 and right_elbow_angle < 65) and \
                (left_shoulder_angle > 0 and left_shoulder_angle < 25) and \
                (right_shoulder_angle > 0 and right_shoulder_angle < 25):
            label = 'Negative'

        if label != 'Unknown Pose':
            color = (0, 255, 0)

        cv2.putText(img_array, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

        # if display:
        #     plt.figure(figsize=[10,10])
        #     plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        #
        # else:
        #     return self.img, label
        return img_array
