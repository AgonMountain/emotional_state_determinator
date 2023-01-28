import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

import mediapipedetector as det

import mediapipe as mp



class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3)
        self.mp_pose_drawing = mp.solutions.drawing_utils

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.6)
        self.mp_hands_drawing = mp.solutions.drawing_utils

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()

            pose_video = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7)
            hands_video = self.mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.6, max_num_hands=2)
            # Perform Pose landmark detection.

            frame = det.detectHands(frame, hands_video, self.mp_hands, self.mp_hands_drawing)
            frame, landmarks = det.detectPose(frame, pose_video, self.mp_pose, self.mp_pose_drawing)

            # Check if the landmarks are detected.
            if landmarks:
                # Perform the Pose Classification.
                frame, _ = det.classifyPose(self.mp_pose, landmarks, frame)

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")