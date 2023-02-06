import tkinter as tk

from config import *

from view.video_player import VideoPlayer
from view.img_player import ImgPlayer
from view.web_cam_player import WebCamPlayer


class TkinterGUI():

    def __init__(self, app):
        self.app = app

        self.is_web_cam_input = False
        self.is_detected = False

        self.window = tk.Tk()
        self.window.title("Детектор")
        self.window.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
        self.window.resizable(0,0)

        self.frame_file = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.label_path_to_file = tk.Label(self.frame_file, text="Путь к файлу")
        self.entry_path_to_file = tk.Entry(self.frame_file, justify="left", width=70, state="readonly")
        self.bt_select = tk.Button(self.frame_file, text="Выбрать", command=self.open_file)

        self.frame_controls = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.bt_switch_to_web_cam = tk.Button(self.frame_controls, text="Включить захват с камеры", command=self.switch_to_web_cam)
        self.bt_activate = tk.Button(self.frame_controls, text="Выполнить", command=self.detect)
        self.bt_save = tk.Button(self.frame_controls, text="Сохранить")

        self.frame_img = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.label_preview = tk.Label(self.frame_img, text="Предпросмотр")
        self.canvas = tk.Canvas(self.frame_img, width=PLAYER_WIDTH, height=PLAYER_HEIGHT)
        self.canvas.create_rectangle(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, fill='black')
        self.img_player = ImgPlayer(canvas=self.canvas, img_player_width=PLAYER_WIDTH, img_player_height=PLAYER_HEIGHT)

        self.web_cam_player = WebCamPlayer(app=app, canvas=self.canvas, window=self.window)

        self.frame_video = tk.Frame(self.window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.video_player = VideoPlayer(window=self.frame_video)

        self.pack_and_place()

    def pack_and_place(self):
        self.frame_file.place(x=0, y=0)
        self.label_path_to_file.place(x=30, y=0)
        self.entry_path_to_file.place(x=30, y=25)
        self.bt_select.place(x=630, y=25)

        self.frame_controls.place(x=0, y=60)
        self.bt_switch_to_web_cam.place(x=30, y=0)
        self.bt_activate.place(x=300, y=0)
        self.bt_save.place(x=400, y=0)

        self.frame_img.place(x=0, y=95)
        self.label_preview.place(x=30, y=0)
        self.canvas.place(x=30, y=25)


    def switch_to_video_player(self):
        self.frame_img.place_forget()
        self.frame_video.place(x=0, y=95)

    def switch_to_img_player(self):
        self.frame_video.place_forget()
        self.frame_img.place(x=0, y=95)

    def switch_to_web_cam(self):
        self.switch_to_img_player()
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
            self.switch_to_img_player()
            self.img_player.load_img(self.app.get_img())
            self.is_detected = False    # очистка с прошлого детектирования
        elif file_format == 'video':
            self.switch_to_video_player()
            self.video_player.load_video(file_path)

    def detect(self):
        if self.is_web_cam_input and not self.is_detected:
            self.web_cam_player.set_detected(True)
            self.is_detected = True
        elif self.is_web_cam_input and self.is_detected:
            self.web_cam_player.set_detected(False)
            self.is_detected = False
        elif not self.is_detected:
            img_array = self.img_player.get_img()
            detected_img_array = self.app.classify_pose(img_array)
            self.img_player.load_img(img_array=detected_img_array)
            self.is_detected = True
        else:
            self.img_player.load_img(self.app.get_img())
            self.is_detected = False

    def run(self):
        self.window.mainloop()

