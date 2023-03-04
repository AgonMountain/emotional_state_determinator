from view.gui_tkinter import TkinterGUI
from model.mediapipe_detector import MediaPipeDetector
from model.emotional_state_classifier import EmotionalStateClassifier
from controller.load_file import *
from model.pose_determinator import PoseDeterminator
from config.config import poses_json_file_path as pjs

import pathlib
from tkinter.filedialog import askopenfilename



VIDEO_SUFFIX = ['.mp4', '.avi']
IMG_SUFFIX = ['.png', '.jpg', '.jpeg', '.webp']


class App():

    def __init__(self):
        self.gui = TkinterGUI(self)
        self.img = None

        self.detector = MediaPipeDetector(static_image_mode=True)
        self.determinator = PoseDeterminator(self.detector)
        self.classifier = EmotionalStateClassifier(self.determinator, pjs)

        self.file_path = None


    def __get_file_path(self):
        file_path = askopenfilename()
        file_format = None
        self.img = None

        if file_path != "":

            suf = pathlib.Path(file_path).suffix.lower()
            if suf in VIDEO_SUFFIX:
                file_format = 'video'
            elif suf in IMG_SUFFIX:
                file_format = 'img'
                file = open(file_path, "rb").read()
                self.img = np.frombuffer(file, dtype=np.uint8)
            else:
                file_format = None

        return file_path, file_format

    def open_file(self):
        file_path, file_format = self.__get_file_path()
        return file_path, file_format

    def get_img(self):
        return self.img

    def classify_pose(self, img_array):
        return self.classifier.classify_pose(img_array)

    def start(self):
        self.gui.run()


app = App()
app.start()