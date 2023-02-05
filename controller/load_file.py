import pathlib
from tkinter.filedialog import askopenfilename

import numpy as np

VIDEO_SUFFIX = ['.mp4', '.avi']
IMG_SUFFIX = ['.png', '.jpg']


def get_file_path():
    file_path = askopenfilename()
    file_format = None

    if file_path != "":

        suf = pathlib.Path(file_path).suffix.lower()
        if suf in VIDEO_SUFFIX:
            file_format = 'video'
        elif suf in IMG_SUFFIX:
            file_format = 'img'

    return file_path, file_format

