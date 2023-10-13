from pathlib import Path
from typing import Union

from natsort import natsorted

from waffle_utils.file.types import (
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_EXTENSION,
)


def get_files(
    directory: Union[str, Path],
    recursive: bool = True,
    extension: Union[list[str], str, None] = None,
) -> list:
    """
    Retrieves a list of files in a directory, optionally filtered by extension.

    Args:
        directory (Union[str, Path]): Path to the directory.
        recursive (bool, optional): Whether to search recursively or not. Defaults to True.
        extension (Union[list[str], str, None], optional): File extension(including ".") to filter the files by. Defaults to None.

    Returns:
        list: List of file paths.
    """
    directory = Path(directory)

    files = directory.glob(f"**/*" if recursive else "*")
    files = list(filter(lambda file: file.is_file(), files))
    if extension:
        if isinstance(extension, str):
            extension = [extension]
        extension = [ext.lower() for ext in extension]
        files = [file for file in files if file.suffix.lower() in extension]

    return natsorted(set(files))


def get_image_files(
    directory: Union[str, Path], recursive: bool = True
) -> list:
    """
    Retrieves a list of all image files in a directory.

    Args:
        directory (Union[str, Path]): Path to the directory.
        recursive (bool, optional): Whether to search recursively or not. Defaults to True.

    Returns:
        list: List of image file paths.
    """
    return get_files(
        directory, recursive=recursive, extension=SUPPORTED_IMAGE_EXTENSIONS
    )


def get_video_files(
    directory: Union[str, Path], recursive: bool = True
) -> list:
    """
    Retrieves a list of all video files in a directory.

    Args:
        directory (Union[str, Path]): Path to the directory.
        recursive (bool, optional): Whether to search recursively or not. Defaults to True.

    Returns:
        list: List of video file paths.
    """
    return get_files(
        directory, recursive=recursive, extension=SUPPORTED_VIDEO_EXTENSION
    )
