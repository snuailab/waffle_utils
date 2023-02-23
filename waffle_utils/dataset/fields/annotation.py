from waffle_utils.file import io
from waffle_utils.utils import type_validator

from .base_field import BaseField


class Annotation(BaseField):
    def __init__(
        self,
        # required
        ann_id: int,
        img_id: int,
        # optional
        cat_id: int = None,
        bbox: list[float] = None,
        mask: list[int] = None,
        area: float = None,
        keypoints: list[float] = None,
        num_keypoints: int = None,
        caption: str = None,
        value: float = None,
        #
        iscrowd: bool = None,
    ):

        self.ann_id = self._ann_id = ann_id
        self.img_id = self._img_id = img_id
        self.cat_id = self._cat_id = cat_id
        self.bbox = self._bbox = bbox
        self.mask = self._mask = mask
        self.area = self._area = area
        self.keypoints = self._keypoints = keypoints
        self.num_keypoints = self._num_keypoints = num_keypoints
        self.caption = self._caption = caption
        self.value = self._value = value
        self.iscrowd = self._iscrowd = iscrowd

    # properties
    @property
    def ann_id(self):
        return self._ann_id

    @ann_id.setter
    @type_validator(int)
    def ann_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self._ann_id = v

    @property
    def img_id(self):
        return self._img_id

    @img_id.setter
    @type_validator(int)
    def img_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self._img_id = v

    @property
    def cat_id(self):
        return self._cat_id

    @cat_id.setter
    @type_validator(int)
    def cat_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self._cat_id = v

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    @type_validator(list)
    def bbox(self, v):
        if v and len(v) != 4:
            raise ValueError("the length of bbox should be 4.")
        self._bbox = v

    @property
    def mask(self):
        return self._mask

    @mask.setter
    @type_validator(list)
    def mask(self, v):
        if v and len(v) % 2 != 0 and len(v) < 6:
            raise ValueError(
                "the length of mask should be at least 6 and divisible by 2."
            )
        self._mask = v

    @property
    def area(self):
        return self._area

    @area.setter
    @type_validator(float, strict=False)
    def area(self, v):
        self._area = v

    @property
    def keypoints(self):
        return self._keypoints

    @keypoints.setter
    @type_validator(list)
    def keypoints(self, v):
        if v and len(v) % 3 != 0 and len(v) < 2:
            raise ValueError(
                "the length of keypoints should be at least 2 and divisible by 3."
            )
        self._keypoints = v

    @property
    def num_keypoints(self):
        return self._num_keypoints

    @num_keypoints.setter
    @type_validator(int)
    def num_keypoints(self, v):
        self._num_keypoints = v

    @property
    def caption(self):
        return self._caption

    @caption.setter
    @type_validator(str)
    def caption(self, v):
        self._caption = v

    @property
    def value(self):
        return self._value

    @value.setter
    @type_validator(float)
    def value(self, v):
        self._value = v

    @property
    def iscrowd(self):
        return self._iscrowd

    @iscrowd.setter
    @type_validator(bool)
    def iscrowd(self, v):
        self._iscrowd = v

    # factories
    @classmethod
    def new(
        cls,
        ann_id: int,
        img_id: int,
        cat_id: int = None,
        bbox: list[int] = None,
        mask: list[int] = None,
        area: int = None,
        keypoints: list[int] = None,
        num_keypoints: int = None,
        caption: str = None,
        value: float = None,
        iscrowd: bool = None,
    ) -> "Annotation":
        """Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            mask (list[int]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): bbox area.
            keypoints (list[int]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            num_keypoints: number of labeled keypoints
            caption (str): string.
            value (float): regression value.
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            img_id,
            cat_id,
            bbox,
            mask,
            area,
            keypoints,
            num_keypoints,
            caption,
            value,
            iscrowd,
        )

    @classmethod
    def from_dict(cls, d: dict) -> "Annotation":
        """Annotation Format from dictionary

        Args:
            d (dict): Annotation dictionary

        Returns:
            Annotation: Annotation class
        """

        ann_id = d.get("id", None)
        img_id = d.get("image_id", None)
        cat_id = d.get("category_id", None)
        bbox = d.get("bbox", None)
        mask = d.get("mask", None)
        area = d.get("area", None)
        keypoints = d.get("keypoints", None)
        num_keypoints = d.get("num_keypoints", None)
        caption = d.get("caption", None)
        value = d.get("value", None)
        iscrowd = bool(d.get("iscrowd", None))

        if ann_id is None:
            raise ValueError("id field missing")
        if img_id is None:
            raise ValueError("image_id field missing")

        return cls(
            ann_id,
            img_id,
            cat_id,
            bbox,
            mask,
            area,
            keypoints,
            num_keypoints,
            caption,
            value,
            iscrowd,
        )

    @classmethod
    def from_json(cls, f: str) -> "Annotation":
        """Annotation Format from json file

        Args:
            d (dict): Annotation json file

        Returns:
            Annotation: Annotation class
        """
        d: dict = io.load_json(f)
        return cls.from_dict(d)

    @classmethod
    def classification(
        cls, ann_id: int, img_id: int, cat_id: int
    ) -> "Annotation":
        """Classification Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.

        Returns:
            Annotation: annotation class
        """
        return cls(ann_id, img_id, cat_id=cat_id)

    @classmethod
    def object_detection(
        cls,
        ann_id: int,
        img_id: int,
        cat_id: int,
        bbox: list[int],
        area: int,
        iscrowd: bool = False,
    ) -> "Annotation":
        """Object Detection Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            area (int): bbox area.
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            img_id,
            cat_id=cat_id,
            bbox=bbox,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def segmentation(
        cls,
        ann_id: int,
        img_id: int,
        cat_id: int,
        bbox: list[int],
        mask: list[int],
        area: int,
        iscrowd: bool = False,
    ) -> "Annotation":
        """Segmentation Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            mask (list[int]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): segmentation mask area.
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            img_id,
            cat_id=cat_id,
            bbox=bbox,
            mask=mask,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def keypoint_detection(
        cls,
        ann_id: int,
        img_id: int,
        cat_id: int,
        bbox: list[int],
        keypoints: list[int],
        num_keypoints: int,
        area: int,
        mask: list[int] = None,
        iscrowd: bool = False,
    ) -> "Annotation":
        """Keypoint Detection Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            keypoints (list[int]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            num_keypoints: number of labeled keypoints
            area (int): segmentation mask or bbox area.
            mask (list[int], optional): [x1, y1, x2, y2, x3, y3, ...].
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            img_id,
            cat_id=cat_id,
            bbox=bbox,
            keypoints=keypoints,
            num_keypoints=num_keypoints,
            mask=mask,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def regression(
        cls, ann_id: int, img_id: int, value: float
    ) -> "Annotation":
        """Regression Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            value (float): regression value.

        Returns:
            Annotation: annotation class
        """
        return cls(ann_id, img_id, value=value)

    @classmethod
    def text_recognition(
        cls, ann_id: int, img_id: int, caption: str
    ) -> "Annotation":
        """Text Recognition Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            caption (str): string.

        Returns:
            Annotation: annotation class
        """
        return cls(ann_id, img_id, caption=caption)

    def to_dict(self) -> dict:
        """Get Dictionary of Annotation Data

        Returns:
            dict: annotation dictionary.
        """

        ann = {"id": self.ann_id, "image_id": self.img_id}

        if self.cat_id is not None:
            ann["category_id"] = self.cat_id
        if self.bbox is not None:
            ann["bbox"] = self.bbox
        if self.mask is not None:
            ann["segmentations"] = self.mask
        if self.area is not None:
            ann["area"] = self.area
        if self.keypoints is not None:
            ann["keypoints"] = self.keypoints
        if self.caption is not None:
            ann["caption"] = self.caption
        if self.value is not None:
            ann["value"] = self.value
        if self.iscrowd is not None:
            ann["iscrowd"] = self.iscrowd * 1

        return ann
