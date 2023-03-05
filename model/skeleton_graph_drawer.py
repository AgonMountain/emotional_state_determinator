from PIL import Image, ImageDraw


class Drawer:

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

    def __draw_body(self, b):
        # simple face
        cartage = self.__to_cortege(b['right_ear'], b['right_eye'], b['nose'], b['left_eye'], b['left_ear'])
        self.__line(cartage, internal_fill=self.body_color)
        self.__ellipse(cartage, internal_fill=self.body_color)

        # in openpose doesnt exist
        if 'left_mouth' in b and 'right_mouth' in b:
            cartage = self.__to_cortege(b['left_mouth'], b['right_mouth'])
            self.__line(cartage, internal_fill=self.body_color)
            self.__ellipse(cartage, internal_fill=self.body_color)

        # body
        cartage = self.__to_cortege(b['left_ankle'], b['left_knee'], b['left_hip'], b['left_shoulder'],
                            b['right_shoulder'], b['right_hip'], b['right_knee'], b['right_ankle'])
        self.__line(cartage, internal_fill=self.body_color)
        self.__line(self.__to_cortege(b['left_hip'], b['right_hip']), internal_fill=self.body_color)
        self.__ellipse(cartage, internal_fill=self.body_color)

        # left hand
        cartage = self.__to_cortege(b['left_shoulder'], b['left_elbow'], b['left_wrist'])
        self.__line(cartage, internal_fill=self.left_hand_color)
        self.__ellipse(cartage, internal_fill=self.left_hand_color)

        # right hand
        cartage = self.__to_cortege(b['right_shoulder'], b['right_elbow'], b['right_wrist'])
        self.__line(cartage, internal_fill=self.right_hand_color)
        self.__ellipse(cartage, internal_fill=self.right_hand_color)

    def __draw_hands(self, h):
        fingers = ['index', 'middle', 'ring', 'pinky']

        cartage = self.__to_cortege(h['wrist'], h['thumb_finger_cmc'], h['thumb_finger_mcp'],
                                      h['thumb_finger_ip'], h['thumb_finger_tip'])
        self.__line(cartage, internal_fill=self.hands_color)
        self.__ellipse(cartage, internal_fill=self.hands_color)

        for f in fingers:
            cartage = self.__to_cortege(h['wrist'], h[f + '_finger_mcp'], h[f + '_finger_pip'],
                                          h[f + '_finger_dip'], h[f + '_finger_tip'])
            self.__line(cartage, internal_fill=self.hands_color)
            self.__ellipse(cartage, internal_fill=self.hands_color)

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
