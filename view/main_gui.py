import tkinter as tk

from config.config import *

from view.video_player import VideoPlayer
from view.img_player import ImgPlayer
from view.web_cam_player import WebCamPlayer
from view.constructor_player import ConstructorPlayer

class TkinterGUI():

    def __init__(self, app):
        self.app = app

        self.is_web_cam_input = False
        self.is_classified = False
        self.active_frame = None

        self.window = tk.Tk()
        self.window.title("Определение эмоционального состояния человека по позе")
        self.window.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
        self.window.resizable(0,0)

        self.frame_file = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.label_path_to_file = tk.Label(self.frame_file, text="Путь к файлу")
        self.entry_path_to_file = tk.Entry(self.frame_file, justify="left", width=70, state="readonly")
        self.bt_select = tk.Button(self.frame_file, text="Выбрать", command=self.open_file)

        self.frame_controls = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.bt_switch_to_web_cam = tk.Button(self.frame_controls, text="Включить захват с камеры", command=self.switch_to_web_cam)
        self.bt_activate = tk.Button(self.frame_controls, text="Выполнить", command=self.classify)
        self.bt_save = tk.Button(self.frame_controls, text="Сохранить")
        self.bt_switch_to_constructor = tk.Button(self.frame_controls, text="Переключиться на конструктор",
                                                  command=self.switch_to_constructor)

        self.frame_img_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.label_preview = tk.Label(self.frame_img_player, text="Предпросмотр")
        self.canvas_img_player = tk.Canvas(self.frame_img_player, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)
        self.canvas_img_player.create_rectangle(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, fill='black')
        self.img_player = ImgPlayer(canvas=self.canvas_img_player, img_player_width=PLAYER_WIDTH, img_player_height=PLAYER_HEIGHT)

        self.frame_web_cam_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.web_cam_player = WebCamPlayer(app, self.frame_web_cam_player, PLAYER_HEIGHT, PLAYER_WIDTH)
        self.web_cam_player.set_flipped(True)

        self.frame_video_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.video_player = VideoPlayer(window=self.frame_video_player)

        self.frame_constructor_player = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.constructor_player = ConstructorPlayer(self.app,
                                                    self.frame_constructor_player,
                                                    PLAYER_HEIGHT,
                                                    PLAYER_WIDTH,
                                                    self.app.get_states(),
                                                    self.app.get_pose_names())


        self.pack_and_place()

        self.active_frame = self.frame_img_player

    def pack_and_place(self):
        self.frame_file.place(x=30, y=0)
        self.label_path_to_file.place(x=0, y=0)
        self.entry_path_to_file.place(x=0, y=25)
        self.bt_select.place(x=600, y=25)

        self.frame_controls.place(x=30, y=60)
        self.bt_switch_to_web_cam.place(x=0, y=0)
        self.bt_activate.place(x=270, y=0)
        self.bt_save.place(x=370, y=0)
        self.bt_switch_to_constructor.place(x=520, y=0)

        self.frame_img_player.place(x=30, y=95)
        self.label_preview.place(x=0, y=0)
        self.canvas_img_player.place(x=0, y=25)

    def switch_to_video_player(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_video_player
        self.active_frame.place(x=30, y=95)
        self.update_filepath("")

    def switch_to_img_player(self):
        self.active_frame.place_forget()
        self.active_frame = self.frame_img_player
        self.active_frame.place(x=30, y=95)
        self.update_filepath("")

    def switch_to_constructor(self):
        if self.active_frame != self.frame_constructor_player:
            self.active_frame.place_forget()
            self.active_frame = self.frame_constructor_player
            self.active_frame.place(x=30, y=95)
            self.bt_switch_to_constructor.config(text="Выйти из конструктора")
            self.update_filepath("")
        else:
            self.active_frame.place_forget()
            self.active_frame = self.frame_img_player
            self.active_frame.place(x=30, y=95)
            self.bt_switch_to_constructor.config(text="Переключиться на конструктор")
            self.update_filepath("")

    def switch_to_web_cam(self):
        if self.active_frame != self.frame_web_cam_player:
            self.active_frame.place_forget()
            self.active_frame = self.frame_web_cam_player
            self.active_frame.place(x=30, y=95)
            self.bt_switch_to_web_cam.config(text="Отключиться от веб-камеры")
            self.web_cam_player.start_video_capture(True)
            self.update_filepath("---------------- Идет трансляция с веб-камеры ----------------")
        else:
            self.active_frame.place_forget()
            self.active_frame = self.frame_img_player
            self.active_frame.place(x=30, y=95)
            self.bt_switch_to_web_cam.config(text="Подключиться к веб-камере")
            self.web_cam_player.start_video_capture(False)
            self.update_filepath("")

    def update_filepath(self, filepath):
        self.filepath = filepath
        self.entry_path_to_file.config(state="normal")
        self.entry_path_to_file.delete(0, 'end')
        if filepath is not None:
            self.entry_path_to_file.insert(0, self.filepath)
        else:
            self.entry_path_to_file.insert(0, '-------- Путь к файлу не указан --------')
        self.entry_path_to_file.config(state="readonly")

    def open_file(self):
        if self.is_web_cam_input:   # закрываем поток видео с камеры, перед загрузкой изображений
            self.switch_to_web_cam()

        file_path, file_format, img = self.app.open_file()
        self.update_filepath(file_path)
        if file_format == 'img' or file_format is None:
            if self.active_frame == self.frame_img_player:
                self.img_player.load_img(img)
            if self.active_frame == self.frame_constructor_player:
                self.constructor_player.load_img(img)
            self.is_classified = False    # очистка с прошлого детектирования
        elif file_format == 'video':
            self.switch_to_video_player()
            self.video_player.load_video(file_path)

    def classify(self):

        if self.is_classified:
            self.is_classified = False
            if self.active_frame != self.frame_web_cam_player:
                img = self.app.get_img()
        else:
            self.is_classified = True
            if self.active_frame != self.frame_web_cam_player:
                img, label, data = self.app.classify_pose(self.app.get_img())

        if self.active_frame == self.frame_web_cam_player:
            self.web_cam_player.set_detected(self.is_classified)
        elif self.active_frame == self.frame_img_player:
            self.img_player.load_img(img)
        elif self.active_frame == self.frame_constructor_player:
            self.constructor_player.load_img(img)
        #
        #
        # if self.is_classified:
        #     self.is_classified = False
        #
        #     if self.active_frame == self.frame_web_cam_player:
        #         if
        #             self.web_cam_player.set_detected(False)
        #     elif self.active_frame == self.frame_img_player:
        #         self.img_player.load_img(img)
        #     elif self.active_frame == self.frame_constructor_player:
        #         self.constructor_player.load_img(img)
        # else:
        #     self.is_classified = True
        #
        #     img = self.app.classify_pose(img)
        #
        #     if self.active_frame == self.frame_web_cam_player:
        #         self.web_cam_player.set_detected(True)
        #     elif self.active_frame == self.frame_img_player:
        #         self.img_player.load_img(img)
        #     elif self.active_frame == self.frame_constructor_player:
        #         self.constructor_player.load_img(img)
        #
        # if self.is_web_cam_input and not self.is_classified:
        #     self.web_cam_player.set_detected(True)
        #     self.is_classified = True
        # elif self.is_web_cam_input and self.is_classified:
        #
        # elif not self.is_classified:
        #     label, img = self.app.classify_pose()
        #     if self.active_frame == self.frame_img_player:
        #         self.img_player.load_img(img)
        #     if self.active_frame == self.frame_constructor_player:
        #         self.constructor_player.load_img(img)
        #     self.is_classified = True
        # else:
        #     self.img_player.load_img(self.app.get_img())
        #     self.is_classified = False

    def run(self):
        self.window.mainloop()

