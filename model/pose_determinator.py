import math
import cv2

from openpose_detector import OpenPoseDetector
from mediapipe_detector_v2 import MediapipeDetector

class PoseDeterminator():

    def __init__(self, detector):
        self.detector = detector

    def __calculate_angle(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        angle = math.degrees(math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x))
        if angle < 0:
            angle += 360
        return angle

    def __ccw(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        return (c_y - a_y) * (b_x - a_x) > (b_y - a_y) * (c_x - a_x)

    def __included_in_circle(self, a, b, r):
        '''
        :param a: координата первой точки
        :param b: координата второй точки, являющейся центром окружности
        :param r: радиус оркжности
        :return:
        '''
        a_x, a_y = a
        b_x, b_y = b
        return (a_x - b_x) * (a_x - b_x) + (a_y - b_y) * (a_y - b_y) <= r * r

    def __is_crossing_vectors(self, a, b, c, d):
        '''
        :param a: первая точка первого вектора
        :param b: вторая точка первого вектора
        :param c: первая точка второго вектора
        :param d: вторая точка второго вектора
        :return:
        '''
        return self.__ccw(a, c, d) != self.__ccw(b, c, d) and \
                self.__ccw(a, b, c) != self.__ccw(a, b, d)

    def __get_pose_angles(self, key_points):
        left_right = ['left_', 'right_']

        out = {}
        for p in left_right:
            out[p + 'elbow_angle'] = self.__calculate_angle(key_points[p + 'shoulder'],
                                                            key_points[p + 'elbow'],
                                                            key_points[p + 'wrist'])
            out[p + 'shoulder_angle'] = self.__calculate_angle(key_points[p + 'elbow'],
                                                               key_points[p + 'shoulder'],
                                                               key_points[p + 'hip'])
            out[p + 'knee_angle'] = self.__calculate_angle(key_points[p + 'hip'],
                                                           key_points[p + 'knee'],
                                                           key_points[p + 'ankle'])
            out[p + 'hip_angle'] = self.__calculate_angle(key_points[p + 'shoulder'],
                                                           key_points[p + 'hip'],
                                                           key_points[p + 'knee'])

        return out

    def __get_pose_crossing(self, key_points):
        out = {}

        out['crossing_forearm'] = self.__is_crossing_vectors(key_points['right_elbow'],
                                                            key_points['right_wrist'],
                                                            key_points['left_elbow'],
                                                            key_points['left_wrist'])
        out['crossing_shin'] = self.__is_crossing_vectors(key_points['right_knee'],
                                                             key_points['right_ankle'],
                                                             key_points['left_knee'],
                                                             key_points['left_ankle'])
        out['crossing_hip'] = self.__is_crossing_vectors(key_points['right_hip'],
                                                             key_points['right_knee'],
                                                             key_points['left_hip'],
                                                             key_points['left_knee'])
        out['crossing_ship_hip'] = self.__is_crossing_vectors(key_points['right_hip'],
                                                             key_points['right_ankle'],
                                                             key_points['left_hip'],
                                                             key_points['left_knee']) or \
                                   self.__is_crossing_vectors(key_points['right_hip'],
                                                             key_points['right_knee'],
                                                             key_points['left_knee'],
                                                             key_points['left_ankle'])

        return out

    def __get_distance_between(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        return math.hypot(b_x - a_x, b_y - a_y)

    def get_key_points_proximity(self, key_points):
        left_right = ['left_', 'right_']
        out = {}
        for p in left_right:
            out[p + 'wrist_ear'] = [self.__included_in_circle(key_points[p + 'wrist'], key_points[p + 'ear'], 56),
                                    self.__get_distance_between(key_points[p + 'wrist'], key_points[p + 'ear'])]
            out[p + 'wrist_mouth'] = [self.__included_in_circle(key_points[p + 'wrist'], key_points[p + 'mouth'], 72),
                                    self.__get_distance_between(key_points[p + 'wrist'], key_points[p + 'mouth'])]

        return out


    def classify_pose(self, img_array):

        # img_array, hands_landmarks = self.detector.detect_hands(img_array)
        img_array, body_landmarks = self.detector.detect_pose(img_array)
        mp_pose = self.detector.get_mp_pose()

        label = 'Unknown Pose'
        color = (0, 0, 255)

        angels = self.__get_pose_angle(mp_pose, body_landmarks)
        crossings = self.__get_pose_crossing(mp_pose, body_landmarks)

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


m = MediapipeDetector()
o = OpenPoseDetector()

p = PoseDeterminator(0)
print(p.get_key_points_proximity(m.detect('C:\\Users\\agonm\\OneDrive\\Рабочий стол\\Новая папка\\Screenshot_1.png')['body']))