from view.gui_tkinter import TkinterGUI
from model.mediapipe_detector import MediaPipeDetector
from model.emotional_state_determinator import EmotionalStateDeterminator
from controller.load_file import *



import pathlib
from tkinter.filedialog import askopenfilename

from config import PLAYER_HEIGHT, PLAYER_WIDTH

VIDEO_SUFFIX = ['.mp4', '.avi']
IMG_SUFFIX = ['.png', '.jpg']


class App():

    def __init__(self):
        self.gui = TkinterGUI(self)
        self.img = None

        # self.video_player = VideoPlayer(window=self.gui.get_window())
        # self.webcam_player = WebCamPlayer(canvas=self.gui.canvas, window=self.gui.get_window())

        # self.detector = MediaPipeDetector()
        # self.determinator = EmotionalStateDeterminator()

        self.file_path = None


    def get_file_path(self):
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
        file_path, file_format = self.get_file_path()
        return file_path, file_format

    def get_img(self):
        return self.img

    def start(self):
        self.gui.run()


app = App()
app.start()