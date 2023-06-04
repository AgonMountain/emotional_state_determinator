import math
from math import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class PoseCompare:

    def __init__(self):
        pass

    def beetwen(self, a, b):
        x1, y1 = a[0], a[1]
        x2, y2 = b[0], b[1]
        return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

    def rotate_point(self, point, angle, center_point=(0, 0)):
        """Rotates a point around center_point(origin by default)
        Angle is in degrees.
        Rotation is counter-clockwise
        """
        angle_rad = radians(angle % 360)
        # Shift the point so that center_point becomes the origin
        new_point = (point[0] - center_point[0], point[1] - center_point[1])
        new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                     new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
        # Reverse the shifting we have done
        new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
        return new_point

    def rotate_polygon(self, polygon, angle, center_point=(0, 0)):
        """Rotates the given polygon which consists of corners represented as (x,y)
        around center_point (origin by default)
        Rotation is counter-clockwise
        Angle is in degrees
        """
        rotated_polygon = []
        for corner in polygon:
            rotated_corner = self.rotate_point(corner, angle, center_point)
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

    def is_open_angel(self, a, b, c, hand):
        f = (b[0] + (b[0] - a[0]), b[1] + (b[1] - a[1]))

        angel = p.angle(a, b, (a[0], b[1]))
        if hand == 'left':
            angel *= -1
        list = p.rotate_polygon((a, b, f, c), angel, b)
        a = list[0]
        b = list[1]
        f = list[2]
        c = list[3]

        a = a[0] - 100, a[1]
        b = b[0], b[1] + 100
        f = f[0] + 100, f[1]

        point = Point(c[0], c[1])
        polygon = Polygon([a, b, f])
        return not polygon.contains(point)

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
                    f = self.__compare_angels(c, h) + inaccuracy
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

    a = (140, 10)
    b = (110, 70)
    c = (150, 100)

    print(p.is_open_angel(a, b, c, 'right'))
