import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
import PIL
from PIL import ImageTk, Image
import cv2
import math
from config import *
from web_cam_module import CanvasWebCam
import numpy as np


class TkinterGUI():

    def __init__(self):
        self.is_web_cam_input = False
        self.is_detected = False
        self.filepath = None
        self.determinator = DETERMINATOR

        self.img_array = None
        self.img_h = None
        self.img_w = None

        self.window = tk.Tk()
        self.window.title("Детектирование эмоционального состояния человека")
        self.window.geometry(str(WINDOW_HEIGHT)+"x"+str(WINDOW_WIDTH))
        self.window.resizable(0,0)

        self.label_path_to_file = tk.Label(text="Путь к файлу")
        self.label_preview = tk.Label(text="Предпросмотр")
        self.entry_path_to_file = tk.Entry(justify="left", width=70, state="readonly")

        self.bt_select = tk.Button(text="Выбрать", command=self.open_file)
        self.bt_switch_to_web_cam = tk.Button(text="Включить захват с камеры", command=self.switch_to_web_cam)
        self.bt_activate = tk.Button(text="Выполнить", command=self.detect)
        self.bt_save = tk.Button(text="Сохранить")

        self.canvas = tk.Canvas(self.window, width=IMG_WINDOW_WIDTH, height=IMG_WINDOW_HEIGHT)
        self.canvas.create_rectangle(0, 0, IMG_WINDOW_WIDTH, IMG_WINDOW_HEIGHT, fill='black')

        self.pack_and_place()

        self.canvas_web_cam = CanvasWebCam(self.window, self.canvas, 0)

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

    def resize(self, img):
        img_height = IMG_WINDOW_HEIGHT
        img_width = IMG_WINDOW_WIDTH
        h, w = img.shape[:2]
        if h < w:
            h = math.floor(h / (w / img_width))
            w = img_width
            img = cv2.resize(img, (w, h))
        else:
            w = math.floor(w / (h / img_height))
            h = img_height
            img = cv2.resize(img, (w, h))
        return h, w, img

    def open_file(self):
        self.is_detected = False
        filepath = askopenfilename()
        if filepath != "":
            file = open(filepath, "rb").read()
            img = np.frombuffer(file, dtype=np.uint8)
            self.update_filepath(filepath)
            self.load_img(img)
        else:
            self.update_filepath(None)
            self.load_img(None)

    def load_img(self, img):
        if img is not None:
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.img_h, self.img_w, self.img_array = self.resize(img)
            self.update_img_window(self.img_array)
        else:
            self.update_img_window(None)

    def update_img_window(self, img_array):
        if img_array is not None:
            self.pil_img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(img_array))
            self.canvas.create_image(IMG_WINDOW_WIDTH/2, IMG_WINDOW_HEIGHT/2, anchor=CENTER, image=self.pil_img)
        else:
            self.canvas.create_rectangle(0, 0, IMG_WINDOW_WIDTH, IMG_WINDOW_HEIGHT, fill='black')

    def switch_to_web_cam(self):
        if self.is_web_cam_input == True:
            self.is_web_cam_input = False
            self.canvas_web_cam.start_video_capture(False)
            self.bt_switch_to_web_cam.config(text="Включить захват с камеры")
            self.update_filepath(None)
            self.load_img(None)
        else:
            self.is_web_cam_input = True
            self.canvas_web_cam.start_video_capture(True)
            self.update_filepath("-------- Идет трансляция с веб-камеры --------")
            self.bt_switch_to_web_cam.config(text="Отключить захват с камеры")

    def detect(self):
        if self.img_array is not None:
            if not self.is_detected:
                # self.detected_img_array = self.detector.detect_hands(self.img_array)
                # self.detected_img_array = self.detector.detect_pose(self.detected_img_array)
                self.detected_img_array = self.determinator.classify_pose(self.img_array)
                self.update_img_window(self.detected_img_array)
                self.is_detected = True
            else:
                self.update_img_window(self.img_array)
                self.is_detected = False

    def run(self):
        self.window.mainloop()


TkinterGUI().run()
