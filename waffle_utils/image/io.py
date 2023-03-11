from pathlib import Path
from typing import Union

import cv2
import numpy as np

Mat = np.ndarray[int, np.dtype[np.generic]]


def save_image(output_path: Union[str, Path], image: Mat) -> None:

    cv2.imwrite(str(output_path), image)


def load_image(input_path: Union[str, Path]) -> Mat:

    return cv2.imread(str(input_path))
