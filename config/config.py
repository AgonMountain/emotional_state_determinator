import os

WINDOW_HEIGHT = 780
WINDOW_WIDTH = 1025

PLAYER_HEIGHT = 640
PLAYER_WIDTH = 960

openpose_folder = os.path.abspath("../openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/")
openpose_demo = os.path.abspath("../openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/bin/OpenPoseDemo.exe")
openpose_img_input = os.path.abspath(r"../openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__input/")
openpose_img_out = os.path.abspath(r"../openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__output/img/")
openpose_json_out = os.path.abspath(r"../openpose/openpose-1.6.0-binaries-win64-gpu-flir-3d/openpose/__output/json/")

poses_json_file_path = os.path.abspath("./config/poses.json")
