def _validate(_type: type):
    def type_check(f):
        def input_check(self, v, *args, **kwargs):
            if v is not None:
                if not isinstance(v, _type):
                    raise TypeError(f"value should be {_type}")
            return f(self, v, *args, **kwargs)

        return input_check

    return type_check


class Annotation:
    def __init__(
        self,
        # required
        ann_id: int,
        image_id: int,
        # optional
        category_id: int = None,
        bbox: list[int] = None,
        mask: list[int] = None,
        area: int = None,
        keypoints: list[int] = None,
        caption: str = None,
        value: float = None,
        #
        iscrowd: bool = None,
    ):

        self.ann_id = self._ann_id = ann_id
        self.image_id = self._image_id = image_id
        self.category_id = self._category_id = category_id
        self.bbox = self._bbox = bbox
        self.mask = self._mask = mask
        self.area = self._area = area
        self.keypoints = self._keypoints = keypoints
        self.caption = self._caption = caption
        self.value = self._value = value
        self.iscrowd = self._iscrowd = iscrowd

    # properties
    @property
    def ann_id(self):
        return self._ann_id

    @ann_id.setter
    @_validate(int)
    def ann_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self._ann_id = v

    @property
    def image_id(self):
        return self._image_id

    @image_id.setter
    @_validate(int)
    def image_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self._image_id = v

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    @_validate(int)
    def category_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self._category_id = v

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    @_validate(list)
    def bbox(self, v):
        if v and len(v) != 4:
            raise ValueError("the length of bbox should be 4.")
        self._bbox = v

    @property
    def mask(self):
        return self._mask

    @mask.setter
    @_validate(list)
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
    @_validate(int)
    def area(self, v):
        self._area = v

    @property
    def keypoints(self):
        return self._keypoints

    @keypoints.setter
    @_validate(list)
    def keypoints(self, v):
        if v and len(v) % 3 != 0 and len(v) < 2:
            raise ValueError(
                "the length of keypoints should be at least 2 and divisible by 3."
            )
        self._keypoints = v

    @property
    def caption(self):
        return self._caption

    @caption.setter
    @_validate(str)
    def caption(self, v):
        self._caption = v

    @property
    def value(self):
        return self._value

    @value.setter
    @_validate(float)
    def value(self, v):
        self._value = v

    @property
    def iscrowd(self):
        return self._iscrowd

    @iscrowd.setter
    @_validate(bool)
    def iscrowd(self, v):
        self._iscrowd = v

    # factories
    @classmethod
    def classification(
        cls, ann_id: int, image_id: int, category_id: int
    ) -> "Annotation":
        """Classification Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.

        Returns:
            Annotation: annotation class
        """
        return cls(ann_id, image_id, category_id=category_id)

    @classmethod
    def object_detection(
        cls,
        ann_id: int,
        image_id: int,
        category_id: int,
        bbox: list[int],
        area: int,
        iscrowd: bool = False,
    ) -> "Annotation":
        """Object Detection Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            area (int): bbox area.
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            image_id,
            category_id=category_id,
            bbox=bbox,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def segmentation(
        cls,
        ann_id: int,
        image_id: int,
        category_id: int,
        bbox: list[int],
        mask: list[int],
        area: int,
        iscrowd: bool = False,
    ) -> "Annotation":
        """Segmentation Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            mask (list[int]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): segmentation mask area.
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            image_id,
            category_id=category_id,
            bbox=bbox,
            mask=mask,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def keypoint_detection(
        cls,
        ann_id: int,
        image_id: int,
        category_id: int,
        bbox: list[int],
        keypoints: list[int],
        area: int,
        mask: list[int] = None,
        iscrowd: bool = False,
    ) -> "Annotation":
        """Keypoint Detection Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[int]): [x1, y1, w, h].
            keypoints (list[int]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            area (int): segmentation mask or bbox area.
            mask (list[int], optional): [x1, y1, x2, y2, x3, y3, ...].
            iscrowd (bool, optional): is crowd or not. Default to False.

        Returns:
            Annotation: annotation class
        """
        return cls(
            ann_id,
            image_id,
            category_id=category_id,
            bbox=bbox,
            keypoints=keypoints,
            mask=mask,
            area=area,
            iscrowd=iscrowd,
        )

    @classmethod
    def regression(
        cls, ann_id: int, image_id: int, value: float
    ) -> "Annotation":
        """Regression Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            value (float): regression value.

        Returns:
            Annotation: annotation class
        """
        return cls(ann_id, image_id, value=value)

    @classmethod
    def text_recognition(
        cls, ann_id: int, image_id: int, caption: str
    ) -> "Annotation":
        """Text Recognition Annotation Format

        Args:
            ann_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            caption (str): string.

        Returns:
            Annotation: annotation class
        """
        return cls(ann_id, image_id, caption=caption)

    def to_dict(self) -> dict:
        """Get Dictionary of Annotation Data

        Returns:
            dict: annotation dictionary.
        """

        ann = {"id": self.ann_id, "image_id": self.image_id}

        if self.category_id is not None:
            ann["category_id"] = self.category_id
        if self.bbox is not None:
            ann["bbox"] = self.bbox
        if self.mask is not None:
            ann["segmentations"] = self.mask
        if self.area is not None:
            ann["segmentations"] = self.area
        if self.keypoints is not None:
            ann["keypoints"] = self.keypoints
        if self.caption is not None:
            ann["caption"] = self.caption
        if self.value is not None:
            ann["value"] = self.value
        if self.iscrowd is not None:
            ann["iscrowd"] = self.iscrowd * 1

        return ann
