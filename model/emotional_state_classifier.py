from PIL import Image, ImageFont, ImageDraw
from model.pose_manager import PoseManager
from model.skeleton_graph_drawer import Drawer


class EmotionalStateClassifier():

    def __init__(self, determinator, pose_json_file_path):
        self.determinator = determinator
        self.pose_manager = PoseManager(pose_json_file_path)
        self.drawer = Drawer()
        self.pose_ids = self.pose_manager.ids()

    def __compare_crossings(self, hot, cold):
        return (cold['crossing_forearm'] == hot['crossing_forearm'] and
                cold['crossing_shin'] == hot['crossing_shin'] and
                cold['crossing_hip'] == hot['crossing_hip'] and
                cold['crossing_ship_hip'] == hot['crossing_ship_hip'])

    def __compare_angel(self, hot_angel, cold_angel, cold_inaccuracy):
        return cold_angel - cold_inaccuracy < hot_angel < cold_angel + cold_inaccuracy

    def __compare_angels(self, hot_angels, cold_angels):
        for angel_name in cold_angels:
            if not (self.__compare_angel(hot_angels[angel_name], cold_angels[angel_name][0], cold_angels[angel_name][1])):
                return False
        return True

    def __compare_distance_between_keypoints(self, hot_distances, cold_distances, cold_distances_inaccuracy):
        return cold_distances - cold_distances_inaccuracy < hot_distances < cold_distances + cold_distances_inaccuracy

    def __compare_distances_between_keypoints(self, hot_distances, cold_distances):
        for name in cold_distances:
            if not (self.__compare_distance_between_keypoints(hot_distances[name],
                                                              cold_distances[name][0],
                                                              cold_distances[name][1])):
                return False
        return True

    def classify_pose(self, image):

        kps, hot_angels, hot_crossings, hot_distances = self.determinator.determinate_pose(image)

        label = 'Unknown'

        for id in self.pose_ids:
            pose = self.pose_manager.get(id)

            cold_angels = pose.pose_angels
            cold_crossings = pose.pose_crossings
            cold_distances = pose.distances

            if self.__compare_crossings(hot_crossings, cold_crossings) and \
                    self.__compare_angels(hot_angels, cold_angels):
                    #self.__compare_distances_between_keypoints(hot_distances, cold_distances): TODO
                label = pose.label

        if label == "Negative":
            color = "red"
        elif label == "Positive":
            color = "green"
        else:
            color = "gray"

        img = self.drawer.get_skeleton(kps, image, color, color, color, color)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((40, 40), label, color, font=font)

        return label, img
