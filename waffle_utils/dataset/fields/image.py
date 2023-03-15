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

        self.img_id = img_id
        self.file_name = file_name
        self.width = width
        self.height = height
        self.date_captured = date_captured

    # properties
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
    def file_name(self):
        return self.__file_name

    @file_name.setter
    @type_validator(str)
    def file_name(self, v):
        self.__file_name = v

    @property
    def width(self):
        return self.__width

    @width.setter
    @type_validator(int)
    def width(self, v):
        self.__width = v

    @property
    def height(self):
        return self.__height

    @height.setter
    @type_validator(int)
    def height(self, v):
        self.__height = v

    @property
    def date_captured(self):
        return self.__date_captured

    @date_captured.setter
    @type_validator(str)
    def date_captured(self, v):
        if v is None:
            self.__date_captured = datetime_now()
        else:
            self.__date_captured = v

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

    def to_dict(self) -> dict:
        """Get Dictionary of Category

        Returns:
            dict: annotation dictionary.
        """

        cat = {
            "img_id": self.img_id,
            "file_name": self.file_name,
            "width": self.width,
            "height": self.height,
            "date_captured": self.date_captured,
        }

        return cat
