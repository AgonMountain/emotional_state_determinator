import os

APP_HEIGHT = 780
APP_WIDTH = 1025

PLAYER_HEIGHT = 640
PLAYER_WIDTH = 960

STATES = {'Очень положительное': 'green',
          'Положительное': 'green',
          'Нейтральное': 'gray',
          'Отрицательное': 'yellow',
          'Очень отрицательное': 'red',
          'Неизвестное': 'black'}

INACCURACY = {'Низкий': 10,
              'Средний': 15,
              'Средне-высокий': 20,
              'Высокий': 25}

POSE_DATA_JSON = os.path.abspath(r"./config/poses.json")
POSE_IMAGES_FOLDER = os.path.abspath(r"./config/pose_images/")

openpose_folder = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/")
openpose_demo = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/bin/OpenPoseDemo.exe")
openpose_img_input = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__input/")
openpose_img_out = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__output/img/")
openpose_json_out = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__output/json/")


