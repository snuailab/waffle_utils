import cv2
from pathlib import Path
from typing import Union, Tuple
import numpy as np


Mat = np.ndarray[int, np.dtype[np.generic]]


def create_video_capture(input_path: Union[str, Path]) -> cv2.VideoCapture:

    return cv2.VideoCapture(str(input_path))


def save_image(output_path: Union[str, Path], image: Mat) -> None:

    cv2.imwrite(str(output_path), image)


def load_image(input_path: Union[str, Path]) -> Mat:

    return cv2.imread(str(input_path))


def create_video_writer(
    output_path: Union[str, Path],
    fourcc: int,
    fps: float,
    frame_size: Tuple[int, int],
) -> cv2.VideoWriter:

    return cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)
