import os

# размеры окна программы
APP_HEIGHT = 780
APP_WIDTH = 1025

# размеры окна проигрывателя внутри программы
PLAYER_HEIGHT = 640
PLAYER_WIDTH = 960

# все возможные состояния и цвета для окраски свелета
STATES = {
    'Положительное': 'green',
    'Нейтральное': 'gray',
    'Отрицательное': 'red',
    'Неизвестное': 'black',
    'Ошибка': 'black'
}

# все возможные уровени точности и их числовые значения (программа оперирует - числами, пользователь - названиями)
INACCURACY = {
    'Низкий': 5,
    'Средний': 10,
    'Высокий': 15
}

# ссылки на позы и папку с картинками поз
POSE_DATA_JSON = os.path.abspath(r"./config/poses.json")
POSE_IMAGES_FOLDER = os.path.abspath(r"./config/pose_images/")

# ссылки на openpose, запускаем openpose через demo приложение
openpose_folder = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/")
openpose_demo = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/bin/OpenPoseDemo.exe")
openpose_img_input = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__input/")
openpose_img_out = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__output/img/")
openpose_json_out = os.path.abspath(r"./openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__output/json/")

movenet_model_path = os.path.abspath(r"./config/lite-model_movenet_singlepose_lightning_tflite_float16_4.tflite")
