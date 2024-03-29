import tkinter as tk
from view.image_player import ImgPlayer
from view.image_web_cam_player import WebCamPlayer
from view.pose_constructor_player import ConstructorPlayer
from view.control_player import ControlPlayer

from config.config import APP_WIDTH, APP_HEIGHT, PLAYER_HEIGHT, PLAYER_WIDTH


GUI_TITLE = "Определение эмоционального состояния человека по его позе"


class MainGUI:

    def __init__(self, app):
        self.app = app

        # main
        self.window = tk.Tk()
        self.window.title(GUI_TITLE)
        self.window.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.window.resizable(0, 0)

        # control player
        self.frame_control_player = tk.Frame(self.window, height=APP_HEIGHT, width=APP_WIDTH)
        self.control_player = ControlPlayer(self, self.frame_control_player, APP_HEIGHT, APP_WIDTH)

        # img player
        self.frame_img_player = tk.Frame(self.window, height=PLAYER_HEIGHT, width=PLAYER_WIDTH)
        self.img_player = ImgPlayer(self.app, self.frame_img_player, PLAYER_HEIGHT, PLAYER_WIDTH)

        # webcam player
        self.frame_web_cam_player = tk.Frame(self.window, height=PLAYER_HEIGHT, width=PLAYER_WIDTH)
        self.web_cam_player = WebCamPlayer(self.app, self.frame_web_cam_player, PLAYER_HEIGHT, PLAYER_WIDTH)

        # constructor player
        self.frame_constructor_player = tk.Frame(self.window, height=PLAYER_HEIGHT, width=PLAYER_WIDTH)
        self.constructor_player = ConstructorPlayer(self.app, self.frame_constructor_player, PLAYER_HEIGHT, PLAYER_WIDTH)

        self.active_frame = self.frame_img_player
        self.pack_and_place()

    def pack_and_place(self):
        self.frame_control_player.place(x=30, y=0)
        self.active_frame.place(x=30, y=100)

    def set_high_quality_mode(self, is_high_quality):
        self.app.set_high_quality_mode(is_high_quality)

    def switch_frame(self, frame_name):
        self.active_frame.place_forget()
        self.active_frame = frame_name
        self.active_frame.place(x=30, y=100)

    def switch_player(self):
        # stop webcam capture before switch to other player
        if self.active_frame == self.frame_web_cam_player:
            self.web_cam_player.start_video_capture(False)

        if self.constructor_player.is_active_editor_player():
            self.constructor_player.switch_to_table()

        # get from control panel what mode is active
        if self.control_player.is_constructor_input():
            self.switch_to_constructor_player()
        elif self.control_player.is_web_cam_input():
            self.switch_to_web_cam_player()
        elif self.control_player.is_img_input():
            self.switch_to_img_player()

    def switch_to_img_player(self):
        self.switch_frame(self.frame_img_player)
        self.img_player.load_img(self.app.get_original_image())

    def switch_to_constructor_player(self):
        self.switch_frame(self.frame_constructor_player)

    def switch_to_web_cam_player(self):
        self.switch_frame(self.frame_web_cam_player)
        self.web_cam_player.start_video_capture(True)

    def save_file(self):
        self.app.save_file(self.img_player.get_img())

    def open_file(self):
        if self.control_player.is_web_cam_input():
            self.switch_to_web_cam_player()

        file_path, img = self.app.open_file()

        if self.active_frame == self.frame_img_player:
            self.img_player.load_img(img)
        if self.active_frame == self.frame_constructor_player:
            self.constructor_player.load_img(img)

        return file_path

    def classify(self):
        # image for set classified image in player
        if self.control_player.is_classified():
            if self.active_frame != self.frame_web_cam_player:
                image, state, hot_angels, comment = self.app.classify_pose(self.app.get_original_image())

        # original image for set unclassified image in player
        elif self.active_frame != self.frame_web_cam_player:
            image = self.app.get_original_image()

        # set image
        if self.active_frame == self.frame_web_cam_player:
            self.web_cam_player.set_detected(self.control_player.is_classified())
        elif self.active_frame == self.frame_img_player:
            self.img_player.load_img(image)
        elif self.active_frame == self.frame_constructor_player:
            self.constructor_player.load_img(image)

    def run(self):
        self.window.mainloop()
