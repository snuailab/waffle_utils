import logging
import random
import warnings
from functools import cached_property
from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np

from waffle_utils.file import io
from waffle_utils.image.io import load_image
from waffle_utils.utils import type_validator

from .fields import Annotation, Category, Image
from .format import Format, polygon_to_rle

logger = logging.getLogger(__name__)


class Dataset:
    VALID_TASK_OPTIONS = ["classification", "object_detection"]

    DEFAULT_DATASET_ROOT_DIR = Path("./datasets")
    RAW_IMAGE_DIR = Path("raw")
    IMAGE_DIR = Path("images")
    ANNOTATION_DIR = Path("annotations")
    CATEGORY_DIR = Path("categories")
    PREDICTION_DIR = Path("predictions")
    EXPORT_DIR = Path("exports")
    SET_DIR = Path("sets")

    TRAIN_SET_FILE_NAME = Path("train.json")
    VAL_SET_FILE_NAME = Path("val.json")
    TEST_SET_FILE_NAME = Path("test.json")
    UNLABELED_SET_FILE_NAME = Path("unlabeled.json")

    def __init__(
        self,
        name: str,
        task: str,
        root_dir: Optional[Union[str, Path]] = None,
    ):
        # check valid task option
        self._validate_task(task)

        # set properties
        self.name = name
        self.root_dir = (
            Path(root_dir) if root_dir else Dataset.DEFAULT_DATASET_ROOT_DIR
        )
        self.task = task

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

    @property
    def task(self):
        return self.__task

    @task.setter
    @type_validator(str)
    def task(self, v):
        self.__task = v

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

    @cached_property
    def train_set_file(self) -> Path:
        return self.set_dir / Dataset.TRAIN_SET_FILE_NAME

    @cached_property
    def val_set_file(self) -> Path:
        return self.set_dir / Dataset.VAL_SET_FILE_NAME

    @cached_property
    def test_set_file(self) -> Path:
        return self.set_dir / Dataset.TEST_SET_FILE_NAME

    @cached_property
    def unlabeled_set_file(self) -> Path:
        return self.set_dir / Dataset.UNLABELED_SET_FILE_NAME

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
                f'{ds.dataset_dir} already exists. try another name or Dataset.load("{name}")'
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
    def load(cls, name: str, root_dir: str = None) -> "Dataset":
        """Load Dataset.

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
        coco_file: Union[str, Path],
        images_dir: Union[str, Path],
        root_dir: Optional[Union[str, Path]] = None,
    ) -> "Dataset":
        """Import Dataset from coco format.

        Args:
            name (str): Dataset name.
            coco_file (str): Coco json file path.
            images_dir (str): Coco image root directory.
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
        io.copy_files_to_directory(images_dir, ds.raw_image_dir)

        return ds

    @classmethod
    def from_yolo(
        cls,
        name: str,
        task: str,
        yolo_root_dir: Union[str, Path],
        images_dir: Union[str, Path],
        root_dir: Optional[Union[str, Path]] = None,
    ) -> "Dataset":
        """
        Import Dataset from YOLO format.

        Args:
            name (str): Dataset name.
            yolo_txt_dir (Union[str, Path]): Directory containing YOLO annotation files.
            images_dir (Union[str, Path]): Directory containing image files.
            yolo_yaml_file (Union[str, Path]): Path to the YOLO YAML file with category names.
            root_dir (Optional[Union[str, Path]]): Dataset root directory. Defaults to None.

        Raises:
            FileExistsError: If the new dataset name already exists.
            NotADirectoryError: If yolo_txt_dir is not a directory.

        Returns:
            Dataset: Dataset instance.
        """
        # check valid task type
        cls._validate_task(task)

        # function to process a single image
        def _process_image(
            ds: "Dataset", images_dir: Path, yolo_txt_file: Path
        ) -> Tuple[int, int, int]:
            """Processes an image file, adds it to the dataset, and returns its ID and dimensions.

            Args:
                ds (Dataset): The Dataset object to add the image to.
                images_dir (Path): The directory containing the image files.
                yolo_txt_file (Path): The path to the YOLO annotation file associated with the image.

            Returns:
                Tuple[int, int, int]: A tuple containing the image ID, width, and height.
            """
            # Extract the image_id from the yolo_txt_file name
            image_id = int(yolo_txt_file.stem)

            # Find the image file with the same id in the images_dir
            image_file_name = next(images_dir.glob(f"{image_id}.*")).name
            ext = image_file_name.split(".")[-1]
            image_file = images_dir / f"{image_id}.{ext}"

            # Load the image and get its dimensions
            image_width, image_height = load_image(image_file).shape[:2]

            # Create an Image instance from the image data
            image = Image.from_dict(
                {
                    "image_id": image_id,
                    "file_name": f"{image_id}.{ext}",
                    "width": image_width,
                    "height": image_height,
                }
            )

            # Add the image to the dataset
            ds.add_images([image])

            return image_id, image_width, image_height

        # function to process a single annotation file
        def _process_annotations(
            ds: "Dataset",
            yolo_txt_file: Path,
            image_id: int,
            image_width: int,
            image_height: int,
            annotation_id: int,
        ) -> int:
            """Processes the annotations from a YOLO annotation file and adds them to the dataset.

            Args:
                ds (Dataset): The Dataset object to add annotations to.
                yolo_txt_file (Path): The path to the YOLO annotation file.
                image_id (int): The ID of the image associated with the annotations.
                image_width (int): The width of the image associated with the annotations.
                image_height (int): The height of the image associated with the annotations.
                annotation_id (int): The starting annotation ID to be used for adding new annotations.

            Returns:
                int: The updated annotation ID after processing all annotations in the file.
            """
            # Load and split the YOLO annotation file into lines
            yolo_txt = io.load_txt(yolo_txt_file)
            yolo_txt_lines = yolo_txt.strip().splitlines()

            # Process each line in the YOLO annotation file
            for yolo_txt_line in yolo_txt_lines:
                # Parse the class_id and vertices from the annotation line
                class_id, *vertices = map(float, yolo_txt_line.split())
                class_id = int(class_id)

                # Scale the x and y coordinates of the vertices
                scaled_x_coords = [
                    int(np.round(x * image_width)) for x in vertices[0::2]
                ]
                scaled_y_coords = [
                    int(np.round(y * image_height)) for y in vertices[1::2]
                ]

                # Calculate the bounding box coordinates and dimensions
                xmin, xmax, ymin, ymax = (
                    min(scaled_x_coords),
                    max(scaled_x_coords),
                    min(scaled_y_coords),
                    max(scaled_y_coords),
                )
                bbox_width = int(np.round(xmax - xmin))
                bbox_height = int(np.round(ymax - ymin))

                # Create the bounding box and segmentation data
                bbox = [xmin, ymin, bbox_width, bbox_height]
                segmentation = polygon_to_rle(
                    image_width, image_height, scaled_x_coords, scaled_y_coords
                )
                area = bbox_width * bbox_height

                # Check if the values are integers
                assert isinstance(annotation_id, int)
                assert isinstance(image_id, int)
                assert isinstance(class_id, int)
                assert isinstance(bbox, list) and all(
                    isinstance(x, int) for x in bbox
                )
                assert isinstance(image_width, int)
                assert isinstance(image_height, int)
                assert isinstance(segmentation, list) and all(
                    isinstance(x, int) for x in segmentation
                )
                assert isinstance(area, int)

                # Create the annotation dictionary and add it to the dataset
                annotation = Annotation.from_dict(
                    {
                        "annotation_id": annotation_id,
                        "image_id": image_id,
                        "category_id": class_id + 1,
                        "bbox": bbox,
                        "segmentation": {
                            "size": [image_width, image_height],
                            "counts": segmentation,
                        },
                        "area": area,
                    }
                )

                ds.add_annotations([annotation])
                annotation_id += 1

            # Return the updated annotation_id
            return annotation_id

        images_dir = Path(images_dir)

        # Initialize the dataset
        ds = cls(name, task, root_dir)
        if ds.initialized():
            raise FileExistsError(
                f"{ds.dataset_dir} already exists. Try another name."
            )
        ds.initialize()

        if self.task == "object_detection":
            # FIXME: get yolo txt dir from yolo root dir
            # FIXME: get yolo yaml file from yolo root dir

            # Ensure yolo_txt_dir is a directory and convert it to a Path object
            yolo_txt_dir = Path(yolo_txt_dir)
            if not yolo_txt_dir.is_dir():
                raise NotADirectoryError(f"{yolo_txt_dir} is not a directory.")

            annotation_id = 1
            for yolo_txt_file in io.get_files_list(yolo_txt_dir):
                # Process images
                image_id, image_width, image_height = _process_image(
                    ds, images_dir, yolo_txt_file
                )

                # Process annotations
                annotation_id = _process_annotations(
                    ds,
                    yolo_txt_file,
                    image_id,
                    image_width,
                    image_height,
                    annotation_id,
                )

            # Process categories
            yolo_yaml = io.load_yaml(yolo_yaml_file)
            category_id = 0
            for name in yolo_yaml["names"]:
                category_id += 1
                ds.add_categories(
                    [
                        Category.from_dict(
                            {
                                "category_id": category_id,
                                "supercategory": None,
                                "name": name,
                            }
                        )
                    ]
                )

            # Copy raw images to the dataset directory
            io.copy_files_to_directory(images_dir, ds.raw_image_dir)

        elif self.task == "classification":
            # TODO: Implement classification task
            pass
        elif self.task == "segmentation":
            raise NotImplementedError(
                "Segmentation task is not implemented yet."
            )
        else:
            raise ValueError(f"Invalid task: {self.task}")

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
    def get_images(
        self, image_ids: list[int] = None, labeled: bool = True
    ) -> list[Image]:
        """Get "Image"s.

        Args:
            image_ids (list[int], optional): id list. None for all "Image"s. Defaults to None.
            labeled (bool, optional): get labeled images. False for unlabeled images. Defaults to True.

        Returns:
            list[Image]: "Image" list
        """
        image_files = (
            list(map(lambda x: self.image_dir / (str(x) + ".json"), image_ids))
            if image_ids
            else list(self.image_dir.glob("*.json"))
        )
        labeled_images = []
        unlabeled_images = []
        for image_file in image_files:
            if self.get_annotations(image_file.stem):
                labeled_images.append(Image.from_json(image_file))
            else:
                unlabeled_images.append(Image.from_json(image_file))

        if labeled:
            logger.info(f"Found {len(labeled_images)} labeled images")
            return labeled_images
        else:
            logger.info(f"Found {len(unlabeled_images)} unlabeled images")
            return unlabeled_images

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
    def split(
        self,
        train_ratio: float,
        val_ratio: float = 0.0,
        test_ratio: float = 0.0,
        seed: int = 0,
    ):
        """Split Dataset to train, validation, test, (unlabeled) sets.

        Args:
            train_ratio (float): train num ratio (0 ~ 1).
            val_ratio (float, optional): val num ratio (0 ~ 1).
            test_ratio (float, optional): test num ratio (0 ~ 1).
            seed (int, optional): random seed. Defaults to 0.
        """

        if val_ratio == 0.0:
            val_ratio = 1 - train_ratio

        total_ratio = train_ratio + val_ratio + test_ratio
        train_ratio = train_ratio / total_ratio
        val_ratio = val_ratio / total_ratio
        test_ratio = test_ratio / total_ratio

        images: list[Image] = self.get_images(labeled=True)

        num_images = len(images)

        random.seed(seed)
        random.shuffle(images)

        train_num = round(num_images * train_ratio)
        val_num = round(num_images * val_ratio)
        test_num = round(num_images * test_ratio)
        logger.info(f"train: {train_num}, val: {val_num}, test: {test_num}")

        train_images = images[:train_num]
        val_images = images[train_num : train_num + val_num]
        test_images = (
            images[train_num + val_num :] if test_num > 0 else val_images
        )

        io.save_json(
            list(map(lambda x: x.image_id, train_images)),
            self.train_set_file,
            create_directory=True,
        )
        io.save_json(
            list(map(lambda x: x.image_id, val_images)),
            self.val_set_file,
            create_directory=True,
        )
        io.save_json(
            list(map(lambda x: x.image_id, test_images)),
            self.test_set_file,
            create_directory=True,
        )

        unlabeled_images: list[Image] = self.get_images(labeled=False)

        io.save_json(
            list(map(lambda x: x.image_id, unlabeled_images)),
            self.unlabeled_set_file,
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

        # get split ids
        if not self.train_set_file.exists() or not self.val_set_file.exists():
            raise FileNotFoundError(
                "There is no set files. Please run ds.split() first"
            )

        train_image_ids: list = io.load_json(self.train_set_file)
        val_image_ids: list = io.load_json(self.val_set_file)
        test_image_ids: list = io.load_json(self.test_set_file)
        unlabeled_image_ids: list = io.load_json(self.unlabeled_set_file)

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
                    test/
                        images/
                            3.png
                        labels/
                            3.txt

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
                image_dir = export_dir / "images"
                label_dir = export_dir / "labels"

                io.make_directory(image_dir)
                io.make_directory(label_dir)

                for image in images:
                    image_path = self.raw_image_dir / image.file_name
                    image_dst_path = image_dir / image.file_name
                    label_dst_path = (label_dir / image.file_name).with_suffix(
                        ".txt"
                    )
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

            if train_image_ids:
                io.make_directory(export_dir / "train")
                _export(self.get_images(train_image_ids), export_dir / "train")
            if val_image_ids:
                io.make_directory(export_dir / "val")
                _export(self.get_images(val_image_ids), export_dir / "val")
            if test_image_ids:
                io.make_directory(export_dir / "test")
                _export(self.get_images(test_image_ids), export_dir / "test")

            io.save_yaml(
                {
                    "path": str(export_dir.absolute()),
                    "train": "train",
                    "val": "val",
                    "test": "test",
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
                    test/
                        person/
                            5.png
                        bicycle/
                            6.png
            - dataset.yaml
                path: [dataset_dir]/exports/{export_format.name}
                train: train
                val: val
                test: test
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
                image_dir = export_dir
                cat_dict: dict = {
                    cat.category_id: cat.name for cat in categories
                }

                for image in images:
                    image_path = self.raw_image_dir / image.file_name

                    annotations: list[Annotation] = self.get_annotations(
                        image.image_id
                    )
                    if len(annotations) > 1:
                        warnings.warn(
                            f"Multi label does not support yet. Skipping {image_path}."
                        )
                        continue
                    category_id = annotations[0].category_id

                    image_dst_path = (
                        image_dir / cat_dict[category_id] / image.file_name
                    )
                    io.copy_file(
                        image_path, image_dst_path, create_directory=True
                    )

            if train_image_ids:
                io.make_directory(export_dir / "train")
                _export(
                    self.get_images(train_image_ids),
                    self.get_categories(),
                    export_dir / "train",
                )
            if val_image_ids:
                io.make_directory(export_dir / "val")
                _export(
                    self.get_images(val_image_ids),
                    self.get_categories(),
                    export_dir / "val",
                )
            if test_image_ids:
                io.make_directory(export_dir / "test")
                _export(
                    self.get_images(test_image_ids),
                    self.get_categories(),
                    export_dir / "test",
                )

            io.save_yaml(
                {
                    "path": str(export_dir.absolute()),
                    "train": "train",
                    "val": "val",
                    "test": "test",
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
            """COCO DETECTION FORMAT
            - directory format
                coco_dataset/
                    images/
                        1.png
                        ...
                    train.json
                    val.json
                    test.json
            """

            def _export(images: list[Image], set_name: str, export_dir: Path):
                image_dir = export_dir / "images"
                label_path = export_dir / f"{set_name}.json"

                io.make_directory(image_dir)

                coco = {"categories": [], "images": [], "annotations": []}

                for category in self.get_categories():
                    d = category.to_dict()
                    category_id = d.pop("category_id")
                    coco["categories"].append({"id": category_id, **d})

                for image in images:
                    image_path = self.raw_image_dir / image.file_name
                    image_dst_path = image_dir / image.file_name
                    io.copy_file(
                        image_path, image_dst_path, create_directory=True
                    )

                    d = image.to_dict()
                    image_id = d.pop("image_id")
                    coco["images"].append({"id": image_id, **d})

                    annotations = self.get_annotations(image_id)
                    for annotation in annotations:
                        d = annotation.to_dict()
                        annotation_id = d.pop("annotation_id")
                        coco["annotations"].append({"id": annotation_id, **d})

                io.save_json(coco, label_path, create_directory=True)

            if train_image_ids:
                _export(self.get_images(train_image_ids), "train", export_dir)
            if val_image_ids:
                _export(self.get_images(val_image_ids), "val", export_dir)
            if test_image_ids:
                _export(self.get_images(test_image_ids), "test", export_dir)
            if unlabeled_image_ids:
                _export(
                    self.get_images(unlabeled_image_ids, labeled=False),
                    "unlabeled",
                    export_dir,
                )

            return str(export_dir)

    # validation check
    @staticmethod
    def _validate_task(task: str) -> None:
        if task not in Dataset.VALID_TASK_OPTIONS:
            raise ValueError(
                f"Invalid task: {task}. Valid tasks are {Dataset.VALID_TASK_OPTIONS}"
            )
