import pathlib
import datetime
from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfile

from view.main_gui import MainGUI
from model.pose_manager import PoseManager, Pose
from model.mediapipe_detector_v2 import MediaPipeDetector
from model.openpose_detector import OpenPoseDetector
from model.emotional_state_classifier import EmotionalStateClassifier
from model.pose_determinator import PoseDeterminator

from config.config import STATES, poses_json_file_path, INACCURACY


class App:

    def __init__(self):
        self.__states = STATES
        self.__inaccuracy = INACCURACY
        self.__file_path = None
        self.__original_image = None

        self.__pose_detector_main = MediaPipeDetector()
        self.__pose_detector_additional = OpenPoseDetector()
        self.__pose_determinator = PoseDeterminator(self.__pose_detector_main, self.__pose_detector_additional)
        self.__emotional_state_classifier = EmotionalStateClassifier(self, self.__pose_determinator)
        self.__pose_manager = PoseManager(poses_json_file_path)
        self.__gui = MainGUI(self)

    def __date_time(self):
        return '{date:%d_%m_%Y_%H_%M_%S}'.format(date=datetime.datetime.now())

    def open_file(self):
        self.__file_path = askopenfilename(filetypes=(("Изображение", "*.jpg *.jpeg *.png *.webp"),))
        self.__original_image = None

        if self.__file_path != "":
            suf = pathlib.Path(self.__file_path).suffix.lower()
            self.__original_image = Image.open(self.__file_path)

        return self.__file_path, self.__original_image.copy() if self.__original_image is not None else None

    def save_file(self, image):
        file = asksaveasfile(mode='w', defaultextension=".png", filetypes=[("png", ".png"), ("jpg", ".jpg")],
                             initialfile='Снимок_' + self.__date_time())
        if file:
            Image.fromarray(image).save(file.name)

    def set_high_quality_mode(self, b):
        self.__pose_determinator.set_high_quality_mode(b)

    def classify_pose(self, image):
        return self.__emotional_state_classifier.classify_pose(image.copy())

    def get_original_image(self):
        return self.__original_image.copy() if self.__original_image is not None else None

    def get_poses(self):
        id_list = self.__pose_manager.get_all_id()
        poses = [self.__pose_manager.get_pose(id) for id in id_list]
        return poses

    def get_pose(self, pose_id):
        return self.__pose_manager.get_pose_image(pose_id), self.__pose_manager.get_pose(pose_id)

    def get_states(self):
        # return list(self.__states.keys())
        return self.__states

    def get_inaccuracy(self):
        return self.__inaccuracy

    def create_pose(self, image, state, pose_angels, pose_crossings, inaccuracy, pose_description):
        self.__pose_manager.create_pose(image= image, state= state, pose_angels= pose_angels, pose_crossings= pose_crossings,
                                        inaccuracy= self.__inaccuracy[inaccuracy], pose_description= pose_description)

    def update_pose(self, pose_data, image):
        self.__pose_manager.update_pose(pose_data=pose_data, image=image)

    def delete_pose(self, pose_id):
        self.__pose_manager.delete_pose(pose_id=pose_id)

    def start(self):
        self.__gui.run()


app = App()
app.start()
