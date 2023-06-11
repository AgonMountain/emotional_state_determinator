import math
from PIL import Image, ImageFont, ImageDraw
from model.pose_drawer import PoseDrawer

from model.pose_compare import PoseCompare


class EmotionalStateClassifier:

    def __init__(self, app, pose_determinator):
        self.__app = app
        self.__pose_determinator = pose_determinator
        self.__drawer = PoseDrawer()
        self.__comparer = PoseCompare()


    def __compare_poses(self, hot_angels, cold_pose_list, min_percent):
        similar_pose_list = []

        for cold_pose in cold_pose_list:
            cold_angels = cold_pose.get_pose_angels()
            inaccuracy = self.__app.get_inaccuracy()[cold_pose.get_inaccuracy()]

            similarity_percentage = self.__comparer.compare(inaccuracy, hot_angels, cold_angels)

            if similarity_percentage >= min_percent:
                similar_pose_list.append((similarity_percentage, cold_pose))

        return similar_pose_list

    def pp(self, pose_list):
        j = sum([p[0] for p in pose_list])

        m_dict = {}
        for p in pose_list:
            m_dict[p[1]] = (p[0] / j)

        lp_dict = {}
        for p in pose_list:
            lp_dict[p[1]] = (2 * p[0]) - j
        lp_min = min(lp_dict.values())
        b = 1
        if lp_min < 0:
            while True:
                b += 1
                if (lp_min + (100 * b)) > 0:
                    break

        e_dict = {}
        for k in m_dict.keys():
            e_dict[k] = (m_dict[k] * (lp_dict[k] + (100 * b))) / 100

        return self.iterp(e_dict)

    def iterp(self, list):
        negative_sum, positive_sum, neutral_sum = 0, 0, 0
        for k in list.keys():
            if k.get_state() == 'Нейтральное':
                neutral_sum += list[k]
            elif k.get_state() == 'Положительное':
                positive_sum += list[k]
            elif k.get_state() == 'Отрицательное':
                negative_sum += (list[k] * -1)

        if neutral_sum > 0.2:
            neutral_sum = 0.2

        sum = negative_sum + positive_sum + neutral_sum
        state = 'Неизвестное'

        if sum < (-0.1):
            state = 'Отрицательное'
        elif sum <= (0.2):
            state = 'Нейтральное'
        elif sum > (0.2):
            state = 'Положительное'

        return state

    def __modify_image(self, image, color, state, comment=None):
        # оценка состояния
        font = ImageFont.truetype("segoeui.ttf", 40)
        draw = ImageDraw.Draw(image)
        position = (10, 10)
        bbox = draw.textbbox(position, f"Состояние: {state}", font=font)
        draw.rectangle(bbox, fill=color)
        draw.text(position, f"Состояние: {state}", font=font, fill="black" if color != "black" else "white")
        # комментарий
        if comment is not None:
            font = ImageFont.truetype("segoeui.ttf", 30)
            draw = ImageDraw.Draw(image)
            position = (10, 50)
            bbox = draw.textbbox(position, comment, font=font)
            draw.rectangle(bbox, fill="black")
            draw.text(position, comment, font=font, fill="white")

    def classify_pose(self, pil_image):
        hot_pose, hot_angels = self.__pose_determinator.determinate_pose(pil_image)
        comment = ''

        if hot_pose is None and hot_angels is None:
            state = 'Не удалось найти позу'
            color = 'pink'
            img = pil_image
        else:
            state = 'Неизвестное'
            cold_pose_list = self.__app.get_poses()

            if len(cold_pose_list) > 0:
                # поиск похожих cold поз
                similar_pose_list = self.__compare_poses(hot_angels, cold_pose_list, 60)

                # проверка, если найдено несколько похожих cold поз
                if len(similar_pose_list) > 1:

                    state = self.pp(similar_pose_list)

                    for p in similar_pose_list:
                        comment += f'id позы: {(p[1].pose_id)} [{(p[0])}% / 100.0%]\n'


                elif len(similar_pose_list) == 1:
                    state = similar_pose_list[0][1].state
                    comment = f'id позы: {(similar_pose_list[0][1].pose_id)} [{(similar_pose_list[0][0])}% / 100.0%]'
            else:
                state = 'Неизвестное'
                comment = 'В базе данных\nотсутствуют позы\nдля сравнения'

            # state = similar_pose_list.get_state()

            color = self.__app.get_states()[state]
            img = self.__drawer.get_skeleton(hot_pose, pil_image, color)


        self.__modify_image(img, color, state, comment)

        return img, state, hot_angels, comment
