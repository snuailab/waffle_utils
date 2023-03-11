import cv2

# Image configurations
DEFAULT_IMAGE_EXTENSION = "jpg"
SUPPORTED_IMAGE_EXTENSION = ["jpg", "jpeg", "png", "bmp", "tif", "tiff"]

# Video configurations
DEFAULT_FRAME_RATE = 30
SUPPORTED_VIDEO_EXTENSION = ["mp4", "avi", "wmv", "mov", "flv", "mkv", "mpeg"]
FOURCC_MAP = {
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
    "avi": cv2.VideoWriter_fourcc(*"xvid")
    if cv2.VideoWriter_fourcc(*"xvid") == -1
    else cv2.VideoWriter_fourcc(*"mjpg"),
    "wmv": cv2.VideoWriter_fourcc(*"wmv2"),
    "mov": cv2.VideoWriter_fourcc(*"xvid"),
    "flv": cv2.VideoWriter_fourcc(*"flv1"),
    "mkv": cv2.VideoWriter_fourcc(*"vp80"),
    "mpeg": cv2.VideoWriter_fourcc(*"xvid"),
    "mpg": cv2.VideoWriter_fourcc(*"xvid"),
}