from pathlib import Path
from typing import Union

from waffle_utils.video.config import (
    SUPPORTED_IMAGE_EXTENSION,
    SUPPORTED_VIDEO_EXTENSION,
)


def get_files(directory: Union[str, Path], extension: Union[str, None] = None) -> list:
    """
    Retrieves a list of files in a directory, optionally filtered by extension.
    """
    raise NotImplementedError("`get_files` is not implemented yet.")


def get_image_files(directory: Union[str, Path]) -> list:
    """
    Retrieves a list of all image files in a directory.
    """
    raise NotImplementedError("`get_image_files` is not implemented yet.")


def get_video_files(directory: Union[str, Path]) -> list:
    """
    Retrieves a list of all video files in a directory.
    """
    raise NotImplementedError("`get_video_files` is not implemented yet.")


def get_unique_extensions(directory: Union[str, Path]):
    """
    Retrieves a set of all unique file extensions in a directory.
    """
    extensions = set()
    for file in Path(directory).iterdir():
        if file.is_file():
            extensions.add(file.suffix.lower())
    return extensions
