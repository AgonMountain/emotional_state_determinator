import math
import cv2


class PoseDeterminator:

    def __init__(self, detector):
        self.detector = detector

    def __calculate_angle(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        angle = math.degrees(math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x))
        if angle < 0:
            angle *= -1
        return round(angle, 2)

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

    def __get_key_points_proximity(self, key_points):
        left_right = ['left_', 'right_']
        out = {}
        for p in left_right:
            # out[p + 'wrist_ear'] = [self.__included_in_circle(key_points[p + 'wrist'], key_points[p + 'ear'], 56),
            #                         round(self.__get_distance_between(key_points[p + 'wrist'], key_points[p + 'ear']) , 2)]
            # out[p + 'wrist_mouth'] = [self.__included_in_circle(key_points[p + 'wrist'], key_points[p + 'mouth'], 72),
            #                         round(self.__get_distance_between(key_points[p + 'wrist'], key_points[p + 'mouth']) , 2)]
            out[p + 'wrist_ear'] = round(self.__get_distance_between(key_points[p + 'wrist'], key_points[p + 'ear']), 2)
            out[p + 'wrist_mouth'] = round(self.__get_distance_between(key_points[p + 'wrist'], key_points[p + 'mouth']), 2)

        return out

    def determinate_pose(self, image):

        pose = self.detector.detect(image)

        angels = self.__get_pose_angles(pose['body'])
        crossings = self.__get_pose_crossing(pose['body'])
        proximitys = self.__get_key_points_proximity(pose['body'])

        return pose, angels, crossings, proximitys
