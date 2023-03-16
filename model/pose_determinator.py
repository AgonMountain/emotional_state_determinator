import math
import cv2


class PoseDeterminator:

    def __init__(self, pose_detector):
        self.pose_detector = pose_detector

    def __ccw(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        return (c_y - a_y) * (b_x - a_x) > (b_y - a_y) * (c_x - a_x)

    def __calculate_vectors_angle(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        angle = math.degrees(math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x))
        if angle < 0:
            angle *= -1
        return round(angle, 2)

    def __calculate_limbs_angle(self, dict, a, b, c):
        if a in dict and b in dict and c in dict :
            return self.__calculate_vectors_angle(dict[a], dict[b], dict[c])
        return None

    def __get_pose_angles(self, kpd):
        left_right = ['left_', 'right_']
        out = {}
        for p in left_right:
            out[p + 'elbow_angle'] = self.__calculate_limbs_angle(kpd, p + 'shoulder', p + 'elbow', p + 'wrist')
            out[p + 'shoulder_angle'] = self.__calculate_limbs_angle(kpd, p + 'elbow', p + 'shoulder', p + 'hip')
            out[p + 'knee_angle'] = self.__calculate_limbs_angle(kpd, p + 'hip', p + 'knee', p + 'ankle')
            out[p + 'hip_angle'] = self.__calculate_limbs_angle(kpd, p + 'shoulder', p + 'hip', p + 'knee')
        return out

    def __is_crossing_vectors(self, a, b, c, d):
        return self.__ccw(a, c, d) != self.__ccw(b, c, d) and \
                self.__ccw(a, b, c) != self.__ccw(a, b, d)

    def __is_limbs_crossing(self, dict, a, b, c, d):
        if a in dict and b in dict and c in dict and d in dict:
            return self.__is_crossing_vectors(dict[a], dict[b], dict[c], dict[d])
        return None

    def __get_pose_crossings(self, kpd):
        out = {}
        out['crossing_forearm'] = self.__is_limbs_crossing(kpd, 'right_elbow', 'right_wrist', 'left_elbow', 'left_wrist')
        out['crossing_shin'] = self.__is_limbs_crossing(kpd, 'right_knee', 'right_ankle', 'left_knee', 'left_ankle')
        out['crossing_hip'] = self.__is_limbs_crossing(kpd, 'right_hip', 'right_knee', 'left_hip', 'left_knee')
        out['crossing_ship_hip'] = self.__is_limbs_crossing(kpd, 'right_hip', 'right_ankle', 'left_hip', 'left_knee') or \
                                   self.__is_limbs_crossing(kpd, 'right_hip', 'right_knee', 'left_knee', 'left_ankle')
        return out

    def __get_distance_between_points(self, a, b):
        a_x, a_y = a
        b_x, b_y = b
        return math.hypot(b_x - a_x, b_y - a_y)

    def __get_distance_between_kp(self, dict, a, b):
        if a in dict and b in dict:
            return self.__get_distance_between_points(dict[a], dict[b])
        return None

    def __get_pose_kp_distances(self, kpd):
        left_right = ['left_', 'right_']
        out = {}
        for p in left_right:
            a = self.__get_distance_between_kp(kpd, p + 'wrist', p + 'ear')
            if a is not None:
                out[p + 'wrist_ear'] = round(a, 2)
            b = self.__get_distance_between_kp(kpd, p + 'wrist', p + 'mouth')
            if b is not None:
                out[p + 'wrist_mouth'] = round(b, 2)
        return out

    def determinate_pose(self, image):
        pose = self.pose_detector.detect(image)
        angels = self.__get_pose_angles(pose['body'])
        crossings = self.__get_pose_crossings(pose['body'])
        kp_distances = self.__get_pose_kp_distances(pose['body'])
        return pose, angels, crossings, kp_distances
