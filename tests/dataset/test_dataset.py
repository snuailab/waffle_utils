from pathlib import Path

import pytest

from waffle_utils.dataset import Dataset
from waffle_utils.dataset.fields import Annotation as A
from waffle_utils.dataset.fields import Category as C
from waffle_utils.dataset.fields import Image as I
from waffle_utils.dataset.format import Format
from waffle_utils.file import io, network


def test_annotations():

    bbox = [100, 100, 100, 100]
    segmentation = [110, 110, 130, 130, 110, 130]
    keypoints = [0, 0, 0, 130, 130, 1, 110, 130, 2]

    # annotation test
    ann = A.classification(annotation_id=1, image_id=1, category_id=1)
    A.from_dict(ann.to_dict())

    ann = A.object_detection(
        annotation_id=1, image_id=1, category_id=1, bbox=bbox, area=10000
    )
    A.from_dict(ann.to_dict())

    ann = A.segmentation(
        annotation_id=1,
        image_id=1,
        category_id=1,
        bbox=bbox,
        segmentation=segmentation,
        area=200,
    )
    A.from_dict(ann.to_dict())

    ann = A.keypoint_detection(
        annotation_id=1,
        image_id=1,
        category_id=1,
        bbox=bbox,
        keypoints=keypoints,
        num_keypoints=2,
        area=200,
    )
    A.from_dict(ann.to_dict())

    ann = A.regression(annotation_id=1, image_id=1, value=3.0)
    A.from_dict(ann.to_dict())

    ann = A.text_recognition(
        annotation_id=1, image_id=1, caption="hello world"
    )
    A.from_dict(ann.to_dict())

    assert not ann.is_prediction()

    # score test (for prediction)
    ann = A.classification(
        annotation_id=1, image_id=1, category_id=1, score=0.8
    )
    A.from_dict(ann.to_dict())

    ann = A.object_detection(
        annotation_id=1,
        image_id=1,
        category_id=1,
        bbox=bbox,
        area=10000,
        score=0.8,
    )
    A.from_dict(ann.to_dict())

    ann = A.segmentation(
        annotation_id=1,
        image_id=1,
        category_id=1,
        bbox=bbox,
        segmentation=segmentation,
        area=200,
        score=0.8,
    )
    A.from_dict(ann.to_dict())

    ann = A.keypoint_detection(
        annotation_id=1,
        image_id=1,
        category_id=1,
        bbox=bbox,
        keypoints=keypoints,
        num_keypoints=2,
        area=200,
        score=[0.8, 0.5],
    )
    A.from_dict(ann.to_dict())

    ann = A.text_recognition(
        annotation_id=1, image_id=1, caption="hello world", score=0.5
    )
    A.from_dict(ann.to_dict())

    assert ann.is_prediction()


def test_images():

    img = I.new(image_id=1, file_name="a.png", width=100, height=100)
    I.from_dict(img.to_dict())

    img = I.new(
        image_id=1,
        file_name="a.png",
        width=100,
        height=100,
    )
    img = I.new(
        image_id=1,
        file_name="a.png",
        width=100,
        height=100,
        date_captured="2020-09-26 18:00:00",
    )
    I.from_dict(img.to_dict())


def test_categories():
    cat = C.classification(category_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())

    cat = C.object_detection(category_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())

    cat = C.segmentation(category_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())

    cat = C.keypoint_detection(
        category_id=1,
        supercategory="animal",
        name="cat",
        keypoints=["eye", "nose", "mouse"],
        skeleton=[[1, 2], [2, 3]],
    )
    C.from_dict(cat.to_dict())

    cat = C.text_recognition(category_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())


@pytest.fixture
def dataset(tmpdir: Path):
    url = "https://github.com/snuailab/waffle_utils/raw/main/mnist.zip"

    dummy_zip_file = tmpdir / "mnist.zip"
    dummy_extract_dir = tmpdir / "extract"
    dummy_coco_root_dir = tmpdir / "extract/raw"
    dummy_coco_file = tmpdir / "extract/exports/coco.json"

    network.get_file_from_url(url, dummy_zip_file, create_directory=True)
    io.unzip(dummy_zip_file, dummy_extract_dir, create_directory=True)

    ds = Dataset.from_coco(
        "mnist",
        dummy_coco_file,
        Path(dummy_coco_root_dir),
        root_dir=tmpdir / "datasets",
    )
    ds.split_train_val(0.8)
    return ds


def test_import_coco(dataset: Dataset):

    exported_dataset_dir = dataset.export(Format.YOLO_DETECTION)
    exported_dataset_dir = dataset.export("yolo_detection")
    exported_dataset_dir = dataset.export("YOLO_DETECTION")
    assert Path(exported_dataset_dir).exists()

    exported_dataset_dir = dataset.export(Format.YOLO_CLASSIFICATION)
    exported_dataset_dir = dataset.export("yolo_classification")
    exported_dataset_dir = dataset.export("YOLO_CLASSIFICATION")
    assert Path(exported_dataset_dir).exists()

    dataset.split_train_val(train_split_ratio=0)
    exported_dataset_dir = dataset.export(Format.YOLO_DETECTION)
    assert len(list((Path(exported_dataset_dir) / "train").rglob("*"))) == 0


def test_predictions(dataset: Dataset):

    dataset.add_predictions(
        [
            A.object_detection(
                annotation_id=1,
                image_id=1,
                category_id=1,
                bbox=[1, 2, 3, 4],
                area=1,
                score=0.5,
            )
        ]
    )
    assert (dataset.prediction_dir / "1" / "1.json").exists()
