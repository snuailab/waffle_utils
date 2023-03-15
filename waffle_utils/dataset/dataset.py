import os
import random
import warnings
from functools import cached_property
from pathlib import Path
from typing import Union

from waffle_utils.file import io
from waffle_utils.utils import type_validator

from .fields import Annotation, Category, Image
from .format import Format


class Dataset:
    DEFAULT_DATASET_ROOT_DIR = Path("./datasets")
    RAW_IMAGE_DIR = Path("raw")
    IMAGE_DIR = Path("images")
    ANNOTATION_DIR = Path("annotations")
    CATEGORY_DIR = Path("categories")
    PREDICTION_DIR = Path("predictions")
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
        self.name = name
        self.root_dir = (
            Path(root_dir) if root_dir else Dataset.DEFAULT_DATASET_ROOT_DIR
        )

    # properties
    @property
    def name(self):
        return self.__name

    @name.setter
    @type_validator(str)
    def name(self, v):
        self.__name = v

    @property
    def root_dir(self):
        return self.__root_dir

    @root_dir.setter
    @type_validator(Path)
    def root_dir(self, v):
        self.__root_dir = v

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
    def prediction_dir(self) -> Path:
        return self.dataset_dir / Dataset.PREDICTION_DIR

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
        for image_dict in coco["images"]:
            image_id = image_dict.pop("id")
            ds.add_images(
                [Image.from_dict({**image_dict, "image_id": image_id})]
            )
        for annotation_dict in coco["annotations"]:
            annotation_id = annotation_dict.pop("id")
            ds.add_annotations(
                [
                    Annotation.from_dict(
                        {**annotation_dict, "annotation_id": annotation_id}
                    )
                ]
            )
        for category_dict in coco["categories"]:
            category_id = category_dict.pop("id")
            ds.add_categories(
                [
                    Category.from_dict(
                        {**category_dict, "category_id": category_id}
                    )
                ]
            )

        # copy raw images
        io.copy_files_to_directory(coco_root_dir, ds.raw_image_dir)

        return ds

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
    def get_images(self, image_ids: list[int] = None) -> list[Image]:
        """Get "Image"s.

        Args:
            image_ids (list[int], optional): id list. None for all "Image"s. Defaults to None.

        Returns:
            list[Image]: "Image" list
        """
        return [
            Image.from_json(f)
            for f in (
                [self.image_dir / f"{image_id}.json" for image_id in image_ids]
                if image_ids
                else self.image_dir.glob("*.json")
            )
        ]

    def get_categories(self, category_ids: list[int] = None) -> list[Category]:
        """Get "Category"s.

        Args:
            category_ids (list[int], optional): id list. None for all "Category"s. Defaults to None.

        Returns:
            list[Category]: "Category" list
        """
        return [
            Category.from_json(f)
            for f in (
                [
                    self.category_dir / f"{category_id}.json"
                    for category_id in category_ids
                ]
                if category_ids
                else self.category_dir.glob("*.json")
            )
        ]

    def get_annotations(self, image_id: int = None) -> list[Annotation]:
        """Get "Annotation"s.

        Args:
            image_id (int, optional): image id. None for all "Annotation"s. Defaults to None.

        Returns:
            list[Annotation]: "Annotation" list
        """
        if image_id:
            return [
                Annotation.from_json(f)
                for f in self.annotation_dir.glob(f"{image_id}/*.json")
            ]
        else:
            return [
                Annotation.from_json(f)
                for f in self.annotation_dir.glob("*/*.json")
            ]

    def get_predictions(self, image_id: int = None) -> list[Annotation]:
        """Get "Prediction"s.

        Args:
            image_id (int, optional): image id. None for all "Prediction"s. Defaults to None.

        Returns:
            list[Annotation]: "Prediction" list
        """
        if image_id:
            return [
                Annotation.from_json(f)
                for f in self.prediction_dir.glob(f"{image_id}/*.json")
            ]
        else:
            return [
                Annotation.from_json(f)
                for f in self.prediction_dir.glob("*/*.json")
            ]

    def get_labeled_images(self) -> list[Image]:
        """Get labeled "Image"s

        Returns:
            list[Image]: "Image" list
        """
        labeled_image_ids = map(
            lambda x: x.name,
            filter(
                lambda x: os.path.isdir(x), Path(self.annotation_dir).glob("*")
            ),
        )
        return [
            Image.from_json(self.image_dir / f"{image_id}.json")
            for image_id in labeled_image_ids
        ]

    # add
    def add_images(self, images: list[Image]):
        """Add "Image"s to dataset.

        Args:
            images (list[Image]): list of "Image"s
        """
        for item in images:
            item_id = item.image_id
            item_path = self.image_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    def add_categories(self, categories: list[Category]):
        """Add "Category"s to dataset.

        Args:
            categories (list[Category]): list of "Category"s
        """
        for item in categories:
            item_id = item.category_id
            item_path = self.category_dir / f"{item_id}.json"
            io.save_json(item.to_dict(), item_path)

    def add_annotations(self, annotations: list[Annotation]):
        """Add "Annotation"s to dataset.

        Args:
            annotations (list[Annotation]): list of "Annotation"s
        """
        for item in annotations:
            item_path = (
                self.annotation_dir
                / f"{item.image_id}"
                / f"{item.annotation_id}.json"
            )
            io.save_json(item.to_dict(), item_path, create_directory=True)

    def add_predictions(self, predictions: list[Annotation]):
        """Add "Annotation"s to dataset.

        Args:
            annotations (list[Annotation]): list of "Annotation"s
        """
        for item in predictions:
            item_path = (
                self.prediction_dir
                / f"{item.image_id}"
                / f"{item.annotation_id}.json"
            )
            io.save_json(item.to_dict(), item_path, create_directory=True)

    # functions
    def split_train_val(self, train_split_ratio: float, seed: int = 0):
        """Split Dataset to train and validation sets. (TODO: unlabeled set)

        Args:
            train_split_ratio (float): train num ratio
            seed (int, optional): random seed. Defaults to 0.
        """
        images: list[Image] = self.get_labeled_images()

        num_images = len(images)
        idxs = list(range(num_images))

        random.seed(seed)
        random.shuffle(idxs)

        train_num = round(num_images * train_split_ratio)

        train_image_idxs = idxs[:train_num]
        val_image_idxs = idxs[train_num:]

        io.save_json(
            [images[idx].image_id for idx in train_image_idxs],
            self.set_dir / self.TRAIN_SET_NAME,
            create_directory=True,
        )
        io.save_json(
            [images[idx].image_id for idx in val_image_idxs],
            self.set_dir / self.VAL_SET_NAME,
            create_directory=True,
        )

    # export
    def export(self, export_format: Union[str, Format]) -> str:
        f"""Export Dataset to Specific data formats

        Args:
            export_format (Union[str, Format]): export format. one of {list(map(lambda x: x.name, Format))}.

        Returns:
            str: exported dataset directory
        """
        if isinstance(export_format, str):
            export_format = export_format.upper()
            format_names = list(map(lambda x: x.name, Format))
            if export_format not in format_names:
                raise ValueError(
                    f"{export_format} is not supported. Use one of {format_names}"
                )
            export_format = Format[export_format]

        export_dir: Path = self.export_dir / export_format.name
        if export_dir.exists():
            io.remove_directory(export_dir)
            warnings.warn(
                f"{export_dir} already exists. Removing exist export and override."
            )
        io.make_directory(export_dir)

        if export_format == Format.YOLO_DETECTION:
            f"""YOLO DETECTION FORMAT
            - directory format
                yolo_dataset/
                    train/
                        images/
                            1.png
                        labels/
                            1.txt
                            ```
                            class x_center y_center width height
                            ```
                    val/
                        images/
                            2.png
                        labels/
                            2.txt
            - dataset.yaml
                path: [dataset_dir]/exports/{export_format.name}
                train: train
                val: val
                names:
                    0: person
                    1: bicycle
                    ...
            """

            def _export(images: list[Image], export_dir: Path):
                img_dir = export_dir / "images"
                label_dir = export_dir / "labels"

                io.make_directory(img_dir)
                io.make_directory(label_dir)

                for image in images:
                    image_path = self.raw_image_dir / f"{image.file_name}"
                    image_dst_path = img_dir / f"{image.file_name}"
                    label_dst_path = (
                        label_dir / f"{image.file_name}"
                    ).with_suffix(".txt")
                    io.copy_file(
                        image_path, image_dst_path, create_directory=True
                    )

                    W = image.width
                    H = image.height

                    annotations: list[Annotation] = self.get_annotations(
                        image.image_id
                    )
                    label_txts = []
                    for annotation in annotations:
                        x1, y1, w, h = annotation.bbox
                        x1, w = x1 / W, w / W
                        y1, h = y1 / H, h / H
                        cx, cy = x1 + w / 2, y1 + h / 2

                        category_id = annotation.category_id - 1

                        label_txts.append(f"{category_id} {cx} {cy} {w} {h}")

                    io.make_directory(label_dst_path.parent)
                    with open(label_dst_path, "w") as f:
                        f.write("\n".join(label_txts))

            train_set_file = (
                self.dataset_dir / self.SET_DIR / self.TRAIN_SET_NAME
            )
            val_set_file = self.dataset_dir / self.SET_DIR / self.VAL_SET_NAME

            if not train_set_file.exists() or not val_set_file.exists():
                # TODO: unlabeled export
                raise FileNotFoundError(
                    "There is no set files. Please run ds.split_train_val() first"
                )

            train_image_ids: list = io.load_json(train_set_file)
            val_image_ids: list = io.load_json(val_set_file)

            io.make_directory(export_dir / "train")
            io.make_directory(export_dir / "val")
            if train_image_ids:
                _export(self.get_images(train_image_ids), export_dir / "train")
            if val_image_ids:
                _export(self.get_images(val_image_ids), export_dir / "val")

            io.save_yaml(
                {
                    "path": str(export_dir.absolute()),
                    "train": "train",
                    "val": "val",
                    "names": {
                        category.category_id - 1: category.name
                        for category in self.get_categories()
                    },
                },
                export_dir / "data.yaml",
            )

            return str(export_dir)

        elif export_format == Format.YOLO_CLASSIFICATION:
            f"""YOLO CLASSIFICATION FORMAT (compatiable with torchvision.datasets.ImageFolder)
            - directory format
                yolo_dataset/
                    train/
                        person/
                            1.png
                        bicycle/
                            2.png
                    val/
                        person/
                            3.png
                        bicycle/
                            4.png
            - dataset.yaml
                path: [dataset_dir]/exports/{export_format.name}
                train: train
                val: val
                names:
                    0: person
                    1: bicycle
                    ...
            """

            def _export(
                images: list[Image],
                categories: list[Category],
                export_dir: Path,
            ):
                img_dir = export_dir
                cat_dict: dict = {
                    cat.category_id: cat.name for cat in categories
                }

                for image in images:
                    image_path = self.raw_image_dir / f"{image.file_name}"

                    annotations: list[Annotation] = self.get_annotations(
                        image.image_id
                    )
                    # TODO: multi label supports.
                    # TODO: check if YOLO will support multi label.
                    if len(annotations) > 1:
                        warnings.warn(
                            f"Multi label does not support yet. Skipping {image_path}."
                        )
                        continue
                    category_id = annotations[0].category_id

                    image_dst_path = (
                        img_dir / cat_dict[category_id] / f"{image.file_name}"
                    )
                    io.copy_file(
                        image_path, image_dst_path, create_directory=True
                    )

            train_set_file = (
                self.dataset_dir / self.SET_DIR / self.TRAIN_SET_NAME
            )
            val_set_file = self.dataset_dir / self.SET_DIR / self.VAL_SET_NAME

            if not train_set_file.exists() or not val_set_file.exists():
                # TODO: unlabeled export
                raise FileNotFoundError(
                    "There is no set files. Please run ds.split_train_val() first"
                )

            train_image_ids: list = io.load_json(train_set_file)
            val_image_ids: list = io.load_json(val_set_file)

            io.make_directory(export_dir / "train")
            io.make_directory(export_dir / "val")
            if train_image_ids:
                _export(
                    self.get_images(train_image_ids),
                    self.get_categories(),
                    export_dir / "train",
                )
            if val_image_ids:
                _export(
                    self.get_images(val_image_ids),
                    self.get_categories(),
                    export_dir / "val",
                )

            io.save_yaml(
                {
                    "path": str(export_dir.absolute()),
                    "train": "train",
                    "val": "val",
                    "names": {
                        category.category_id - 1: category.name
                        for category in self.get_categories()
                    },
                },
                export_dir / "data.yaml",
            )

            return str(export_dir)

        elif export_format == Format.YOLO_SEGMENTATION:
            raise NotImplementedError
        elif export_format == Format.COCO_DETECTION:
            raise NotImplementedError
