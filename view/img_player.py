import math
import cv2
import PIL


class ImgPlayer():

    def __init__(self, canvas, img_player_height, img_player_width):
        self.canvas = canvas
        self.img_player_height = img_player_height
        self.img_player_width = img_player_width

    def __resize_img(self, img):
        h, w = img.shape[:2]
        if h < w:
            h = math.floor(h / (w / self.img_player_width))
            w = self.img_player_width
            img_array = cv2.resize(img, (w, h))
        else:
            w = math.floor(w / (h / self.img_player_height))
            h = self.img_player_height
            img_array = cv2.resize(img, (w, h))
        return img_array

    def load_img(self, img):
        if img is not None:
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_array = self.__resize_img(img)
            self.update_canvas(img_array)

    def update_canvas(self, img_array):
        if img_array is not None:
            pil_img = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(img_array))
            self.canvas.create_image(self.img_player_width / 2, self.img_player_height / 2, anchor=CENTER, image=pil_img)
        else:
            self.clear_canvas_frame()

    def clear_canvas_frame(self):
        self.canvas.create_rectangle(0, 0, self.img_player_width, self.img_player_height, fill='black')
