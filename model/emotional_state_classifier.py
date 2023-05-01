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
        if len(hot) == len(cold):
            for k in cold:
                if not (self.__compare_angel(hot[k], cold[k], cold_inaccuracy)):
                    return False
        else:
            return False

        return True

    def __compare_pose_crossings(self, hot, cold):
        if -2 <= len(hot) - len(cold) <= 2:
            e = 0
            for k in cold:
                if k not in hot and e < 2:
                    e = e + 1
                if e == 2:
                    return False
        else:
            return False
        return True

    def classify_pose(self, image):
        hot_pose, hot_angels, hot_crossings = self.__pose_determinator.determinate_pose(image)

        if hot_pose is None and hot_angels is None and hot_crossings is None:
            state ='Не удалось определить позу'
            color = 'pink'
            img = image
        else:
            state = 'Неизвестное'
            for pose in self.__app.get_poses():
                cold_angels = pose.get_pose_angels()
                cold_crossings = pose.get_pose_crossings()
                cold_angels_inaccuracy = pose.get_inaccuracy()

                if self.__compare_pose_angels(hot_angels, cold_angels, cold_angels_inaccuracy): #self.__compare_pose_crossings(hot_crossings, cold_crossings) and \
                    state = pose.get_state()

            color = self.__app.get_states()[state]
            img = self.__drawer.get_skeleton(hot_pose, image, color, color, color, color)

        font = ImageFont.truetype("segoeui.ttf", 40)
        draw = ImageDraw.Draw(image)
        position = (10, 10)
        bbox = draw.textbbox(position, state, font=font)
        draw.rectangle(bbox, fill=color)

        if color != "black":
            draw.text(position, state, font=font, fill="black")
        else:
            draw.text(position, state, font=font, fill="white")

        return img, state, {"angels": hot_angels, "crossings": hot_crossings}
