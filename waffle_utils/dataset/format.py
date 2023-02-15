import enum


# enums
class Format(enum.Flag):
    YOLO_CLASSIFICATION = enum.auto()
    YOLO_DETECTION = enum.auto()
    YOLO_SEGMENTATION = enum.auto()

    COCO_DETECTION = enum.auto()
