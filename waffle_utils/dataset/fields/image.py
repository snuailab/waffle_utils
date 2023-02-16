from waffle_utils.file import io
from waffle_utils.log import datetime_now
from waffle_utils.utils import type_validator

from . import BaseField


class Image(BaseField):
    def __init__(
        self,
        # required
        img_id: int,
        file_name: str,
        width: int,
        height: int,
        # optional
        date_captured: str = None,
    ):

        self.img_id = self._img_id = img_id
        self.file_name = self._file_name = file_name
        self.width = self._width = width
        self.height = self._height = height
        self.date_captured = self._date_captured = date_captured

    # properties
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
    def file_name(self):
        return self._file_name

    @file_name.setter
    @type_validator(str)
    def file_name(self, v):
        self._file_name = v

    @property
    def width(self):
        return self._width

    @width.setter
    @type_validator(int)
    def width(self, v):
        self._width = v

    @property
    def height(self):
        return self._height

    @height.setter
    @type_validator(int)
    def height(self, v):
        self._height = v

    @property
    def date_captured(self):
        return self._date_captured

    @date_captured.setter
    @type_validator(str)
    def date_captured(self, v):
        if v is None:
            self._date_captured = datetime_now()
        else:
            self._date_captured = v

    @classmethod
    def new(
        cls,
        img_id: int,
        file_name: str,
        width: int,
        height: int,
        date_captured: str = None,
    ) -> "Image":
        """Image Format

        Args:
            img_id (int): image id. natural number.
            file_name (str): file name. relative file path.
            width (int): image width.
            height (int): image height.
            date_captured (str): date_captured string. "%Y-%m-%d %H:%M:%S"

        Returns:
            Image: image class
        """
        return cls(img_id, file_name, width, height, date_captured)

    @classmethod
    def from_dict(cls, d: dict) -> "Image":
        """Image Format from dictionary

        Args:
            d (dict): Image dictionary

        Returns:
            Image: image class
        """
        img_id = d.get("id", None)
        file_name = d.get("file_name", None)
        width = d.get("width", None)
        height = d.get("height", None)
        date_captured = d.get("date_captured", datetime_now())

        if img_id is None:
            raise ValueError("id field missing")
        if file_name is None:
            raise ValueError("file_name field missing")
        if width is None:
            raise ValueError("width field missing")
        if height is None:
            raise ValueError("height field missing")

        return cls(img_id, file_name, width, height, date_captured)

    @classmethod
    def from_json(cls, f: str) -> "Image":
        """Image Format from json file

        Args:
            d (dict): Image json file

        Returns:
            Image: Image class
        """
        d: dict = io.load_json(f)
        return cls.from_dict(d)

    def to_dict(self) -> dict:
        """Get Dictionary of Category

        Returns:
            dict: annotation dictionary.
        """

        cat = {
            "id": self.img_id,
            "file_name": self.file_name,
            "width": self.width,
            "height": self.height,
            "date_captured": self.date_captured,
        }

        return cat
