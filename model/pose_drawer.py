import PIL.Image
from PIL import Image, ImageDraw


class PoseDrawer:

    def __init__(self, body_color="white", left_hand_color="white", right_hand_color="white", hands_color="white"):
        self.img = None
        self.body_color = body_color
        self.left_hand_color = left_hand_color
        self.right_hand_color = right_hand_color
        self.hands_color = hands_color

    def __line(self, coordinates, width=2, internal_fill="black", external_fill="white", joint="curve"):
        draw = ImageDraw.Draw(self.img)
        draw.line(coordinates, width=width+1, fill=external_fill, joint=joint)
        draw = ImageDraw.Draw(self.img)
        draw.line(coordinates, width=width, fill=internal_fill, joint=joint)

    def __ellipse(self, c, r=2, internal_fill="black", external_fill="white"):
        draw = ImageDraw.Draw(self.img)
        for i in range(len(c)):
            if not i%2:
                draw.ellipse((c[i] - r - 1, c[i + 1] - r - 1,
                              c[i] + r + 1, c[i + 1] + r + 1), fill=external_fill)
                draw.ellipse((c[i] - r, c[i + 1] - r,
                              c[i] + r, c[i + 1] + r), fill=internal_fill)

    def __to_cortege(self, *list):
        c = ()
        for element in list:
            c = c + (element[0], element[1])
        return c

    def __draw_line(self, d, a, b):
        if a in d and b in d:
            cartage = self.__to_cortege(d[a], d[b])
            self.__line(cartage, internal_fill=self.body_color)
            self.__ellipse(cartage, internal_fill=self.body_color)

    def __draw_body(self, b):
        # body top
        self.__draw_line(b, 'left_shoulder', 'center_shoulder')
        self.__draw_line(b, 'center_shoulder', 'right_shoulder')
        self.__draw_line(b, 'left_shoulder', 'left_elbow')
        self.__draw_line(b, 'left_elbow', 'left_wrist')
        self.__draw_line(b, 'left_wrist', 'left_hand')
        self.__draw_line(b, 'right_shoulder', 'right_elbow')
        self.__draw_line(b, 'right_elbow', 'right_wrist')
        self.__draw_line(b, 'right_wrist', 'right_hand')
        self.__draw_line(b, 'left_hip', 'left_shoulder')
        self.__draw_line(b, 'right_shoulder', 'right_hip')
        # body down
        self.__draw_line(b, 'left_ankle', 'left_knee')
        self.__draw_line(b, 'left_knee', 'left_hip')
        self.__draw_line(b, 'right_hip', 'right_knee')
        self.__draw_line(b, 'right_knee', 'right_ankle')
        self.__draw_line(b, 'left_hip', 'center_hip')
        self.__draw_line(b, 'center_hip', 'right_hip')
        self.__draw_line(b, 'left_ankle', 'left_foot')
        self.__draw_line(b, 'right_ankle', 'right_foot')

    def get_skeleton(self, pose, image, body_color="white"):
        self.img = image
        self.body_color = body_color

        if pose is not None:
            self.__draw_body(pose)

        return self.img
