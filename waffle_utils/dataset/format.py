import enum

import cv2
import numpy as np


# enums
class Format(enum.Flag):
    YOLO_CLASSIFICATION = enum.auto()
    YOLO_DETECTION = enum.auto()
    YOLO_SEGMENTATION = enum.auto()

    COCO_DETECTION = enum.auto()


def mask_to_rle(mask):
    """Convert mask to RLE.

    Args:
        mask (np.ndarray): Mask.

    Returns:
        list: RLE format.
    """
    # Run in vertical direction, so transpose first
    pixels = mask.T.flatten()

    run_length = 1
    runs = []

    # Iterate through pairs of consecutive elements
    for prev_pixel, curr_pixel in zip(pixels[:-1], pixels[1:]):
        if curr_pixel == prev_pixel:
            run_length += 1
        else:
            runs.append(run_length)
            run_length = 1

    # Append the last run_length
    runs.append(run_length)

    return runs


def polygon_to_rle(image_width, image_height, x_coords, y_coords):
    """Convert polygon to RLE.

    Args:
        image_width (int): Image width.
        image_height (int): Image height.
        x_coords (list): List of x coordinates.
        y_coords (list): List of y coordinates.

    Returns:
        list: RLE format.
    """
    # create mask
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    polygon = np.array([x_coords, y_coords]).T
    polygon_int32 = np.round(polygon).astype(np.int32)
    cv2.fillPoly(mask, [polygon_int32], 1)

    # convert mask to rle
    rle = mask_to_rle(mask)

    return rle
