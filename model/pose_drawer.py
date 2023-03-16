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
        # simple face
        self.__draw_line(b, 'right_ear', 'right_eye')
        self.__draw_line(b, 'right_eye', 'nose')
        self.__draw_line(b, 'nose', 'left_eye')
        self.__draw_line(b, 'left_eye', 'left_ear')
        self.__draw_line(b, 'left_mouth', 'right_mouth')
        # body
        self.__draw_line(b, 'left_ankle', 'left_knee')
        self.__draw_line(b, 'left_knee', 'left_hip')
        self.__draw_line(b, 'left_hip', 'left_shoulder')
        self.__draw_line(b, 'left_shoulder', 'right_shoulder')
        self.__draw_line(b, 'right_shoulder', 'right_hip')
        self.__draw_line(b, 'right_hip', 'right_knee')
        self.__draw_line(b, 'right_knee', 'right_ankle')
        self.__draw_line(b, 'left_hip', 'right_hip')
        # left hand
        self.__draw_line(b, 'left_shoulder', 'left_elbow')
        self.__draw_line(b, 'left_elbow', 'left_wrist')
        # right hand
        self.__draw_line(b, 'right_shoulder', 'right_elbow')
        self.__draw_line(b, 'right_elbow', 'right_wrist')

    def __draw_hands(self, h):
        fingers = ['index', 'middle', 'ring', 'pinky']

        self.__draw_line(h, 'wrist', 'thumb_finger_cmc')
        self.__draw_line(h, 'thumb_finger_cmc', 'thumb_finger_mcp')
        self.__draw_line(h, 'thumb_finger_mcp', 'thumb_finger_ip')
        self.__draw_line(h, 'thumb_finger_ip', 'thumb_finger_tip')

        for f in fingers:
            self.__draw_line(h, 'wrist', f + '_finger_mcp')
            self.__draw_line(h, f + '_finger_mcp', f + '_finger_pip')
            self.__draw_line(h, f + '_finger_pip', f + '_finger_dip')
            self.__draw_line(h, f + '_finger_dip', f + '_finger_tip')

    def get_skeleton(self, pose, image, body_color="white", left_hand_color="white", right_hand_color="white", hands_color="white"):
        self.img = image

        self.body_color = body_color
        self.left_hand_color = left_hand_color
        self.right_hand_color = right_hand_color
        self.hands_color = hands_color

        if 'body' in pose:
            self.__draw_body(pose['body'])

        if 'left_hand' in pose:
            self.__draw_hands(pose['left_hand'])

        if 'right_hand' in pose:
            self.__draw_hands(pose['right_hand'])

        return self.img
