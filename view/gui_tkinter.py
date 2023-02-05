import tkinter as tk

from config import *

from view.video_module import VideoPlayer
from view.img_player import ImgPlayer
from view.web_cam_module import WebCamPlayer


class TkinterGUI():

    def __init__(self, app):
        self.app = app

        self.is_web_cam_input = False
        self.is_detected = False

        self.window = tk.Tk()
        self.window.title("Название программы")
        self.window.geometry(str(WINDOW_HEIGHT)+"x"+str(WINDOW_WIDTH))
        self.window.resizable(0,0)

        self.label_path_to_file = tk.Label(text="Путь к файлу")
        self.label_preview = tk.Label(text="Предпросмотр")
        self.entry_path_to_file = tk.Entry(justify="left", width=70, state="readonly")

        self.bt_select = tk.Button(text="Выбрать", command=self.open_file)
        self.bt_switch_to_web_cam = tk.Button(text="Включить захват с камеры", command=self.switch_to_web_cam)
        self.bt_activate = tk.Button(text="Выполнить")
        self.bt_save = tk.Button(text="Сохранить")

        self.canvas = tk.Canvas(self.window, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)
        self.canvas.create_rectangle(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, fill='black')

        self.img_player = ImgPlayer(canvas=self.canvas, img_player_width=PLAYER_WIDTH, img_player_height=PLAYER_HEIGHT)
        self.web_cam_player = WebCamPlayer(canvas=self.canvas, window=self.window)

        self.pack_and_place()

    def pack_and_place(self):
        self.label_path_to_file.place(x=30, y=0)
        self.entry_path_to_file.place(x=30, y=25)
        self.bt_select.place(x=630, y=25)
        self.bt_switch_to_web_cam.place(x=30, y=50)
        self.bt_activate.place(x=300, y=50)
        self.bt_save.place(x=400, y=50)
        self.label_preview.place(x=30, y=85)
        self.canvas.place(x=30, y=110)

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

        file_path, file_format = self.app.open_file()
        self.update_filepath(file_path)
        if file_format == 'img' or file_format is None:
            self.img_player.load_img(self.app.get_img())

    def switch_to_web_cam(self):
        if self.is_web_cam_input == True:
            self.is_web_cam_input = False
            self.web_cam_player.start_video_capture(False)
            self.bt_switch_to_web_cam.config(text="Включить захват с камеры")
            self.update_filepath(None)
            self.img_player.load_img(None)
        else:
            self.img_player.load_img(None)  # очистка от картинок, перед разверткой видео с камеры
            self.is_web_cam_input = True
            self.web_cam_player.start_video_capture(True)
            self.update_filepath("-------- Идет трансляция с веб-камеры --------")
            self.bt_switch_to_web_cam.config(text="Отключить захват с камеры")

    # def detect(self):
    #     if self.img_array is not None:
    #         if not self.is_detected:
    #             # self.detected_img_array = self.detector.detect_hands(self.img_array)
    #             # self.detected_img_array = self.detector.detect_pose(self.detected_img_array)
    #             self.detected_img_array = self.determinator.classify_pose(self.img_array)
    #             self.update_img_window(self.detected_img_array)
    #             self.is_detected = True
    #         else:
    #             self.update_img_window(self.img_array)
    #             self.is_detected = False

    def run(self):
        self.window.mainloop()

