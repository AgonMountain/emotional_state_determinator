import math
import cv2
import PIL
from PIL import ImageTk, Image
import tkinter as tk

from img_player import ImgPlayer

class ConstructorPlayer(ImgPlayer):

    def __init__(self, canvas, img_player_height, img_player_width):
        super().__init__(canvas, img_player_height, img_player_width)

        self.bt_save = tk.Button(self.frame_controls, text="Сохранить", command=self.detect)
        self.bt_update = tk.Button(self.frame_controls, text="Сохранить", command=self.detect)
        self.bt_delete = tk.Button(self.frame_controls, text="Удалить", command=self.detect)

