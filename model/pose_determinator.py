import math
import cv2


class PoseDeterminator:

    def __init__(self, pose_detector_main, pose_detector_additional):
        self.pose_detector_main = pose_detector_main
        self.pose_detector_additional = pose_detector_additional

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

    def __check_body_wrist(self, pose):
        if 'right_hand' in pose and 'wrist' in pose['right_hand']:
            pose['body']['right_wrist'] = pose['right_hand']['wrist']
        if 'left_hand' in pose and 'wrist' in pose['left_hand']:
            pose['body']['left_wrist'] = pose['left_hand']['wrist']

        if 'right_hand' in pose and 'right_wrist' in pose['body']:
            pose['right_hand']['wrist'] = pose['body']['right_wrist']
        if 'right_hand' in pose and 'wrist' in pose['body']:
            pose['left_wrist']['wrist'] = pose['body']['left_wrist']

        return pose

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

    def determinate_pose(self, image):
        pose = self.pose_detector_main.detect(image)

        if not self.__check_number_of_known_key_points(pose):
            pose_additional = self.pose_detector_additional.detect(image)
            pose = self.__merge_key_points(pose, pose_additional)

        pose = self.__check_body_wrist(pose)

        angels = self.__get_pose_angles(pose['body'])
        crossings = self.__get_pose_crossings(pose['body'])
        kp_distances = self.__get_pose_kp_distances(pose['body'])
        return pose, angels, crossings, kp_distances
