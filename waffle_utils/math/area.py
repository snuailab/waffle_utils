import cv2
import numpy as np


def get_mask_area(mask: np.ndarray):
    binary_mask = np.array(mask > 0, dtype=np.uint8)
    area = cv2.countNonZero(binary_mask)

    return area


def get_mask(seg: np.ndarray):
    np.zeros()


def min_bbox(seg: np.ndarray):
    pass
