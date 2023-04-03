import math


class PoseDeterminator:

    def __init__(self, pose_detector, high_quality_pose_detector):
        self.__pose_detector = pose_detector
        self.__high_quality_pose_detector = high_quality_pose_detector
        self.__is_high_quality_mode = False

        self.__body_vector_list = [('right_wrist', 'right_elbow'),
                                   ('left_wrist', 'left_elbow'),
                                   ('right_elbow', 'right_shoulder'),
                                   ('left_elbow', 'left_shoulder'),
                                   ('right_shoulder', 'right_hip'),
                                   ('left_shoulder', 'left_hip'),
                                   ('right_hip', 'right_knee'),
                                   ('left_hip', 'left_knee'),
                                   ('right_knee', 'right_ankle'),
                                   ('left_knee', 'left_ankle'),
                                   ('right_shoulder', 'left_shoulder'),
                                   ('right_hip', 'left_hip')]

        self.__body_angel_list = [('right_elbow', 'right_shoulder', 'right_hip'),
                                  ('right_wrist', 'right_elbow', 'right_shoulder'),
                                  ('right_shoulder', 'right_hip', 'right_knee'),
                                  ('right_hip', 'right_knee', 'right_ankle'),
                                  ('left_elbow', 'left_shoulder', 'left_hip'),
                                  ('left_wrist', 'left_elbow', 'left_shoulder'),
                                  ('left_shoulder', 'left_hip', 'left_knee'),
                                  ('left_hip', 'left_knee', 'left_ankle')]

    def set_high_quality_mode(self, is_high_quality_mode):
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

        x_min = min(vec_a[0][0], vec_a[1][0], vec_b[0][0], vec_b[1][0])
        x_max = max(vec_a[0][0], vec_a[1][0], vec_b[0][0], vec_b[1][0])
        y_min = min(vec_a[0][1], vec_a[1][1], vec_b[0][1], vec_b[1][1])
        y_max = max(vec_a[0][1], vec_a[1][1], vec_b[0][1], vec_b[1][1])

        if x_min <= x <= x_max and y_min <= y <= y_max:
            return round(x, 2), round(y, 2)
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

    def __get_pose_angles(self, kpd, crossings):
        angel_list = {}
        for k in crossings:
            if crossings[k] is not None:
                l = k.split(',')
                angel_list['angel,%s,%s,%s' % (l[2], '?', l[4])] = \
                    self.__calculate_vectors_angle(kpd[l[2]], crossings[k], kpd[l[4]])

        for a in self.__body_angel_list:
            if a[0] in kpd and a[1] in kpd and a[2] in kpd:
                angel_list['angel,%s,%s,%s' % (a[0], a[1], a[2])] = \
                    self.__calculate_vectors_angle(kpd[a[0]], kpd[a[1]], kpd[a[2]])

        return angel_list

    def __get_pose_crossings(self, kpd):
        out = {}
        list = self.__body_vector_list.copy()
        for v_1 in list:
            list.remove(v_1)
            for v_2 in list:
                if v_1[0] in kpd and v_1[1] in kpd and v_2[0] in kpd and v_2[1] in kpd and \
                        (v_1[0] != v_2[0] and v_1[0] != v_2[1] and v_1[1] != v_2[0] and v_1[1] != v_2[1]):
                    intersection = self.__get_vectors_intersection((kpd[v_1[0]], kpd[v_1[1]]), (kpd[v_2[0]], kpd[v_2[1]]))
                    if intersection is not None:
                        out['crossing,%s,%s,%s,%s' % (v_1[0], v_1[1], v_2[0], v_2[1])] = intersection
        return out

    def __reset_wrist(self, pose_and_hands):
        # right_hand in body and in hand list
        if 'right_hand' in pose_and_hands and 'wrist' in pose_and_hands['right_hand']:
            pose_and_hands['body']['right_wrist'] = pose_and_hands['right_hand']['wrist']
        if 'right_hand' in pose_and_hands and 'right_wrist' in pose_and_hands['body']:
            pose_and_hands['right_hand']['wrist'] = pose_and_hands['body']['right_wrist']

        # left_hand in body and in hand list
        if 'left_hand' in pose_and_hands and 'wrist' in pose_and_hands['left_hand']:
            pose_and_hands['body']['left_wrist'] = pose_and_hands['left_hand']['wrist']
        if 'left_hand' in pose_and_hands and 'left_wrist' in pose_and_hands['body']:
            pose_and_hands['left_hand']['wrist'] = pose_and_hands['body']['left_wrist']
        return pose_and_hands

    def __is_top_part_body_only(self, pose):
        down_part_body = ['left_hip', 'left_knee', 'left_ankle',
                          'right_hip', 'right_knee', 'right_ankle']
        for p in down_part_body:
            if p in pose['body']:
                return False
        return True

    def __check_number_of_known_key_points(self, pose):
        is_ok = True
        if 'body' not in pose or (len(pose['body']) <= (17 * 0.8) and not self.__is_top_part_body_only(pose)):
            is_ok = False
        if 'right_hand' not in pose or len(pose['right_hand']) <= (21 * 0.8):
            is_ok = False
        if 'left_hand' not in pose or len(pose['left_hand']) <= (21 * 0.8):
            is_ok = False
        return is_ok

    def __merge_dicts(self, main, additional):
        return {**main, **additional}

    def __merge_key_points(self, main_pose, additional_pose):
        pose = {}
        pose['body'] = self.__merge_dicts(additional_pose['body'] if 'body' in additional_pose else {},
                                          main_pose['body'] if 'body' in main_pose else {},)
        pose['right_hand'] = self.__merge_dicts(additional_pose['right_hand'] if 'right_hand' in additional_pose else {},
                                          main_pose['right_hand'] if 'right_hand' in main_pose else {},)
        pose['left_hand'] = self.__merge_dicts(additional_pose['left_hand'] if 'left_hand' in additional_pose else {},
                                          main_pose['left_hand'] if 'left_hand' in main_pose else {},)
        return pose

    def determinate_pose(self, pil_image):
        pose_and_hands = self.__pose_detector.detect_pose(pil_image)

        if not self.__check_number_of_known_key_points(pose_and_hands) and self.__is_high_quality_mode:
            pose_additional = self.__high_quality_pose_detector.detect_pose(pil_image)
            pose_and_hands = self.__merge_key_points(pose_and_hands, pose_additional)

        if 'body' in pose_and_hands:
            pose_and_hands = self.__reset_wrist(pose_and_hands)
            crossings = self.__get_pose_crossings(pose_and_hands['body'])
            angels = self.__get_pose_angles(pose_and_hands['body'], crossings)
            return pose_and_hands, angels, crossings

        return None, None, None
