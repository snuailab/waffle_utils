from waffle_utils.data_tools import Annotation as A


def test_create_annotations():

    bbox = [100, 100, 100, 100]
    mask = [110, 110, 130, 130, 110, 130]
    keypoints = [110, 110, 0, 130, 130, 1, 110, 130, 2]

    ann = A.classification(ann_id=1, image_id=1, category_id=1)
    print("classification sample format\n", ann.to_dict())

    ann = A.object_detection(
        ann_id=1, image_id=1, category_id=1, bbox=bbox, area=10000
    )
    print("object_detection sample format\n", ann.to_dict())

    ann = A.segmentation(
        ann_id=1, image_id=1, category_id=1, bbox=bbox, mask=mask, area=200
    )
    print("segmentation sample format\n", ann.to_dict())

    ann = A.keypoint_detection(
        ann_id=1,
        image_id=1,
        category_id=1,
        bbox=bbox,
        keypoints=keypoints,
        area=200,
    )
    print("keypoint_detection sample format\n", ann.to_dict())

    ann = A.regression(ann_id=1, image_id=1, value=3.0)
    print("regression sample format\n", ann.to_dict())

    ann = A.text_recognition(ann_id=1, image_id=1, caption="hello world")
    print("text_recognition sample format\n", ann.to_dict())
