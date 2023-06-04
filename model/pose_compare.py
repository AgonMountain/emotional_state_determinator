import math

class PoseCompare:

    def __init__(self):
        pass

    def is_open_angel(self, a, b, c, hand):
        a_x, a_y = a[0], a[1]
        b_x, b_y = b[0], b[1]
        c_x, c_y = c[0], c[1]

        is_open = False

        if hand == 'right':
            # горизонтальная линия
            if c_x <= b_x <= a_x:
                if b_y >= min(a_y, c_y):
                    is_open = True
            # вертикальная линия первого типа
            if c_y <= b_y <= a_y:
                if b_x >= min(a_x, c_x):
                    is_open = True
            # вертикальная линия второго типа
            if c_y >= b_y >= a_y:
                if b_x <= max(a_x, c_x):
                    is_open = True
        elif hand == 'left':
            # горизонтальная линия
            if c_x <= b_x <= a_x:
                if b_y >= max(a_y, c_y):
                    is_open = True
            # вертикальная линия первого типа
            if c_y <= b_y <= a_y:
                if b_x <= min(a_x, c_x):
                    is_open = True
            # вертикальная линия второго типа
            if c_y >= b_y >= a_y:
                if b_x >= max(a_x, c_x):
                    is_open = True

        # исключение для позы вида скрещенные руки с открытыми углами
        if is_open:
            if (hand == 'right' and a_x < b_x) or (hand == 'left' and a_x > b_x):
                is_open = False

        return is_open

        # z = math.sqrt((b_x - a_x) ** 2 + (b_y - a_y) ** 2)
        # w = math.sqrt((b_x - c_x) ** 2 + (b_y - c_y) ** 2)
        # f_x, f_y = b_x + (b_x - a_x), b_y + (b_y - a_y)
        # l = math.sqrt((f_x - c_x) ** 2 + (f_y - c_y) ** 2)
        #
        # a_x, a_y = a_x, a_y
        # b_x, b_y = a_x + z, a_y
        # f_x, f_y = b_x + w, a_y
        # c_x, c_y = b_x + w, a_y + l

        # f_x, f_y = b_x + b_c_distance, a_y
        #
        # a_x, a_y = a_x - 10 * b_c_distance, a_y
        # b_x, b_y = b_x, b_y + 10 * b_c_distance
        # f_x, f_y = f_x + 10 * b_c_distance, f_y
        #
        # return not self.is_point_in_triangle((a_x, a_y), (b_x, b_y), (f_x, f_y), (c_x, c_y))


    def __compare_angels(self, angel_a, angel_b):
        a = max(angel_a, angel_b)
        b = min(angel_a, angel_b)

        a_k = round(a / 180, 10)
        b_k = round(b / 180, 10)

        return round((b_k * 100) / a_k, 2)

    def __q(self, p_list):
        result = 1

        for el in p_list:
            result *= el

        return round((result / ((100) ** len(p_list))) * 100, 2)

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

    d = PoseCompare()

    a_x, a_y = 160, 0
    b_x, b_y = 120, 90
    c_x, c_y = 70, 60

    print(d.is_open_angel((a_x, a_y), (b_x, b_y), (c_x, c_y), 'right'))
