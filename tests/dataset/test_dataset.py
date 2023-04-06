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


@pytest.fixture(
    params=[
        {
            "url": "https://github.com/snuailab/assets/raw/main/waffle/sample_dataset/mnist.zip",
            "format": "coco",
        },
        {
            # 'url': "https://github.com/snuailab/assets/raw/main/waffle/sample_dataset/mnist_yolo.zip",
            "url": "https://github.com/oneQuery/waffle_utils/raw/46-need-to-import-yolo-format-dataset/mnist_yolo.zip",  # HACK: temporal yolo mnist dataset
            "format": "yolo",
        },
    ]
)
def dataset(request, tmpdir: Path):
    url = request.param["url"]
    dataset_format = request.param["format"]

    dummy_zip_file = tmpdir / "mnist.zip"
    dummy_extract_dir = tmpdir / "extract"

    network.get_file_from_url(url, dummy_zip_file, create_directory=True)
    io.unzip(dummy_zip_file, dummy_extract_dir, create_directory=True)

    print(list(Path(dummy_extract_dir).glob("*")))

    if dataset_format == "coco":
        ds = Dataset.from_coco(
            "mnist",
            coco_file=dummy_extract_dir / "coco.json",
            images_dir=Path(dummy_extract_dir / "raw"),
            root_dir=tmpdir,
        )
    elif dataset_format == "yolo":
        ds = Dataset.from_yolo(
            "mnist",
            yolo_txt_dir=dummy_extract_dir / "labels",
            images_dir=Path(dummy_extract_dir / "raw"),
            root_dir=tmpdir,
        )
    else:
        raise ValueError(f"Unknown dataset format: {dataset_format}")

    return ds


def test_dataset_export_formats(dataset: Dataset):
    dataset.split(0.8)

    exported_dataset_dir = dataset.export(Format.YOLO_DETECTION)
    assert Path(exported_dataset_dir).exists()

    exported_dataset_dir = dataset.export(Format.YOLO_CLASSIFICATION)
    assert Path(exported_dataset_dir).exists()

    exported_dataset_dir = dataset.export(Format.COCO_DETECTION)
    assert Path(exported_dataset_dir).exists()

    dataset.split(0)
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
