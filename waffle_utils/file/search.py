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
    if extension is None:
        # Return all files
        return [file for file in Path(directory).iterdir() if file.is_file()]
    else:
        # Return files with matching extension
        return [
            file
            for file in Path(directory).iterdir()
            if file.is_file() and file.suffix.lower()[1:] == extension.lower()[1:]
        ]


def get_image_files(directory: Union[str, Path]) -> list:
    """
    Retrieves a list of all image files in a directory.
    """
    image_files = []
    for file in Path(directory).iterdir():
        if file.is_file() and file.suffix.lower()[1:] in SUPPORTED_IMAGE_EXTENSION:
            image_files.append(file)
    return image_files


def get_video_files(directory: Union[str, Path]) -> list:
    """
    Retrieves a list of all video files in a directory.
    """
    video_files = []
    for file in Path(directory).iterdir():
        if file.is_file() and file.suffix.lower()[1:] in SUPPORTED_VIDEO_EXTENSION:
            video_files.append(file)
    return video_files


def get_unique_extensions(directory: Union[str, Path]):
    """
    Retrieves a set of all unique file extensions in a directory.
    """
    extensions = set()
    for file in Path(directory).iterdir():
        if file.is_file():
            extensions.add(file.suffix.lower()[1:])
    return extensions
