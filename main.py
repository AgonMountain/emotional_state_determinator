from view.gui_tkinter import TkinterGUI
from model.mediapipe_detector_v2 import MediapipeDetector
from model.emotional_state_classifier import EmotionalStateClassifier
from controller.load_file import *
from model.pose_determinator import PoseDeterminator
from config.config import poses_json_file_path as pjs
from PIL import Image
import pathlib
from tkinter.filedialog import askopenfilename

VIDEO_SUFFIX = ['.mp4', '.avi']
IMG_SUFFIX = ['.png', '.jpg', '.jpeg', '.webp']


class App:

    def __init__(self):
        self.gui = TkinterGUI(self)

        self.detector = MediapipeDetector()
        self.determinator = PoseDeterminator(self.detector)
        self.classifier = EmotionalStateClassifier(self.determinator, pjs)

        self.file_path = None
        self.file_format = None
        self.img = None

    def open_file(self):
        self.file_path = askopenfilename()
        self.img = None

        if self.file_path != "":
            suf = pathlib.Path(self.file_path).suffix.lower()
            if suf in VIDEO_SUFFIX:
                self.file_format = 'video'
            elif suf in IMG_SUFFIX:
                self.file_format = 'img'
                # file = open(self.file_path, "rb").read()
                # self.img = np.frombuffer(file, dtype=np.uint8)
                self.img = Image.open(self.file_path)
            else:
                self.file_format = None

        return self.file_path, self.file_format, self.img.copy()

    def classify_pose(self):
        return self.classifier.classify_pose(self.img.copy())

    def get_img(self):
        return self.img.copy()

    def start(self):
        self.gui.run()


app = App()
app.start()