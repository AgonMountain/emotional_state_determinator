import math
from math import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class PoseCompare:

    def __init__(self):
        pass

    def __rotate_point(self, point, angle, center_point=(0, 0)):
        angle_rad = radians(angle % 360)

        new_point = (point[0] - center_point[0], point[1] - center_point[1])
        new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                     new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))

        new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
        return new_point

    def __rotate_polygon(self, polygon, angle, center_point=(0, 0)):
        rotated_polygon = []
        for corner in polygon:
            rotated_corner = self.__rotate_point(corner, angle, center_point)
            rotated_polygon.append(rotated_corner)
        return rotated_polygon

    def __compare_angels(self, angel_a, angel_b):
        a = max(angel_a, angel_b)
        b = min(angel_a, angel_b)

        a_k = round(a / 180, 10)
        b_k = round(b / 180, 10)

        return round((b_k * 100) / a_k, 2)

    def angle(self, a, b, c):
        a_x, a_y = a
        b_x, b_y = b
        c_x, c_y = c
        angle = math.degrees(math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x))
        if angle < 0:
            angle *= -1
        if angle > 180:
            angle = 360 - angle

        return round(angle, 2)

    def __q(self, p_list):
        result = 1

        for el in p_list:
            result *= el

        return round((result / ((100) ** len(p_list))) * 100, 2)

    def is_open_angel(self, a, b, c, rotate_clockwise=True):
        '''
        Определение открытости угла по повороту и выравниваю угла c основанием на двух опорных точках,
        угол открыт - точка C выше повертикали основания опорных точек, иначе - угол закрытый
        :param a: опорная крайняя точка
        :param b: опорная центральная точка
        :param c: крайняя точка
        :rotate_clockwise: True - по часовой, False - против часовой
        :return: истинности утверждения что угол является открытым
        '''
        angel = self.angle(a, b, (a[0], b[1]))
        angel *= 1 if rotate_clockwise else -1  # поворот угла по часовой или против часовой

        list = self.__rotate_polygon((a, b, c), angel, b)
        a, b, c = list[0], list[1], list[2]

        return c[1] <= a[1]

    def compare(self, inaccuracy, hot_pose_angels, cold_pose_angels):

        temp_0 = 0
        body_percentage_dict = {}

        for i in cold_pose_angels.keys():

            if len(cold_pose_angels[i].keys()):
                temp_0 += 1

            temp = 0
            element_percentage_dict = {}

            for j in cold_pose_angels[i].keys():

                if j in hot_pose_angels[i]:
                    c = cold_pose_angels[i][j]
                    h = hot_pose_angels[i][j]

                    if (c > 0 and h > 0) or (c < 0 and h < 0):
                        f = self.__compare_angels(c, h) + inaccuracy
                    elif (170 <= c <= 180 or -170 >= c >= -180) and (170 <= h <= 180 or -170 >= h >= -180):
                        c *= -1 if -170 >= c >= -180 else 1
                        h *= -1 if -170 >= h >= -180 else 1
                        f = self.__compare_angels(c, h) + inaccuracy
                    else:
                        f = 0
                    element_percentage_dict[j] = 100 if f > 100 else f
                    temp += 1

            if len(element_percentage_dict.values()) > 0:
                t = (temp / len(cold_pose_angels[i].keys()))
                x = self.__q(element_percentage_dict.values())
                body_percentage_dict[i] = x * t


        t = (len(body_percentage_dict.keys()) / temp_0)
        x = self.__q(body_percentage_dict.values())
        a = x * t
        return a


if __name__ == '__main__':
    p = PoseCompare()

    a = (180, 20)
    b = (170, 80)
    c = (138, 40)
    w = False

    print(p.is_open_angel(a, b, c, w))
