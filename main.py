import pathlib
import datetime
from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfile

from view.main_gui import MainGUI
from model.pose_manager import PoseManager
from model.mediapipe_detector_v2 import MediapipeDetector
from model.openpose_detector import OpenPoseDetector
from model.emotional_state_classifier import EmotionalStateClassifier
from model.pose_determinator import PoseDeterminator

from config.config import STATES, poses_json_file_path


class App:

    def __init__(self):
        self.__states = STATES
        self.__file_path = None
        self.__img = None

        self.__pose_detector_main = MediapipeDetector()
        self.__pose_detector_additional = OpenPoseDetector()
        self.__pose_determinator = PoseDeterminator(self.__pose_detector_main, self.__pose_detector_additional)
        self.__emotional_state_classifier = EmotionalStateClassifier(self, self.__pose_determinator)
        self.__pose_manager = PoseManager(poses_json_file_path)
        self.__gui = MainGUI(self)

    def date_time(self):
        return '{date:%d_%m_%Y_%H_%M_%S}'.format(date=datetime.datetime.now())

    def open_file(self):
        self.__file_path = askopenfilename(filetypes=(("Изображение", "*.jpg *.jpeg *.png *.webp"),))
        self.__img = None

        if self.__file_path != "":
            suf = pathlib.Path(self.__file_path).suffix.lower()
            self.__img = Image.open(self.__file_path)

        return self.__file_path, self.__img.copy() if self.__img is not None else None

    def save_file(self, image):
        file = asksaveasfile(mode='w', defaultextension=".png", filetypes=[("png", ".png"), ("jpg", ".jpg")],
                             initialfile='Снимок_' + self.date_time())
        if file:
            Image.fromarray(image).save(file.name)

    def set_high_quality_mode(self, b):
        self.__pose_determinator.set_high_quality_mode(b)

    def classify_pose(self, image):
        return self.__emotional_state_classifier.classify_pose(image.copy())

    def get_img(self):
        return self.__img.copy() if self.__img is not None else None

    def get_poses(self):
        id_list = self.__pose_manager.get_all_id()
        poses = [self.__pose_manager.get_pose(id) for id in id_list]
        return poses

    def get_pose_name_list(self):
        id_list = self.__pose_manager.get_all_id()
        poses = [self.__pose_manager.get_pose(id) for id in id_list]
        return [pose.id for pose in poses]

    def get_pose(self, pose_id):
        return self.__pose_manager.get_pose_image(pose_id), self.__pose_manager.get_pose(pose_id)

    def get_states(self):
        return list(self.__states.keys())

    def create_pose(self, image, state, pose_angels, kp_distances, pose_crossings, pose_description):
        self.__pose_manager.create_pose(image, state, pose_angels, kp_distances, pose_crossings, pose_description)

    def start(self):
        self.__gui.run()


app = App()
app.start()
