from waffle_utils.dataset import Dataset
from waffle_utils.dataset.format import Format

ds = Dataset.from_coco(
    "mnist_detection",
    coco_file="mnist_dataset/coco.json",
    coco_root_dir="mnist_dataset/images",
    root_dir="my_datasets",
)

ds.split_train_val(train_split_ratio=0.8)

ds.export(Format.YOLO_DETECTION)
