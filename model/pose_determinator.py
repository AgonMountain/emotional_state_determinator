import math
from model.pose_compare import PoseCompare


class PoseDeterminator:

    def __init__(self, pose_detector, high_quality_pose_detector=None):
        self.__pose_detector = pose_detector

        self.__high_quality_pose_detector = high_quality_pose_detector
        self.__is_high_quality_mode = False
        self.__p = PoseCompare()

        # !!!! !!!! WARNING !!!! !!!! для определения типа угла влияет последовательность ключевых точек
        self.__body_top_angel_list = [
            ('center_shoulder', 'right_shoulder', 'right_elbow'),
            ('right_shoulder', 'right_elbow', 'right_wrist'),
            ('right_elbow', 'right_wrist', 'right_hand'),
            ('center_shoulder', 'left_shoulder', 'left_elbow'),
            ('left_shoulder', 'left_elbow', 'left_wrist'),
            ('left_elbow', 'left_wrist', 'left_hand'),
        ]
        # !!!! !!!! WARNING !!!! !!!! для определения типа угла влияет последовательность ключевых точек
        self.__body_down_angel_list = [
            ('center_hip', 'right_hip', 'right_knee'),
            ('right_hip', 'right_knee', 'right_ankle'),
            ('right_knee', 'right_ankle', 'right_foot'),
            ('center_hip', 'left_hip', 'left_knee'),
            ('left_hip', 'left_knee', 'left_ankle'),
            ('left_knee', 'left_ankle', 'left_foot')
        ]

    def set_high_quality_mode(self, is_high_quality_mode):
        if self.__high_quality_pose_detector is not None:
            self.__is_high_quality_mode = is_high_quality_mode

    def __calculate_vectors_angle(self, a, b, c, hand):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c

        angle = math.degrees(math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x))
        if angle < 0:
            angle *= -1
        if angle > 180:
            angle = 360 - angle

        if 'right' in hand:
            angle *= -1 if not self.__p.is_open_angel(a, b, c, True) else 1
        else:
            angle *= -1 if not self.__p.is_open_angel(a, b, c, False) else 1

        return round(angle, 2)

    def __get_pose_angles(self, pose_points):
        out_angel_list = {'body_top_angels': {}, 'body_down_angels': {}}

        for key, angels in {'body_top_angels': self.__body_top_angel_list.copy(),
                            'body_down_angels': self.__body_down_angel_list.copy()}.items():
            dict = {}
            for angel_points in angels:
                a = angel_points[0]
                b = angel_points[1]
                c = angel_points[2]
                hand = 'right' if ('right' in a or 'right' in b or 'right' in c) else 'left'
                if a in pose_points and b in pose_points and c in pose_points:
                    dict['angel,%s,%s,%s' % (a, b, c)] = \
                        self.__calculate_vectors_angle(pose_points[a], pose_points[b], pose_points[c], hand)

            out_angel_list[key] = dict

        return out_angel_list

    def __merge_dicts(self, main, additional):
        if main is not None and additional is not None:
            result = {**main, **additional}
        else:
            result = main if main is not None else additional if additional is not None else None
        return result


    def determinate_pose(self, pil_image):
        pose = self.__pose_detector.detect_pose(pil_image)

        if self.__is_high_quality_mode:
            pose_additional = self.__high_quality_pose_detector.detect_pose(pil_image)
            pose = self.__merge_dicts(pose_additional, pose)

        if pose is not None:
            angels = self.__get_pose_angles(pose)
            return pose, angels

        return None, None
