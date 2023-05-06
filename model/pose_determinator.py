import math


class PoseDeterminator:

    def __init__(self, pose_detector, high_quality_pose_detector=None):
        self.__pose_detector = pose_detector

        self.__high_quality_pose_detector = high_quality_pose_detector
        self.__is_high_quality_mode = False

        self.__body_top_angel_list = [('right_elbow', 'right_shoulder', 'left_shoulder'),
                                      ('right_elbow', 'right_shoulder', 'right_hip'),
                                      ('right_wrist', 'right_elbow', 'right_shoulder'),
                                      ('left_elbow', 'left_shoulder', 'right_shoulder'),
                                      ('left_elbow', 'left_shoulder', 'left_hip'),
                                      ('left_wrist', 'left_elbow', 'left_shoulder')]

        self.__body_down_angel_list = [('right_shoulder', 'right_hip', 'right_knee'),
                                       ('right_hip', 'right_knee', 'right_ankle'),
                                       ('left_shoulder', 'left_hip', 'left_knee'),
                                       ('left_hip', 'left_knee', 'left_ankle')]

        self.__body_top_vector_list = [('right_wrist', 'right_elbow'),
                                       ('left_wrist', 'left_elbow'),
                                       ('right_elbow', 'right_shoulder'),
                                       ('left_elbow', 'left_shoulder')]

        self.__body_down_vector_list = [('right_hip', 'right_knee'),
                                        ('left_hip', 'left_knee'),
                                        ('right_knee', 'right_ankle'),
                                        ('left_knee', 'left_ankle')]

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
        return round(angle, 2)
    #
    def __calculate_limbs_angle(self, dict, a, b, c):
        if a in dict and b in dict and c in dict:
            return self.__calculate_vectors_angle(dict[a], dict[b], dict[c])
        return None

    def __get_pose_angles(self, pose_points, crossings):
        out_angel_list = {'body_top_angels': {}, 'body_down_angels': {},
                          'body_top_crossings_angels': {}, 'body_down_crossings_angels': {}}

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

        for key, angels in {'body_top_crossings_angels': crossings['body_top_crossings'].items(),
                            'body_down_crossings_angels': crossings['body_down_crossings'].items()}.items():
            dict = {}
            for k, v in angels:
                a = k.split(',')[2]
                b = k.split(',')[4]

                dict['angel,%s,%s,%s' % (a, '?', b)] = self.__calculate_vectors_angle(pose_points[a], v, pose_points[b])

            out_angel_list[key] = dict

        return out_angel_list

    def __get_pose_crossings(self, points):
        out_crossing_list = {'body_top_crossings': {}, 'body_down_crossings': {}}

        for key, vector_list in {'body_top_crossings': self.__body_top_vector_list.copy(),
                                 'body_down_crossings': self.__body_down_vector_list.copy()}.items():
            dict = {}
            for i in range(len(vector_list)):
                for j in range(len(vector_list)):

                    j = j + i + 1
                    if j == len(vector_list):
                        break

                    a = vector_list[i][0]
                    b = vector_list[i][1]
                    c = vector_list[j][0]
                    d = vector_list[j][1]

                    # проверка наличия hot точек в наборе cold точек
                    # проверка что векторы пересекаются, а не соединяются
                    if (a in points and b in points and c in points and d in points) and \
                            (a != c and a != d and b != c and b != d):

                        vec_a = (points[a], points[b])
                        vec_b = (points[c], points[d])

                        intersection = self.__get_vectors_intersection(vec_a, vec_b)

                        if intersection is not None:
                            dict['crossing,%s,%s,%s,%s' % (a, b, c, d)] = intersection

            out_crossing_list[key] = dict

        return out_crossing_list


    def __merge_dicts(self, main, additional):
        return {**main, **additional}

    def __merge_key_points(self, main_pose, additional_pose):
        pose = {}

        pose['body'] = \
            self.__merge_dicts(main_pose['body'] if  main_pose['body'] is not None else {},
                               additional_pose['body'] if additional_pose['body'] is not None else {})
        pose['right_hand'] = \
            self.__merge_dicts(main_pose['right_hand'] if main_pose['right_hand'] is not None else {},
                               additional_pose['right_hand'] if additional_pose['right_hand'] is not None else {})
        pose['left_hand'] = \
            self.__merge_dicts(main_pose['left_hand'] if main_pose['left_hand'] is not None else {},
                               additional_pose['left_hand'] if additional_pose['left_hand'] is not None else {})

        return pose

    def determinate_pose(self, pil_image):
        pose = self.__pose_detector.detect_pose(pil_image)

        if self.__is_high_quality_mode:
            pose_additional = self.__high_quality_pose_detector.detect_pose(pil_image)
            pose = self.__merge_key_points(pose, pose_additional)

        if pose['body'] is not None:
            crossings = self.__get_pose_crossings(pose['body'])
            angels = self.__get_pose_angles(pose['body'], crossings)
            return pose, angels, crossings

        return None, None, None
