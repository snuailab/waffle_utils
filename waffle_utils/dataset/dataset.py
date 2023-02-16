from functools import cached_property
from pathlib import Path

from waffle_utils.file import io
from waffle_utils.utils import type_validator

from .fields import Annotation, Category, Image
from .format import Format


class Dataset:
    DEFAULT_DATASET_ROOT_DIR = Path("./datasets")
    RAW_IMAGE_DIR = Path("raw")
    IMAGE_DIR = Path("images")
    ANNOTATION_DIR = Path("labels")
    CATEGORY_DIR = Path("categories")
    EXPORT_DIR = Path("exports")
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
    @type_validator(Path)
    def root_dir(self, v):
        self._root_dir = v

    # cached properties
    @cached_property
    def dataset_dir(self) -> Path:
        return self.root_dir / self.name

    @cached_property
    def raw_image_dir(self) -> Path:
        return self.dataset_dir / Dataset.RAW_IMAGE_DIR

    @cached_property
    def image_dir(self) -> Path:
        return self.dataset_dir / Dataset.IMAGE_DIR

    @cached_property
    def annotation_dir(self) -> Path:
        return self.dataset_dir / Dataset.ANNOTATION_DIR

    @cached_property
    def category_dir(self) -> Path:
        return self.dataset_dir / Dataset.CATEGORY_DIR

    @cached_property
    def export_dir(self) -> Path:
        return self.dataset_dir / Dataset.EXPORT_DIR

    @cached_property
    def set_dir(self) -> Path:
        return self.dataset_dir / Dataset.SET_DIR

    # factories
    @classmethod
    def new(cls, name: str, root_dir: str = None) -> "Dataset":
        ds = cls(name, root_dir)
        if ds.initialized():
            raise FileExistsError(
                f'{ds.dataset_dir} already exists. try another name or Dataset.from_directory("{name}")'
            )
        ds.initialize()
        return ds

    @classmethod
    def clone(
        cls,
        src_name: str,
        name: str,
        src_root_dir: str = None,
        root_dir: str = None,
    ) -> "Dataset":
        src_ds = cls(src_name, src_root_dir)
        if not src_ds.initialized():
            raise FileNotFoundError(
                f"{src_ds.dataset_dir} has not been created."
            )

        ds = cls(name, root_dir)
        if ds.initialized():
            raise FileExistsError(
                f"{ds.dataset_dir} already exists. try another name."
            )
        ds.initialize()
        io.copy_files_to_directory(
            src_ds.dataset_dir, ds.dataset_dir, create_directory=True
        )

    @classmethod
    def from_directory(cls, name: str, root_dir: str = None) -> "Dataset":
        ds = cls(name, root_dir)
        if not ds.initialized():
            raise FileNotFoundError(
                f'{ds.dataset_dir} has not been created. Run Dataset.new("{name}") first.'
            )
        return ds

    @classmethod
    def from_coco(
        cls,
        name: str,
        coco_file: str,
        coco_root_dir: str,
        root_dir: str = None,
    ) -> "Dataset":
        ds = cls(name, root_dir)
        if ds.initialized():
            raise FileExistsError(
                f"{ds.dataset_dir} already exists. try another name."
            )
        ds.initialize()

        # parse coco annotation file
        coco = io.load_json(coco_file)
        ds.add_imgs([Image.from_dict(image) for image in coco["images"]])
        ds.add_anns(
            [
                Annotation.from_dict(annotation)
                for annotation in coco["annotations"]
            ]
        )
        ds.add_cats(
            [Category.from_dict(category) for category in coco["categories"]]
        )

        # copy raw images
        io.copy_files_to_directory(coco_root_dir, ds.raw_image_dir)

        return ds

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

    def initialize(self):
        io.make_directory(self.raw_image_dir)
        io.make_directory(self.image_dir)
        io.make_directory(self.annotation_dir)
        io.make_directory(self.category_dir)

    def initialized(self):
        return (
            self.raw_image_dir.exists()
            and self.image_dir.exists()
            and self.annotation_dir.exists()
            and self.category_dir.exists()
        )

    # get
    def get_imgs(self) -> list[Image]:
        return [
            Image.from_json(f) for f in Path(self.image_dir).glob("*.json")
        ]

    def get_cats(self) -> list[Category]:
        return [
            Category.from_json(f)
            for f in Path(self.category_dir).glob("*.json")
        ]

    def get_anns(self) -> list[Annotation]:
        return [
            Annotation.from_json(f)
            for f in Path(self.annotation_dir).glob("*.json")
        ]

    # add
    def add_imgs(self, images: list[Image]):
        for item in images:
            item_id = item.img_id
            item_path = self.image_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    def add_cats(self, categories: list[Category]):
        for item in categories:
            item_id = item.cat_id
            item_path = self.category_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    def add_anns(self, annotations: list[Annotation]):
        for item in annotations:
            item_id = item.ann_id
            item_path = self.annotation_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    # export
    def export(self, export_format: Format) -> str:
        if export_format == Format.YOLO_DETECTION:
            raise NotImplementedError
        elif export_format == Format.YOLO_CLASSIFICATION:
            raise NotImplementedError
        elif export_format == Format.YOLO_SEGMENTATION:
            raise NotImplementedError
        elif export_format == Format.COCO_DETECTION:
            raise NotImplementedError
