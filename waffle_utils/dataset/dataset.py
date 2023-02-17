import os
import random
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

    TRAIN_SET_NAME = Path("train.json")
    VAL_SET_NAME = Path("val.json")
    UNLABELED_SET_NAME = Path("unlabeled.json")

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
        """Create New Dataset

        Args:
            name (str): Dataset name
            root_dir (str, optional): Dataset root directory. Defaults to None.

        Raises:
            FileExistsError: if dataset name already exists

        Returns:
            Dataset: Dataset Class
        """
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
        """Clone Existing Dataset

        Args:
            src_name (str):
                Dataset name to clone.
                It should be Waffle Created Dataset.
            name (str): New Dataset name
            src_root_dir (str, optional): Source Dataset root directory. Defaults to None.
            root_dir (str, optional): New Dataset root directory. Defaults to None.

        Raises:
            FileNotFoundError: if source dataset does not exist.
            FileExistsError: if new dataset name already exist.

        Returns:
            Dataset: Dataset Class
        """
        src_ds = cls(src_name, src_root_dir)
        if not src_ds.initialized():
            raise FileNotFoundError(
                f"{src_ds.dataset_dir} has not been created by Waffle."
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
        """Load Dataset from directory.

        Args:
            name (str): Dataset name that Waffle Created
            root_dir (str, optional): Dataset root directory. Defaults to None.

        Raises:
            FileNotFoundError: if source dataset does not exist.

        Returns:
            Dataset: Dataset Class
        """
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
        """Import Dataset from coco format.

        Args:
            name (str): Dataset name.
            coco_file (str): Coco json file path.
            coco_root_dir (str): Coco image root directory.
            root_dir (str, optional): Dataset root directory. Defaults to None.

        Raises:
            FileExistsError: if new dataset name already exist.

        Returns:
            Dataset: Dataset Class
        """
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
        """Initialize Dataset.
        It creates necessary directories under {dataset_root_dir}/{dataset_name}.
        """
        io.make_directory(self.raw_image_dir)
        io.make_directory(self.image_dir)
        io.make_directory(self.annotation_dir)
        io.make_directory(self.category_dir)

    def initialized(self) -> bool:
        """Check if Dataset has been initialized or not.

        Returns:
            bool:
                initialized -> True
                not initialized -> False
        """
        return (
            self.raw_image_dir.exists()
            and self.image_dir.exists()
            and self.annotation_dir.exists()
            and self.category_dir.exists()
        )

    # get
    def get_imgs(self, img_ids: list[int] = None) -> list[Image]:
        """Get "Image"s.

        Args:
            img_ids (list[int], optional): id list. None for all "Image"s. Defaults to None.

        Returns:
            list[Image]: "Image" list
        """
        return [
            Image.from_json(f)
            for f in (
                [self.image_dir / f"{img_id}.json" for img_id in img_ids]
                if img_ids
                else self.image_dir.glob("*.json")
            )
        ]

    def get_cats(self, cat_ids: list[int] = None) -> list[Category]:
        """Get "Category"s.

        Args:
            cat_ids (list[int], optional): id list. None for all "Category"s. Defaults to None.

        Returns:
            list[Category]: "Category" list
        """
        return [
            Category.from_json(f)
            for f in (
                [self.category_dir / f"{cat_id}.json" for cat_id in cat_ids]
                if cat_ids
                else self.category_dir.glob("*.json")
            )
        ]

    def get_anns(self, img_id: int = None) -> list[Annotation]:
        """Get "Annotation"s.

        Args:
            img_id (int, optional): image id. None for all "Annotation"s. Defaults to None.

        Returns:
            list[Annotation]: "Annotation" list
        """
        if img_id:
            return [
                Annotation.from_json(f)
                for f in self.annotation_dir.glob(f"{img_id}/*.json")
            ]
        else:
            return [
                Annotation.from_json(f)
                for f in self.annotation_dir.glob("*/*.json")
            ]

    def get_labeled_imgs(self) -> list[Image]:
        """Get labeled "Image"s

        Returns:
            list[Image]: "Image" list
        """
        labeled_img_ids = map(
            lambda x: x.name,
            filter(
                lambda x: os.path.isdir(x), Path(self.annotation_dir).glob("*")
            ),
        )
        return [
            Image.from_json(self.image_dir / f"{img_id}.json")
            for img_id in labeled_img_ids
        ]

    # add
    def add_imgs(self, images: list[Image]):
        """Add "Image"s to dataset.

        Args:
            images (list[Image]): list of "Image"s
        """
        for item in images:
            item_id = item.img_id
            item_path = self.image_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    def add_cats(self, categories: list[Category]):
        """Add "Category"s to dataset.

        Args:
            categories (list[Category]): list of "Category"s
        """
        for item in categories:
            item_id = item.cat_id
            item_path = self.category_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    def add_anns(self, annotations: list[Annotation]):
        """Add "Annotation"s to dataset.

        Args:
            annotations (list[Annotation]): list of "Annotation"s
        """
        for item in annotations:
            item_path = (
                self.annotation_dir / f"{item.img_id}" / f"{item.ann_id}.json"
            )
            io.save_json(item.to_dict(), item_path, create_directory=True)

    # functions
    def split_train_val(self, train_split_ratio: float, seed: int = 0):
        """Split Dataset to train and validation sets. (TODO: unlabeled set)

        Args:
            train_split_ratio (float): train num ratio
            seed (int, optional): random seed. Defaults to 0.
        """
        imgs: list[Image] = self.get_labeled_imgs()

        num_imgs = len(imgs)
        idxs = list(range(num_imgs))

        random.seed(seed)
        random.shuffle(idxs)

        train_num = round(num_imgs * train_split_ratio)

        train_img_idxs = idxs[:train_num]
        val_img_idxs = idxs[train_num:]

        io.save_json(
            train_img_idxs,
            self.set_dir / self.TRAIN_SET_NAME,
            create_directory=True,
        )
        io.save_json(
            val_img_idxs,
            self.set_dir / self.VAL_SET_NAME,
            create_directory=True,
        )

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
