from PIL import ImageTk, Image
import PIL
import tkinter as tk
import numpy


class ImgPlayer:

    def __init__(self, app, window, img_player_height, img_player_width):

        self.img_player_height = int(img_player_height)
        self.img_player_width = int(img_player_width)
        self.img_array = None

        self.app = app

        self.frame_img_player = tk.Frame(window, height=img_player_height, width=img_player_width)
        self.label_preview = tk.Label(self.frame_img_player, text="Предпросмотр:")
        self.canvas_img_player = tk.Canvas(self.frame_img_player, width=img_player_width, height=img_player_height)
        self.canvas_img_player.create_rectangle(0, 0, img_player_width, img_player_height, fill='black')
        self.canvas_img_player.create_text((self.img_player_width / 2, self.img_player_height / 2),
                                           text="Изображение отсутствует, загрузите его с помощью кнопки \"Выбрать\"",
                                           fill="#ffffff", font=1000)

        self.__pack_and_place()

    def __pack_and_place(self):
        self.frame_img_player.place(x=0, y=0)
        self.label_preview.place(x=0, y=0)
        self.canvas_img_player.place(x=0, y=25)

    def __resize_img(self, image):
        base_width = self.img_player_width
        base_height = self.img_player_height

        width_percent = (base_width / float(image.size[0]))
        height_percent = (base_height / float(image.size[1]))

        height_size = int(float(image.size[1]) * float(width_percent))
        width_size = int(float(image.size[0]) * float(height_percent))

        if width_percent < height_percent:
            img = image.resize((base_width, height_size), Image.Resampling.LANCZOS)
        elif width_percent > height_percent:
            img = image.resize((width_size, base_height), Image.Resampling.LANCZOS)
        elif width_percent == height_percent != 1.0:
            img = image.resize((width_size, height_size), Image.Resampling.LANCZOS)
        else:
            img = image

        return numpy.array(img)

    def load_img(self, image):
        self.img_array = None
        if image is not None:
            self.img_array = self.__resize_img(image)
        self.__update_canvas(self.img_array)

    def get_img(self):
        '''

        :return: pil image
        '''
        return PIL.Image.fromarray(self.img_array)

    def __update_canvas(self, img_array):
        if img_array is not None:
            self.pil_img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(img_array))
            self.canvas_img_player.create_rectangle(0, 0, self.img_player_width, self.img_player_height, fill='black')
            self.canvas_img_player.create_image(self.img_player_width / 2, self.img_player_height / 2, anchor=tk.CENTER, image=self.pil_img)
        else:
            self.__clear_canvas_frame()

    def __clear_canvas_frame(self):
        self.canvas_img_player.create_rectangle(0, 0, self.img_player_width, self.img_player_height, fill='black')
        self.canvas_img_player.create_text((self.img_player_width / 2, self.img_player_height / 2),
                                           text="Изображение отсутствует, загрузите его с помощью кнопки \"Выбрать\"",
                                           fill="#ffffff", font=1000)
