import math
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import imutils

class WebCamPlayer:

    def __init__(self, app, window, canvas, video_source=0):
        self.app = app
        self.window = window
        self.canvas = canvas
        self.video_source = video_source
        self.vid = None
        self.is_detected = False
        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.is_start_video_capture = False

    # def snapshot(self):
    #     # Get a frame from the video source
    #     ret, frame = self.vid.get_frame()
    #
    #     if ret:
    #         cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def __resize_img(self, img):
        return cv2.resize(img, (640, 480))

    def start_video_capture(self, start):
        self.is_start_video_capture = start
        if start:
            self.vid = MyVideoCapture(self.video_source)
            self.__update_frame()
        else:
            self.vid.__del__()

    def set_detected(self, is_detected):
        self.is_detected = is_detected

    def __update_frame(self):
        if self.is_start_video_capture:
            ret, frame = self.vid.get_frame()

            if self.is_detected:
                detected_img_array = self.app.classify_pose(self.__resize_img(frame))
                frame = detected_img_array

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

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
