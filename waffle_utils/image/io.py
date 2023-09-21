from pathlib import Path
from typing import Union

import cv2
import numpy as np
from file.io import make_directory

Mat = np.ndarray[int, np.dtype[np.generic]]


def save_image(
    output_path: Union[str, Path], image: Mat, create_directory: bool = False
) -> None:
    output_path = Path(output_path)
    if create_directory:
        make_directory(output_path.parent)

    cv2.imwrite(str(output_path), image)


def load_image(input_path: Union[str, Path]) -> Mat:

    return cv2.imread(str(input_path))
