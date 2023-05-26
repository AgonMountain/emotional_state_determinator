import math

from PIL import Image, ImageFont, ImageDraw
from model.pose_drawer import PoseDrawer


class EmotionalStateClassifier:

    def __init__(self, app, pose_determinator):
        self.__app = app
        self.__pose_determinator = pose_determinator
        self.__drawer = PoseDrawer()

    def __compare_angel(self, hot_angel, cold_angel, cold_inaccuracy):
        return cold_angel - cold_inaccuracy < hot_angel < cold_angel + cold_inaccuracy

    def __compare_pose_angels(self, hot, cold, cold_inaccuracy):
        key_list = list(hot.keys())

        for l in key_list:
            if len(hot[l]) == len(cold[l]):
                for k in cold[l]:
                    if k in hot[l] and \
                            not (self.__compare_angel(hot[l][k], cold[l][k], cold_inaccuracy)):
                        return False
                    if k not in hot[l]:
                        return False
            else:
                return False

        return True

    def __compare_pose_crossings(self, hot, cold):
        key_list = list(hot.keys())

        for l in key_list:
            if len(hot[l]) == len(cold[l]):
                for key in hot[l]:
                    if key not in cold[l]:
                        return False
        return True

    def __check_conflict(self, hot_angels, cold_pose_list):
        # проверяем похожие позы, ищем какая из похожих поз ближе
        dict = {}
        list = []
        for cold_pose in cold_pose_list:
            cold_angels = cold_pose.get_pose_angels()
            for k in cold_angels:
                maximum = max(hot_angels[k], cold_angels[k])
                minimum = min(hot_angels[k], cold_angels[k])
                list.append(maximum - minimum)

            key = sum(list) / len(list)
            if key not in dict:
                dict.setdefault(key, [])
            dict[key].append(cold_pose)
            list.clear()

        # return [element] or [element, element, ...]
        return dict[min(list(dict.keys()))]


    def __compare_poses(self, hot_angels, hot_crossings, cold_pose_list):
        # проверяем все позы и ищем похожие
        list = []
        for cold_pose in cold_pose_list:
            cold_angels = cold_pose.get_pose_angels()
            cold_crossings = cold_pose.get_pose_crossings()
            cold_angels_inaccuracy = cold_pose.get_inaccuracy()

            if self.__compare_pose_angels(hot_angels, cold_angels, cold_angels_inaccuracy) and \
                    self.__compare_pose_crossings(hot_crossings, cold_crossings):
                list.append(cold_pose)

        return list

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
        hot_pose, hot_angels, hot_crossings = self.__pose_determinator.determinate_pose(pil_image)

        comment = None

        if hot_pose is None and hot_angels is None and hot_crossings is None:
            state = 'Не удалось определить позу'
            color = 'pink'
            img = pil_image
        else:
            state = 'Неизвестное'
            cold_pose_list = self.__app.get_poses()

            if len(cold_pose_list) > 0:
                # поиск похожих cold поз
                similar_pose_list = self.__compare_poses(hot_angels, hot_crossings, cold_pose_list)

                # проверка, если найдено несколько похожих cold поз
                if len(similar_pose_list) > 1:
                    similar_pose_list = self.__check_conflict(hot_angels, similar_pose_list)
                    # несколько cold поз имеют одинаковую приближенность к hot позе
                    if len(similar_pose_list) > 1:
                        state = 'Ошибка'
                        comment = 'Конфликт'
                    else:
                        state = similar_pose_list[0].state
                elif len(similar_pose_list) == 1:
                    state = similar_pose_list[0].state
                    comment = f'id позы: {(similar_pose_list[0].pose_id)}'
            else:
                state = 'Ошибка'
                comment = 'Пустая база'

            # state = similar_pose_list.get_state()

            color = self.__app.get_states()[state]
            img = self.__drawer.get_skeleton(hot_pose, pil_image, color, color, color, color)


        self.__modify_image(img, color, state, comment)

        return img, state, {"angels": hot_angels, "crossings": hot_crossings}
