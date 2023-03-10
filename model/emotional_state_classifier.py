from PIL import Image, ImageFont, ImageDraw
from model.skeleton_graph_drawer import Drawer


class EmotionalStateClassifier():

    def __init__(self, app, pose_determinator):
        self.app = app
        self.pose_determinator = pose_determinator
        self.drawer = Drawer()

    def __compare_angel(self, hot_angel, cold_angel, cold_inaccuracy):
        return cold_angel - cold_inaccuracy < hot_angel < cold_angel + cold_inaccuracy

    def __compare_distance_between_keypoints(self, hot_distances, cold_distances, cold_distances_inaccuracy):
        return cold_distances - cold_distances_inaccuracy < hot_distances < cold_distances + cold_distances_inaccuracy

    def __compare_angels(self, hot_angels, cold_angels):
        for angel_name in cold_angels:
            if not (self.__compare_angel(hot_angels[angel_name], cold_angels[angel_name][0], cold_angels[angel_name][1])):
                return False
        return True

    def __compare_crossings(self, hot, cold):
        return (cold['crossing_forearm'] == hot['crossing_forearm'] and cold['crossing_shin'] == hot['crossing_shin'] and
                cold['crossing_hip'] == hot['crossing_hip'] and cold['crossing_ship_hip'] == hot['crossing_ship_hip'])

    def __compare_distances_between_keypoints(self, hot_distances, cold_distances):
        for name in cold_distances:
            if not (self.__compare_distance_between_keypoints(hot_distances[name], cold_distances[name][0], cold_distances[name][1])):
                return False
        return True

    def classify_pose(self, image):
        hot_pose, hot_angels, hot_crossings, hot_distances = self.pose_determinator.determinate_pose(image)

        state = 'Unknown'

        for pose in self.app.get_poses():
            cold_angels = pose.pose_angels
            cold_crossings = pose.pose_crossings
            cold_distances = pose.kp_distances

            if self.__compare_crossings(hot_crossings, cold_crossings) and \
                    self.__compare_angels(hot_angels, cold_angels):
                    #self.__compare_distances_between_keypoints(hot_distances, cold_distances): TODO
                state = pose.state

        state_color = {'Negative': 'red', 'Positive': 'green', 'Neutral': 'gray', 'Unknown': 'black'}
        color = state_color[state]
        img = self.drawer.get_skeleton(hot_pose, image, color, color, color, color)

        font = ImageFont.truetype("segoeui.ttf", 40)
        draw = ImageDraw.Draw(image)
        position = (10, 10)
        bbox = draw.textbbox(position, state, font=font)
        draw.rectangle(bbox, fill=color)

        if color != "black":
            draw.text(position, state, font=font, fill="black")
        else:
            draw.text(position, state, font=font, fill="white")

        return img, state, {"angels": hot_angels, "crossings": hot_crossings, "distances": hot_distances}
