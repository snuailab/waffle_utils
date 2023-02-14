
def check_id(f):
    def inner(self, v, *args, **kwargs):
        if not isinstance(v, int) or v < 1:
            raise ValueError("id should be 'int' type and greater than 0")
        return f(self, v, *args, **kwargs)
    return inner

class Annotation:
    
    def __init__(
        self,
        # required
        ann_id: int,
        image_id: int,
        # optional
        category_id: int = 0,
        bbox: list[int] = [],
        mask: list[int] = [],
        keypoints: list[int] = [],
        caption: str = "",
        value: float = 0.,
        # 
        iscrowd: bool = False
    ):
        
        self._ann_id = ann_id
        self._image_id = image_id
        
        self._category_id = category_id
        self._bbox = bbox
        self._mask = mask
        self._keypoints = keypoints
        self._caption = caption
        self._value = value
        
        self._iscrowd = iscrowd
        self._area = 0

    # properties
    @property
    def ann_id(self):
        return self._ann_id
    
    @ann_id.setter
    @check_id
    def ann_id(self, v):
        self._ann_id = v
        
    @property
    def image_id(self):
        return self._image_id
    
    @image_id.setter
    @check_id
    def image_id(self, v):
        self._image_id = v
        
    @property
    def category_id(self):
        return self._category_id
    
    @category_id.setter
    @check_id
    def category_id(self, v):
        self._category_id = v

    @property
    def bbox(self):
        return self._bbox

    @bbox.setter
    def bbox(self, v):
        if v:
            if not isinstance(v, list[int]) or len(v) != 4:
                raise ValueError("bbox should be a list of integers and the length of the list should be 4.")
        self._bbox = v
        self._area = v[2] * v[3]

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, v):
        if v:
            if not isinstance(v, list[int]) or len(v) % 2 != 0:
                raise ValueError("mask should be a list of integers and the length of the list should be divisible by 2.")
        self._mask = v

    @property
    def keypoints(self):
        return self._keypoints

    @keypoints.setter
    def keypoints(self, v):
        if v:
            if not isinstance(v, list[int]) or len(v) % 3 != 0:
                raise ValueError("keypoints should be a list of integers and the length of the list should be divisible by 3.")
        self._keypoints = v

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, v):
        if v:
            if not isinstance(v, str):
                raise ValueError("caption should be a str type.")
        self._caption = v

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v:
            if not isinstance(v, float):
                raise ValueError("value should be a number.")
        self._value = float(v)

    @property
    def iscrowd(self):
        return self._iscrowd

    @iscrowd.setter
    def iscrowd(self, v):
        if v:
            if not isinstance(v, bool):
                raise ValueError("iscrowd should be a bool.")
        self._iscrowd = float(v)
    
    # factories
    @classmethod
    def classification(cls, ann_id: int, image_id: int, category_id: int):
        return cls(ann_id, image_id, category_id=category_id)
    
    @classmethod
    def object_detection(cls, ann_id: int, image_id: int, category_id: int, bbox: list[int], iscrowd: bool = False):
        return cls(ann_id, image_id, category_id=category_id, bbox=bbox, iscrowd=iscrowd)
    
    @classmethod
    def segmentation(cls, ann_id: int, image_id: int, category_id: int, mask: list[int], iscrowd: bool = False):
        return cls(ann_id, image_id, category_id=category_id, mask=mask, iscrowd=iscrowd)
    
    @classmethod
    def keypoint_detection(cls, ann_id: int, image_id: int, category_id: int, keypoints: list[int], bbox: list[int] = [], iscrowd: bool = False):
        return cls(ann_id, image_id, category_id=category_id, keypoints=keypoints, bbox=bbox, iscrowd=iscrowd)
    
    @classmethod
    def regression(cls, ann_id: int, image_id: int, value: float):
        return cls(ann_id, image_id, value=value)
    
    @classmethod
    def text_recognition(cls, ann_id: int, image_id: int, caption: str):
        return cls(ann_id, image_id, caption=caption)
    
    
    def to_dict(self):
        
        ann = {
            "id": self.ann_id,
            "image_id": self.image_id,
            "iscrowd": self.iscrowd * 1
        }
        
        if self.category_id:
            ann["category_id"] = self.category_id
        if self.bbox:
            ann["bbox"] = self.bbox
        if self.mask:
            ann["segmentations"] = self.mask
        if self.keypoints:
            ann["keypoints"] = self.keypoints
        if self.caption:
            ann["caption"] = self.caption
        if self.value:
            ann["value"] = self.value
        
        