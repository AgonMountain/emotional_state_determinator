import tkinter as tk
from view.img_player import ImgPlayer
from view.web_cam_player import WebCamPlayer
from view.constructor_player import ConstructorPlayer
from view.control_player import ControlPlayer
from view.pose_table_player import PoseTablePlayer

from config.config import WINDOW_WIDTH, WINDOW_HEIGHT, PLAYER_HEIGHT, PLAYER_WIDTH


class MainGUI:

    def __init__(self, app):
        self.app = app
        self.active_frame = None

        # main
        self.window = tk.Tk()
        self.window.title("Определение эмоционального состояния человека по его позе")
        self.window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.window.resizable(0, 0)

        # control player
        self.frame_control_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.control_player = ControlPlayer(self, self.frame_control_player, WINDOW_HEIGHT, WINDOW_WIDTH)

        # img player
        self.frame_img_player = tk.Frame(self.window, height=PLAYER_HEIGHT, width=PLAYER_WIDTH)
        self.img_player = ImgPlayer(self.app, self.frame_img_player, PLAYER_HEIGHT, PLAYER_WIDTH)

        # webcam player
        self.frame_web_cam_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.web_cam_player = WebCamPlayer(self.app, self.frame_web_cam_player, PLAYER_HEIGHT, PLAYER_WIDTH)

        # constructor player
        self.frame_constructor_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.constructor_player = ConstructorPlayer(self.app, self.frame_constructor_player,
                                                    PLAYER_HEIGHT, PLAYER_WIDTH,
                                                    self.app.get_states(), self.app.get_pose_name_list())

        self.pack_and_place()

        self.active_frame = self.frame_img_player

    def pack_and_place(self):
        self.frame_control_player.place(x=30, y=0)
        self.frame_img_player.place(x=30, y=95)

    def switch_player(self):
        if self.active_frame == self.frame_web_cam_player: # stop webcam capture before switch to other player
            self.web_cam_player.start_video_capture(False)

        if self.control_player.is_constructor_input():
            self.switch_to_constructor_player()
        elif self.control_player.is_web_cam_input():
            self.switch_to_web_cam_player()
        elif self.control_player.is_img_input():
            self.switch_to_img_player()

    def switch_to_img_player(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_img_player
        self.active_frame.place(x=30, y=95)
        self.img_player.load_img(self.app.get_img())

    def switch_to_constructor_player(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_constructor_player
        self.active_frame.place(x=30, y=95)
        self.constructor_player.load_img(self.app.get_img())

    def switch_to_web_cam_player(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_web_cam_player
        self.active_frame.place(x=30, y=95)
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
        if not self.control_player.is_classified():
            if self.active_frame != self.frame_web_cam_player:
                img = self.app.get_img()
        else:
            if self.active_frame != self.frame_web_cam_player:
                img, label, data = self.app.classify_pose(self.app.get_img())

        if self.active_frame == self.frame_web_cam_player:
            self.web_cam_player.set_detected(self.control_player.is_classified())
        elif self.active_frame == self.frame_img_player:
            self.img_player.load_img(img)
        elif self.active_frame == self.frame_constructor_player:
            self.constructor_player.load_img(img)

    def run(self):
        self.window.mainloop()
