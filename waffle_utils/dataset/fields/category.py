from waffle_utils.file import io
from waffle_utils.utils import type_validator

from . import BaseField


class Category(BaseField):
    def __init__(
        self,
        # required
        cat_id: int,
        supercategory: str,
        name: str,
        # for keypoint detection
        keypoints: list[str] = None,
        skeleton: list[list[int]] = None,
    ):

        self.cat_id = self._cat_id = cat_id
        self.supercategory = self._supercategory = supercategory
        self.name = self._name = name
        self.keypoints = self._keypoints = keypoints
        self.skeleton = self._skeleton = skeleton

    # properties
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
    def supercategory(self):
        return self._supercategory

    @supercategory.setter
    @type_validator(str)
    def supercategory(self, v):
        self._supercategory = v

    @property
    def name(self):
        return self._name

    @name.setter
    @type_validator(str)
    def name(self, v):
        self._name = v

    @property
    def keypoints(self):
        return self._keypoints

    @keypoints.setter
    @type_validator(list)
    def keypoints(self, v):
        self._keypoints = v

    @property
    def skeleton(self):
        return self._skeleton

    @skeleton.setter
    @type_validator(list)
    def skeleton(self, v):
        self._skeleton = v

    # factories
    @classmethod
    def new(
        cls,
        cat_id: int,
        supercategory: str,
        name: str,
        keypoints: list[str] = None,
        skeleton: list[list[int]] = None,
    ) -> "Category":
        """Category Format

        Args:
            cat_id (int): category id. natural number.
            supercategory (str): supercategory name.
            name (str): category name.
            keypoints (list[str]): category name.
            skeleton (list[list[int]]): skeleton edges.

        Returns:
            Category: category class
        """
        return cls(cat_id, supercategory, name, keypoints, skeleton)

    @classmethod
    def from_dict(cls, d: dict) -> "Category":
        """Category Format from dictionary

        Args:
            d (dict): Category dictionary

        Returns:
            Category: category class
        """
        cat_id = d.get("id", None)
        supercategory = d.get("supercategory", None)
        name = d.get("name", None)
        keypoints = d.get("keypoints", None)
        skeleton = d.get("skeleton", None)

        if cat_id is None:
            raise ValueError("id field missing")
        if supercategory is None:
            raise ValueError("file_name field missing")
        if name is None:
            raise ValueError("width field missing")

        return cls(cat_id, supercategory, name, keypoints, skeleton)

    @classmethod
    def from_json(cls, f: str) -> "Category":
        """Category Format from json file

        Args:
            d (dict): Category json file

        Returns:
            Category: Category class
        """
        d: dict = io.load_json(f)
        return cls.from_dict(d)

    @classmethod
    def classification(
        cls, cat_id: int, supercategory: str, name: str
    ) -> "Category":
        """Classification Category Format

        Args:
            cat_id (int): category id. natural number.
            supercategory (str): supercategory name.
            name (str): category name.

        Returns:
            Category: category class
        """
        return cls(cat_id, supercategory, name)

    @classmethod
    def object_detection(
        cls, cat_id: int, supercategory: str, name: str
    ) -> "Category":
        """Object Detection Category Format

        Args:
            cat_id (int): category id. natural number.
            supercategory (str): supercategory name.
            name (str): category name.

        Returns:
            Category: category class
        """
        return cls(cat_id, supercategory, name)

    @classmethod
    def segmentation(
        cls, cat_id: int, supercategory: str, name: str
    ) -> "Category":
        """Segmentation Category Format

        Args:
            cat_id (int): category id. natural number.
            supercategory (str): supercategory name.
            name (str): category name.

        Returns:
            Category: category class
        """
        return cls(cat_id, supercategory, name)

    @classmethod
    def keypoint_detection(
        cls,
        cat_id: int,
        supercategory: str,
        name: str,
        keypoints: list[str],
        skeleton: list[list[int]],
    ) -> "Category":
        """Keypoint Detection Category Format

        Args:
            cat_id (int): category id. natural number.
            supercategory (str): supercategory name.
            name (str): category name.
            keypoints (list[str]): category name.
            skeleton (list[list[int]]): skeleton edges.

        Returns:
            Category: category class
        """
        return cls(
            cat_id, supercategory, name, keypoints=keypoints, skeleton=skeleton
        )

    @classmethod
    def text_recognition(
        cls, cat_id: int, supercategory: str, name: str
    ) -> "Category":
        """Text Recognition Category Format

        Args:
            cat_id (int): category id. natural number.
            supercategory (str): supercategory name.
            name (str): category name.

        Returns:
            Category: category class
        """
        return cls(cat_id, supercategory, name)

    def to_dict(self) -> dict:
        """Get Dictionary of Category

        Returns:
            dict: annotation dictionary.
        """

        cat = {
            "id": self.cat_id,
            "supercategory": self.supercategory,
            "name": self.name,
        }

        if self.keypoints is not None:
            cat["keypoints"] = self.keypoints
        if self.skeleton is not None:
            cat["skeleton"] = self.skeleton

        return cat
