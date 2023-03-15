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
        segmentation: list[float] = None,
        area: float = None,
        keypoints: list[float] = None,
        num_keypoints: int = None,
        caption: str = None,
        value: float = None,
        #
        iscrowd: int = None,
    ):

        self.ann_id = ann_id
        self.img_id = img_id
        self.cat_id = cat_id
        self.bbox = bbox
        self.segmentation = segmentation
        self.area = area
        self.keypoints = keypoints
        self.num_keypoints = num_keypoints
        self.caption = caption
        self.value = value
        self.iscrowd = iscrowd

    # properties
    @property
    def ann_id(self):
        return self.__ann_id

    @ann_id.setter
    @type_validator(int)
    def ann_id(self, v):
        if v is None:
            raise ValueError("ann_id should not be None")
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self.__ann_id = v

    @property
    def img_id(self):
        return self.__img_id

    @img_id.setter
    @type_validator(int)
    def img_id(self, v):
        if v is None:
            raise ValueError("img_id should not be None")
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self.__img_id = v

    @property
    def cat_id(self):
        return self.__cat_id

    @cat_id.setter
    @type_validator(int)
    def cat_id(self, v):
        if v is None:
            raise ValueError("cat_id should not be None")
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self.__cat_id = v

    @property
    def bbox(self):
        return self.__bbox

    @bbox.setter
    @type_validator(list)
    def bbox(self, v):
        if v and len(v) != 4:
            raise ValueError("the length of bbox should be 4.")
        self.__bbox = v

    @property
    def segmentation(self):
        return self.__segmentation

    @segmentation.setter
    @type_validator(list)
    def segmentation(self, v):
        if v and len(v) % 2 != 0 and len(v) < 6:
            raise ValueError(
                "the length of segmentation should be at least 6 and divisible by 2."
            )
        self.__segmentation = v

    @property
    def area(self):
        return self.__area

    @area.setter
    @type_validator(float, strict=False)
    def area(self, v):
        self.__area = v

    @property
    def keypoints(self):
        return self.__keypoints

    @keypoints.setter
    @type_validator(list)
    def keypoints(self, v):
        if v and len(v) % 3 != 0 and len(v) < 2:
            raise ValueError(
                "the length of keypoints should be at least 2 and divisible by 3."
            )
        self.__keypoints = v

    @property
    def num_keypoints(self):
        return self.__num_keypoints

    @num_keypoints.setter
    @type_validator(int)
    def num_keypoints(self, v):
        self.__num_keypoints = v

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    @type_validator(str)
    def caption(self, v):
        self.__caption = v

    @property
    def value(self):
        return self.__value

    @value.setter
    @type_validator(float)
    def value(self, v):
        self.__value = v

    @property
    def iscrowd(self):
        return self.__iscrowd

    @iscrowd.setter
    @type_validator(int)
    def iscrowd(self, v):
        self.__iscrowd = v

    # factories
    @classmethod
    def new(
        cls,
        ann_id: int,
        img_id: int,
        cat_id: int = None,
        bbox: list[float] = None,
        segmentation: list[float] = None,
        area: int = None,
        keypoints: list[float] = None,
        num_keypoints: int = None,
        caption: str = None,
        value: float = None,
        iscrowd: int = None,
    ) -> "Annotation":
        """Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            segmentation (list[float]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): bbox area.
            keypoints (list[float]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            num_keypoints: number of labeled keypoints
            caption (str): string.
            value (float): regression value.
            iscrowd (int, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id=ann_id,
            img_id=img_id,
            cat_id=cat_id,
            bbox=bbox,
            segmentation=segmentation,
            area=area,
            keypoints=keypoints,
            num_keypoints=num_keypoints,
            caption=caption,
            value=value,
            iscrowd=iscrowd,
        )

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
        bbox: list[float],
        area: int,
        iscrowd: int = False,
    ) -> "Annotation":
        """Object Detection Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            area (int): bbox area.
            iscrowd (int, optional): is crowd or not. Default to False.

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
        bbox: list[float],
        segmentation: list[float],
        area: int,
        iscrowd: int = 0,
    ) -> "Annotation":
        """Segmentation Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            segmentation (list[float]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): segmentation segmentation area.
            iscrowd (int, optional): is crowd or not. Default to 0.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            img_id,
            cat_id=cat_id,
            bbox=bbox,
            segmentation=segmentation,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def keypoint_detection(
        cls,
        ann_id: int,
        img_id: int,
        cat_id: int,
        bbox: list[float],
        keypoints: list[float],
        num_keypoints: int,
        area: int,
        segmentation: list[float] = None,
        iscrowd: int = False,
    ) -> "Annotation":
        """Keypoint Detection Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            img_id (int): image id. natural number.
            cat_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            keypoints (list[float]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            num_keypoints: number of labeled keypoints
            area (int): segmentation segmentation or bbox area.
            segmentation (list[float], optional): [x1, y1, x2, y2, x3, y3, ...].
            iscrowd (int, optional): is crowd or not. Default to 0.

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
            segmentation=segmentation,
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

        ann = {"ann_id": self.ann_id, "image_id": self.img_id}

        if self.cat_id is not None:
            ann["category_id"] = self.cat_id
        if self.bbox is not None:
            ann["bbox"] = self.bbox
        if self.segmentation is not None:
            ann["segmentation"] = self.segmentation
        if self.area is not None:
            ann["area"] = self.area
        if self.keypoints is not None:
            ann["keypoints"] = self.keypoints
        if self.caption is not None:
            ann["caption"] = self.caption
        if self.value is not None:
            ann["value"] = self.value
        if self.iscrowd is not None:
            ann["iscrowd"] = self.iscrowd

        return ann
