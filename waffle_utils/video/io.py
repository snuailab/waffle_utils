from pathlib import Path
from typing import Union

import cv2

from waffle_utils.video import get_fourcc


def create_video_capture(
    input_path: Union[str, Path]
) -> list[cv2.VideoCapture, dict]:

    cap = cv2.VideoCapture(str(input_path))
    meta = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "width": cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        "height": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
    }

    return cap, meta


def create_video_writer(
    output_path: Union[str, Path],
    fps: float,
    frame_size: tuple[int, int],
) -> cv2.VideoWriter:

    fourcc = get_fourcc(Path(output_path).suffix[1:])
    return cv2.VideoWriter(str(output_path), fourcc, fps, frame_size)
