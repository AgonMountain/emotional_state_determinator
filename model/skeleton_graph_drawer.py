from PIL import Image, ImageDraw
from pose_determinator import PoseDeterminator
from mediapipe_detector_v2 import MediapipeDetector
from openpose_detector import OpenPoseDetector

class Drawer:

    def __init__(self):
        self.img = None

    def __load(self, image_path):
        self.img = Image.open(image_path)

    def __save(self, output_path):
        self.img.save(output_path)

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

    def __draw_body(self, b, body_color="white", left_hand_color="white", right_hand_color="white"):
        # simple face
        cartage = self.__to_cortege(b['right_ear'], b['right_eye'], b['nose'], b['left_eye'], b['left_ear'])
        self.__line(cartage, internal_fill=body_color)
        self.__ellipse(cartage, internal_fill=body_color)

        # in openpose doesnt exist
        if 'left_mouth' in b and 'right_mouth' in b:
            cartage = self.__to_cortege(b['left_mouth'], b['right_mouth'])
            self.__line(cartage, internal_fill=body_color)
            self.__ellipse(cartage, internal_fill=body_color)

        # body
        cartage = self.__to_cortege(b['left_ankle'], b['left_knee'], b['left_hip'], b['left_shoulder'],
                            b['right_shoulder'], b['right_hip'], b['right_knee'], b['right_ankle'])
        self.__line(cartage, internal_fill=body_color)
        self.__ellipse(cartage, internal_fill=body_color)

        # left hand
        cartage = self.__to_cortege(b['left_shoulder'], b['left_elbow'], b['left_wrist'])
        self.__line(cartage, internal_fill=left_hand_color)
        self.__ellipse(cartage, internal_fill=left_hand_color)

        # right hand
        cartage = self.__to_cortege(b['right_shoulder'], b['right_elbow'], b['right_wrist'])
        self.__line(cartage, internal_fill=right_hand_color)
        self.__ellipse(cartage, internal_fill=right_hand_color)

    def __draw_hands(self, h, color="white"):
        fingers = ['index', 'middle', 'ring', 'pinky']

        cartage = self.__to_cortege(h['wrist'], h['thumb_finger_cmc'], h['thumb_finger_mcp'],
                                      h['thumb_finger_ip'], h['thumb_finger_tip'])
        self.__line(cartage, internal_fill=color)
        self.__ellipse(cartage, internal_fill=color)

        for f in fingers:
            cartage = self.__to_cortege(h['wrist'], h[f + '_finger_mcp'], h[f + '_finger_pip'],
                                          h[f + '_finger_dip'], h[f + '_finger_tip'])
            self.__line(cartage, internal_fill=color)
            self.__ellipse(cartage, internal_fill=color)


    def get_skeleton(self, c, image_path, output_path):
        self.__load(image_path)

        if 'body' in c:
            self.__draw_body(c['body'], body_color="green", left_hand_color="blue", right_hand_color="red")

        if 'left_hand' in c:
            self.__draw_hands(c['left_hand'], color="blue")

        if 'right_hand' in c:
            self.__draw_hands(c['right_hand'], color="red")

        self.__save(output_path)


if __name__ == "__main__":
    d = MediapipeDetector()
    p = PoseDeterminator(d)
    pose = d.detect("2.jpg")

    b = pose['body']
    dr = Drawer()
    dr.get_skeleton(pose, '2.jpg', '10.jpg')