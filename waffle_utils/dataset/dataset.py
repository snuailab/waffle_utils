from functools import cached_property
from pathlib import Path

from waffle_utils.utils import type_validator

from . import Format
from .fields import Annotation, Category, Image


class Dataset:
    DEFAULT_DATASET_ROOT_DIR = Path("./datasets")
    IMAGE_DIR = Path("images")
    LABEL_DIR = Path("labels")
    SET_DIR = Path("sets")

    def __init__(
        self,
        name: str,
        root_dir: str = None,
    ):
        self.name = self._name = name
        self.root_dir = self._root_dir = (
            Path(root_dir) if root_dir else Dataset.DEFAULT_DATASET_ROOT_DIR
        )

    # properties
    @property
    def name(self):
        return self._name

    @name.setter
    @type_validator(str)
    def name(self, v):
        self._name = v

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    @type_validator(str)
    def root_dir(self, v):
        self._root_dir = v

    # cached properties
    @cached_property
    def dataset_dir(self) -> Path:
        return self.root_dir / self.name

    @cached_property
    def image_dir(self) -> Path:
        return self.root_dir / Dataset.IMAGE_DIR

    @cached_property
    def label_dir(self) -> Path:
        return self.root_dir / Dataset.LABEL_DIR

    @cached_property
    def set_dir(self) -> Path:
        return self.root_dir / Dataset.SET_DIR

    # factories
    @classmethod
    def new(cls, *args, **kwargs) -> "Dataset":
        return cls(*args, **kwargs)

    @classmethod
    def clone(cls) -> "Dataset":
        raise NotImplementedError

    @classmethod
    def from_directory(cls) -> "Dataset":
        raise NotImplementedError

    @classmethod
    def from_nas(cls) -> "Dataset":
        # download to root_dir from nas
        # return cls(root_dir=root_dir)
        raise NotImplementedError

    @classmethod
    def from_minio(cls) -> "Dataset":
        # download to root_dir from minio
        # return cls(root_dir=root_dir)
        raise NotImplementedError

    @classmethod
    def from_ftp(cls) -> "Dataset":
        # download to root_dir from ftp
        # return cls(root_dir=root_dir)
        raise NotImplementedError

    # get
    def get_imgs(self) -> list[Image]:
        pass

    def get_cats(self) -> list[Category]:
        pass

    def get_anns(self) -> list[Annotation]:
        pass

    # add
    def add_img(self, img: Image):
        pass

    def add_cat(self, cat: Category):
        pass

    def add_ann(self, ann: Annotation):
        pass

    # export
    def export(self, export_format: Format) -> str:
        pass
