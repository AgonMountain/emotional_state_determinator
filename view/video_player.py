import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo

from moviepy.editor import *

from config.config import *

class VideoPlayer():

    def __init__(self, window):
        # self.load_btn = tk.Button(window, text="Load", command=self.load_video)
        self.vid_player = TkinterVideo(scaled=True, keep_aspect=True, master=window)
        self.vid_player.set_size((300,300))

        # self.frame_controls = tk.Frame(window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        self.skip_minus_5sec = tk.Button(window, text="-5 сек", command=lambda: self.skip(-5))
        self.play_pause_btn = tk.Button(window, text="Старт", command=self.play_pause)
        self.skip_plus_5sec = tk.Button(window, text="+5 сек", command=lambda: self.skip(5))
        # time-line status bar
        self.start_time = tk.Label(window, text=str(datetime.timedelta(seconds=0)))
        self.progress_slider = tk.Scale(window, from_=0, to=0, orient="horizontal")
        self.end_time = tk.Label(window, text=str(datetime.timedelta(seconds=0)))

        self.vid_player.bind("<<Duration>>", self.update_duration)
        self.vid_player.bind("<<SecondChanged>>", self.update_scale)
        self.vid_player.bind("<<Ended>>", self.video_ended)
        self.progress_slider.bind("<ButtonRelease-1>", self.seek)

        self.pack_and_place()

    def pack_and_place(self):
        # self.load_btn.pack()
        self.vid_player.pack(expand=True, fill="both")
        self.play_pause_btn.pack()
        self.skip_minus_5sec.pack(side="left")
        self.start_time.pack(side="left")
        self.progress_slider.pack(side="left", fill="x", expand=True)
        self.end_time.pack(side="left")
        self.skip_plus_5sec.pack(side="left")

        # self.frame_controls.place(x=0, y=0)
        # self.skip_minus_5sec.place(x=30, y=0)
        # self.play_pause_btn.place(x=60, y=0)
        # self.skip_plus_5sec.place(x=90, y=0)
        # self.start_time.place(x=30, y=35)
        # self.progress_slider.place(x=60, y=35)
        # self.end_time.place(x=100, y=35)




    def update_duration(self, event):
        """ updates the duration after finding the duration """
        duration = self.vid_player.video_info()["duration"]
        self.end_time["text"] = str(datetime.timedelta(seconds=duration))
        self.progress_slider["to"] = duration

    def update_scale(self, event):
        """ updates the scale value """
        self.progress_slider.set(self.vid_player.current_duration())

    def load_video(self, file_path):
        """ loads the video """
        # file_path = filedialog.askopenfilename()

        if file_path:
            self.vid_player.load(file_path)

            self.progress_slider.config(to=0, from_=0)
            self.play_pause_btn["text"] = "Старт"
            self.progress_slider.set(0)

    def seek(self, event=None):
        """ used to seek a specific timeframe """
        self.vid_player.seek(int(self.progress_slider.get()))

    def skip(self, value: int):
        """ skip seconds """
        self.vid_player.seek(int(self.progress_slider.get()) + value)
        self.progress_slider.set(self.progress_slider.get() + value)

    def play_pause(self):
        """ pauses and plays """
        if self.vid_player.is_paused():
            self.vid_player.play()
            self.play_pause_btn["text"] = "Пауза"
        else:
            self.vid_player.pause()
            self.play_pause_btn["text"] = "Старт"

    def video_ended(self, event):
        """ handle video ended """
        self.progress_slider.set(self.progress_slider["to"])
        self.play_pause_btn["text"] = "Старт"
        self.progress_slider.set(0)

    def get_frame(self):
        img = self.vid_player.current_img()
        return img

    def __convert_to_30_fps(self, file_path, new_file_path):
        # TODO надо настроить права на запись новых файлов и тд
        clip = VideoFileClip(file_path)
        clip.write_videofile(new_file_path, fps=30, codec="libx264")
