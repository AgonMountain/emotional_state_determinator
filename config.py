from mediapipe_detector import MediaPipeDetector
from emotional_state_determinator import EmotionalStateDeterminator

WINDOW_HEIGHT = 1025
WINDOW_WIDTH = 780

IMG_WINDOW_HEIGHT = 640
IMG_WINDOW_WIDTH = 960

DETECTOR = MediaPipeDetector(True)
DETERMINATOR = EmotionalStateDeterminator(DETECTOR)


IMAGE_TYPES = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")