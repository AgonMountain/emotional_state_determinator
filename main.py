from view.main_gui import TkinterGUI
from model.mediapipe_detector_v2 import MediapipeDetector
from model.emotional_state_classifier import EmotionalStateClassifier
from controller.load_file import *
from model.pose_determinator import PoseDeterminator
from config.config import poses_json_file_path
from PIL import Image
import pathlib
from tkinter.filedialog import askopenfilename
from model.pose_manager import PoseManager

VIDEO_SUFFIX = ['.mp4', '.avi']
IMG_SUFFIX = ['.png', '.jpg', '.jpeg', '.webp']


class App:

    def __init__(self):
        self.__states = ['Positive', 'Neutral', 'Negative']
        self.__file_path = None
        self.__file_format = None
        self.__img = None

        self.__pose_detector = MediapipeDetector()
        self.__pose_determinator = PoseDeterminator(self.__pose_detector)
        self.__emotional_state_classifier = EmotionalStateClassifier(self, self.__pose_determinator)
        self.__pose_manager = PoseManager(poses_json_file_path)
        self.__gui = TkinterGUI(self)

    def open_file(self):
        self.__file_path = askopenfilename()
        self.__img = None

        if self.__file_path != "":
            suf = pathlib.Path(self.__file_path).suffix.lower()
            if suf in VIDEO_SUFFIX:
                self.__file_format = 'video'
            elif suf in IMG_SUFFIX:
                self.__file_format = 'img'
                # file = open(self.file_path, "rb").read()
                # self.img = np.frombuffer(file, dtype=np.uint8)
                self.__img = Image.open(self.__file_path)
            else:
                self.__file_format = None

        if self.__img is not None:
            img = self.__img.copy()
        else:
            img = None

        return self.__file_path, self.__file_format, img

    def classify_pose(self, image):
        return self.__emotional_state_classifier.classify_pose(image.copy())

    def get_img(self):
        return self.__img.copy()

    def get_poses(self):
        id_list = self.__pose_manager.get_all_id()
        poses = [self.__pose_manager.get_pose(id) for id in id_list]
        return poses

    def get_pose_names(self):
        id_list = self.__pose_manager.get_all_id()
        poses = [self.__pose_manager.get_pose(id) for id in id_list]
        return [pose.id for pose in poses]

    def get_pose(self, pose_id):
        return self.__pose_manager.get_pose_image(pose_id), self.__pose_manager.get_pose(pose_id)

    def get_states(self):
        return self.__states.copy()

    def create_pose(self, image, state, pose_angels, kp_distances, pose_crossings, pose_description):
        self.__pose_manager.create_pose(image, state, pose_angels, kp_distances, pose_crossings, pose_description)

    def start(self):
        self.__gui.run()


app = App()
app.start()
