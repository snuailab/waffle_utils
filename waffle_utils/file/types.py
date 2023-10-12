import cv2

SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]
DEFAULT_IMAGE_EXTENSION = SUPPORTED_IMAGE_EXTENSIONS[0]

SUPPORTED_VIDEO_EXTENSION = [
    ".mp4",
    ".avi",
    ".wmv",
    ".mov",
    ".flv",
    ".mkv",
    ".mpeg",
]
DEFAULT_VIDEO_EXTENSION = SUPPORTED_VIDEO_EXTENSION[0]
FOURCC_MAP = {
    ".mp4": cv2.VideoWriter_fourcc(*"mp4v"),
    ".avi": cv2.VideoWriter_fourcc(*"xvid")
    if cv2.VideoWriter_fourcc(*"xvid") == -1
    else cv2.VideoWriter_fourcc(*"mjpg"),
    ".wmv": cv2.VideoWriter_fourcc(*"wmv2"),
    ".mov": cv2.VideoWriter_fourcc(*"xvid"),
    ".flv": cv2.VideoWriter_fourcc(*"flv1"),
    ".mkv": cv2.VideoWriter_fourcc(*"vp80"),
    ".mpeg": cv2.VideoWriter_fourcc(*"xvid"),
    ".mpg": cv2.VideoWriter_fourcc(*"xvid"),
}
