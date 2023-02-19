from waffle_utils.dataset import Dataset
from waffle_utils.dataset.format import Format

ds = Dataset.from_coco(
    "mnist_detection",
    coco_file="/tmp/data/mnist_dataset/coco.json",
    coco_root_dir="/tmp/data/mnist_dataset/images",
    root_dir="my_datasets",
)

ds.split_train_val(train_split_ratio=0.8)

ds.export(Format.YOLO_DETECTION)
ds.export(Format.YOLO_CLASSIFICATION)

# yolo detect train model=yolov8n.pt data=/home/snu/ws/waffle_utils/my_datasets/mnist_detection/exports/YOLO_DETECTION/data.yaml epochs=20 batch=4 imgsz=256
# yolo classify train model=yolov8n-cls.pt data=/home/snu/ws/waffle_utils/my_datasets/mnist_detection/exports/YOLO_CLASSIFICATION/data.yaml epochs=50 batch=8 imgsz=28
