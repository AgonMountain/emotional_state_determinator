import math
import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import imutils
import numpy
from PIL import Image

from view.img_player import ImgPlayer


class WebCamPlayer:

    def __init__(self, app, window, web_cam_player_height, web_cam_player_width, video_source=0):
        self.vid = None
        self.is_detected = False
        self.is_flipped = False

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

        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.pack_and_place()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.is_start_video_capture = False

    def pack_and_place(self):
        self.frame_web_cam_player.place(x=0, y=0)
        self.img_canvas.place(x=0, y=0)

    # def snapshot(self):
    #     # Get a frame from the video source
    #     ret, frame = self.vid.get_frame()
    #
    #     if ret:
    #         cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

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
        self.is_start_video_capture = start
        if start:
            self.vid = MyVideoCapture(self.video_source)
            self.__update_frame()
        else:
            self.vid.__del__()

    def set_detected(self, is_detected):
        self.is_detected = is_detected

    def set_flipped(self, is_flipped):
        self.is_flipped = is_flipped

    def __update_frame(self):
        if self.is_start_video_capture:
            ret, frame = self.vid.get_frame()

            frame = self.__resize_img(frame)

            if self.is_flipped:
                frame = cv2.flip(frame, 1)

            if self.is_detected:
                detected_img_array, label, data = self.app.classify_pose(Image.fromarray(frame))
                frame = detected_img_array
            else:
                frame = PIL.Image.fromarray(frame)

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=frame)
                self.img_canvas.create_image(self.img_player_width / 2, self.img_player_height / 2, image=self.photo, anchor=tk.CENTER)

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
