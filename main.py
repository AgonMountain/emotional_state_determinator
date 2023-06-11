import pathlib
import datetime
from tkinter import messagebox

from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfile

from view.main_gui import MainGUI
from model.pose_manager import PoseManager, Pose
from model.pose_detector_mediapipe import MediaPipeHolisticDetector
from model.pose_detector_openpose import OpenPoseDetector
from model.pose_detector_movenet import MoveNetDetector
from model.emotional_state_classifier import EmotionalStateClassifier
from model.pose_determinator import PoseDeterminator

from config.config import STATES, POSE_DATA_JSON, INACCURACY


class App:

    def __init__(self):
        self.__states = STATES
        self.__inaccuracy = INACCURACY
        self.__file_path = None
        self.__original_image = None

        self.__pose_detector_main = MediaPipeHolisticDetector(0.5)
        self.__pose_detector_additional = MoveNetDetector(0.5)
        self.__pose_determinator = PoseDeterminator(self.__pose_detector_main, self.__pose_detector_additional)
        self.__emotional_state_classifier = EmotionalStateClassifier(self, self.__pose_determinator)
        self.__pose_manager = PoseManager(POSE_DATA_JSON)
        self.__gui = MainGUI(self)

    def __date_time(self):
        return '{date:%d_%m_%Y_%H_%M_%S}'.format(date=datetime.datetime.now())

    def open_file(self):
        self.__file_path = askopenfilename(filetypes=(("Изображение", "*.jpg *.jpeg *.png *.webp"),))
        self.__original_image = None

        if self.__file_path != "":
            suf = pathlib.Path(self.__file_path).suffix.lower()

            # битый файл изображения
            try:
                self.__original_image = Image.open(self.__file_path)
            except:
                messagebox.showerror("Что-то пошло не так", 'Не удается открыть выбранный файл с изображением.\n' +
                                                            'Возможно выбранный файл поврежден.\n\n' +
                                                            f'{self.__file_path}')

        return self.__file_path, self.__original_image.copy() if self.__original_image is not None else None

    def save_file(self, pil_image):
        file = asksaveasfile(mode='w', defaultextension=".png", filetypes=[("png", ".png"), ("jpg", ".jpg")],
                             initialfile='Снимок_' + self.__date_time())
        if file:
            pil_image.save(file.name)

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
        pose_image = self.__pose_manager.get_pose_image(pose_id)
        pose_data = self.__pose_manager.get_pose(pose_id)

        return pose_image, pose_data

    def get_states(self):
        # return list(self.__states.keys())
        return self.__states

    def get_inaccuracy(self):
        return self.__inaccuracy

    def create_pose(self, image, state, inaccuracy, pose_description, forcibly_execute=False):
        hot_image, hot_state, hot_angels, hot_comment = self.classify_pose(image)

        if hot_angels is None:
            return False, 'Не удалось найти позу'
        elif hot_state != 'Неизвестное' and not forcibly_execute:
            return False, hot_comment
        else:
            self.__pose_manager.create_pose(image=image,
                                            state=state,
                                            pose_angels=hot_angels,
                                            inaccuracy=inaccuracy,
                                            pose_description=pose_description)
            return True, ''

    def update_pose(self, id, image, state, inaccuracy, description, forcibly_execute=False):
        hot_image, hot_state, hot_angels, hot_comment = self.classify_pose(image)

        if hot_angels is None:
            return False, 'Не удалось найти позу'
        elif hot_state != 'Неизвестное' and not forcibly_execute:
            return False, hot_comment
        else:
            self.__pose_manager.update_pose(id=id,
                                            image=image,
                                            state=state,
                                            pose_angels=hot_angels,
                                            inaccuracy=inaccuracy,
                                            description=description)
            return True, ''

    def delete_pose(self, pose_id):
        self.__pose_manager.delete_pose(pose_id=pose_id)

    def start(self):
        self.__gui.run()


app = App()
app.start()
