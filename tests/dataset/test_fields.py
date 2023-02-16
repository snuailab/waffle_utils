from waffle_utils.dataset.fields import Annotation as A
from waffle_utils.dataset.fields import Category as C
from waffle_utils.dataset.fields import Image as I


def test_annotations():

    bbox = [100, 100, 100, 100]
    mask = [110, 110, 130, 130, 110, 130]
    keypoints = [0, 0, 0, 130, 130, 1, 110, 130, 2]

    ann = A.classification(ann_id=1, img_id=1, cat_id=1)
    A.from_dict(ann.to_dict())

    ann = A.object_detection(
        ann_id=1, img_id=1, cat_id=1, bbox=bbox, area=10000
    )
    A.from_dict(ann.to_dict())

    ann = A.segmentation(
        ann_id=1, img_id=1, cat_id=1, bbox=bbox, mask=mask, area=200
    )
    A.from_dict(ann.to_dict())

    ann = A.keypoint_detection(
        ann_id=1,
        img_id=1,
        cat_id=1,
        bbox=bbox,
        keypoints=keypoints,
        num_keypoints=2,
        area=200,
    )
    A.from_dict(ann.to_dict())

    ann = A.regression(ann_id=1, img_id=1, value=3.0)
    A.from_dict(ann.to_dict())

    ann = A.text_recognition(ann_id=1, img_id=1, caption="hello world")
    A.from_dict(ann.to_dict())


def test_images():

    img = I.new(img_id=1, file_name="a.png", width=100, height=100)
    I.from_dict(img.to_dict())

    img = I.new(
        img_id=1,
        file_name="a.png",
        width=100,
        height=100,
        date_captured="2020-09-26 18:00:00",
    )
    I.from_dict(img.to_dict())


def test_categories():
    cat = C.classification(cat_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())

    cat = C.object_detection(cat_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())

    cat = C.segmentation(cat_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())

    cat = C.keypoint_detection(
        cat_id=1,
        supercategory="animal",
        name="cat",
        keypoints=["eye", "nose", "mouse"],
        skeleton=[[1, 2], [2, 3]],
    )
    C.from_dict(cat.to_dict())

    cat = C.text_recognition(cat_id=1, supercategory="animal", name="cat")
    C.from_dict(cat.to_dict())
