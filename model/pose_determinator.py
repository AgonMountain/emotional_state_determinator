import math


class PoseDeterminator:

    def __init__(self, pose_detector, high_quality_pose_detector=None):
        self.__pose_detector = pose_detector

        self.__high_quality_pose_detector = high_quality_pose_detector
        self.__is_high_quality_mode = False

        self.__body_top_angel_list = [
            ('right_hand', 'right_wrist', 'right_elbow'),
            ('right_wrist', 'right_elbow', 'right_shoulder'),
            ('right_elbow', 'right_shoulder', 'center_shoulder'),
            ('left_hand', 'left_wrist', 'left_elbow'),
            ('left_wrist', 'left_elbow', 'left_shoulder'),
            ('left_elbow', 'left_shoulder', 'center_shoulder')
        ]

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

    def __get_vectors_intersection(self, vec_a, vec_b):
        xdiff = (vec_a[0][0] - vec_a[1][0], vec_b[0][0] - vec_b[1][0])
        ydiff = (vec_a[0][1] - vec_a[1][1], vec_b[0][1] - vec_b[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None
        d = (det(*vec_a), det(*vec_b))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        # проверка что перескаются отрезки, а не вектора (отсекаем варианты когда пересечение благодаря продлению)
        a_x_min = min(vec_a[0][0], vec_a[1][0])
        a_x_max = max(vec_a[0][0], vec_a[1][0])
        a_y_min = min(vec_a[0][1], vec_a[1][1])
        a_y_max = max(vec_a[0][1], vec_a[1][1])
        b_x_min = min(vec_b[0][0], vec_b[1][0])
        b_x_max = max(vec_b[0][0], vec_b[1][0])
        b_y_min = min(vec_b[0][1], vec_b[1][1])
        b_y_max = max(vec_b[0][1], vec_b[1][1])
        if (a_x_min <= x <= a_x_max and a_y_min <= y <= a_y_max) and \
                (b_x_min <= x <= b_x_max and b_y_min <= y <= b_y_max):
            return (round(x, 2), round(y, 2))
        else:
            return None

    def __calculate_vectors_angle(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        angle = math.degrees(math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x))
        if angle < 0:
            angle *= -1
        if angle > 180:
            angle = 360 - angle

        # ориентация угла, положительный угол - открытый угол, отрицательный - закрытый


        return round(angle, 2)
    #
    def __calculate_limbs_angle(self, dict, a, b, c):
        if a in dict and b in dict and c in dict:
            return self.__calculate_vectors_angle(dict[a], dict[b], dict[c])
        return None

    def __get_pose_angles(self, pose_points):
        out_angel_list = {'body_top_angels': {}, 'body_down_angels': {}}

        for key, angels in {'body_top_angels': self.__body_top_angel_list.copy(),
                            'body_down_angels': self.__body_down_angel_list.copy()}.items():
            dict = {}
            for angel_points in angels:
                a = angel_points[0]
                b = angel_points[1]
                c = angel_points[2]

                if a in pose_points and b in pose_points and c in pose_points:
                    dict['angel,%s,%s,%s' % (a, b, c)] = \
                        self.__calculate_vectors_angle(pose_points[a], pose_points[b], pose_points[c])

            out_angel_list[key] = dict

        return out_angel_list


    def __merge_dicts(self, main, additional):
        result = None
        if main is not None and additional is not None:
            result = {**main, **additional}
        else:
            result = main if main is not None else None
            result = additional if additional is not None else None
        return result


    def determinate_pose(self, pil_image):
        pose = self.__pose_detector.detect_pose(pil_image)

        if self.__is_high_quality_mode:
            pose_additional = self.__high_quality_pose_detector.detect_pose(pil_image)
            pose = self.__merge_dicts(pose, pose_additional)

        if pose is not None:
            angels = self.__get_pose_angles(pose)
            return pose, angels

        return None, None
