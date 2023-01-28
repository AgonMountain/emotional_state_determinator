import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename

import PIL
import numpy as np
from PIL import ImageTk, Image
from mediapipedetector import MediaPipeDetector
import cv2

class TkinterGUI():

    def __init__(self):
        self.is_web_cam_input = False
        self.filepath = None
        self.detector = MediaPipeDetector(True)
        self.img_array = None

        self.window = tk.Tk()
        self.window.title("Детектирование эмоционального состояния человека")
        self.window.geometry("1025x780")
        self.window.resizable(0,0)

        self.label_path_to_file = tk.Label(text="Подсказка")
        self.label_preview = tk.Label(text="Предпросмотр")
        self.entry_path_to_file = tk.Entry(justify="left", width=70, state="readonly")

        self.bt_select = tk.Button(text="Выбрать", command=self.open_file)
        self.bt_switch_to_web_cam = tk.Button(text="Включить захват с камеры",
                                         command=self.switch_to_web_cam)
        self.bt_activate = tk.Button(text="Выполнить", command=self.detect)
        self.bt_save = tk.Button(text="Сохранить")

        self.canvas = tk.Canvas(self.window, width=960, height=640)
        self.canvas.create_rectangle(0, 0, 960, 640, fill='black')

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

    def update_path_to_file(self, text):
        self.filepath = text

        self.entry_path_to_file.config(state="normal")
        self.entry_path_to_file.delete(0, 'end')
        self.entry_path_to_file.insert(0, self.filepath)
        self.entry_path_to_file.config(state="readonly")

    def update_img_window(self, array):
        self.img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(self.img_array))
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)

    def open_file(self):
        filepath = askopenfilename()

        if filepath != "":
            # self.switch_to_web_cam()
            self.update_path_to_file(filepath)

            self.img_array = self.detector.resize(cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_BGR2RGB))
            self.update_img_window(self.img_array)
        else:
            self.filepath = None

    def switch_to_web_cam(self):
        if self.is_web_cam_input == True:
            self.is_web_cam_input = False
            self.update_path_to_file("")
            self.bt_switch_to_web_cam.config(text="Включить захват с камеры")
        else:
            self.is_web_cam_input = True
            self.update_path_to_file("Идет трансляция с веб-камеры")
            self.bt_switch_to_web_cam.config(text="Отключить захват с камеры")

    def detect(self):
        if self.filepath is not None:
            self.img_array = self.detector.detect_hands(self.img_array)
            self.img_array = self.detector.detect_pose(self.img_array)

            self.update_img_window(self.img_array)

    def run(self):
        self.window.mainloop()


TkinterGUI().run()
