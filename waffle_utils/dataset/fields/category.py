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

        self.cat_id = cat_id
        self.supercategory = supercategory
        self.name = name
        self.keypoints = keypoints
        self.skeleton = skeleton

    # properties
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
    def supercategory(self):
        return self.__supercategory

    @supercategory.setter
    @type_validator(str)
    def supercategory(self, v):
        self.__supercategory = v

    @property
    def name(self):
        return self.__name

    @name.setter
    @type_validator(str)
    def name(self, v):
        self.__name = v

    @property
    def keypoints(self):
        return self.__keypoints

    @keypoints.setter
    @type_validator(list)
    def keypoints(self, v):
        self.__keypoints = v

    @property
    def skeleton(self):
        return self.__skeleton

    @skeleton.setter
    @type_validator(list)
    def skeleton(self, v):
        self.__skeleton = v

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
            "cat_id": self.cat_id,
            "supercategory": self.supercategory,
            "name": self.name,
        }

        if self.keypoints is not None:
            cat["keypoints"] = self.keypoints
        if self.skeleton is not None:
            cat["skeleton"] = self.skeleton

        return cat
