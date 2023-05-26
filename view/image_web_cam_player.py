import math
import time
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import imutils
import numpy
from PIL import Image

from view.image_player import ImgPlayer


class WebCamPlayer:

    def __init__(self, app, window, web_cam_player_height, web_cam_player_width, video_source=0):
        self.vid = None
        self.is_detected = False
        self.is_flipped = False
        self.start_time = None
        self.end_time = None
        self.video_source = video_source
        self.app = app
        self.window = window
        self.web_cam_player_height = web_cam_player_height
        self.web_cam_player_width = web_cam_player_width

        size = 1
        self.img_player_height = web_cam_player_height * size
        self.img_player_width = web_cam_player_width * size

        self.frame_web_cam_player = tk.Frame(window, height=self.web_cam_player_height, width=self.web_cam_player_width)
        self.img_canvas = tk.Canvas(self.frame_web_cam_player, width=self.img_player_width, height=self.img_player_height)
        self.img_canvas.create_rectangle(0, 0, self.img_player_width, self.img_player_height, fill='black')
        self.bt_flip_input_from_web_cam = tk.Button(self.frame_web_cam_player, text="Отзеркалить изображение", command=self.set_flipped)
        self.bt_snapshot = tk.Button(self.frame_web_cam_player, text="Выполнить скриншот", command=self.snapshot)

        self.delay = 15
        self.is_start_video_capture = False

        self.pack_and_place()

    def pack_and_place(self):
        self.frame_web_cam_player.place(x=0, y=0)
        self.img_canvas.place(x=0, y=0)
        self.bt_flip_input_from_web_cam.place(x=self.web_cam_player_width - 200, y=self.web_cam_player_height - 100)
        self.bt_snapshot.place(x=self.web_cam_player_width - 200, y=self.web_cam_player_height - 50)

    def snapshot(self):
        # Get a frame from the video source
        # ret, frame = self.vid.get_frame()
        if self.start_time == None:
            self.start_time = time.time()

        if self.start_time != None:
            self.end_time = time.time()
            self.bt_snapshot.config(text='Скриншот через ' + str(5 -  int(self.end_time - self.start_time)) + " сек")
            if int(self.end_time - self.start_time) >= 5:
                self.bt_snapshot.config(text=("Выполнить скриншот"))
                self.start_time = None
                self.app.save_file(PIL.Image.fromarray(self.array_frame))


    def __resize_img(self, image):
        base_width = self.img_player_width
        base_height = self.img_player_height

        height_percent = (base_height / float(image.shape[0]))
        width_percent = (base_width / float(image.shape[1]))

        height_size = int(float(image.shape[0]) * float(width_percent))
        width_size = int(float(image.shape[1]) * float(height_percent))

        if width_percent < height_percent:
            img = cv2.resize(image, (base_width, height_size))
        elif width_percent > height_percent:
            img = cv2.resize(image, (width_size, base_height))
        else:
            img = image

        return numpy.array(img)

    def start_video_capture(self, start):
        if start:
            self.is_start_video_capture = start
            self.vid = MyVideoCapture(self.video_source)
            self.__update_frame()
        elif not start and self.is_start_video_capture:
            self.vid.__del__()

    def set_detected(self, is_detected):
        self.is_detected = is_detected

    def set_flipped(self):
        self.is_flipped = True if not self.is_flipped else False

    def __update_frame(self):
        if self.is_start_video_capture:
            ret, frame = self.vid.get_frame()

            frame = self.__resize_img(frame)

            if self.is_flipped:
                frame = cv2.flip(frame, 1)

            self.array_frame = frame

            if self.is_detected:
                detected_img_array, label, data = self.app.classify_pose(Image.fromarray(frame))
                frame = detected_img_array
                self.array_frame = numpy.asarray(detected_img_array)
            else:
                frame = PIL.Image.fromarray(frame)

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=frame)
                self.img_canvas.create_image(self.img_player_width / 2, self.img_player_height / 2, image=self.photo, anchor=tk.CENTER)

            if self.start_time != None:
                self.snapshot()
            self.window.after(self.delay, self.__update_frame)




class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = imutils.resize(frame, width=800) # TODO
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
