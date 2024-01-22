from pathlib import Path
from typing import Union

from natsort import natsorted

from waffle_utils.file.types import (
    SUPPORTED_IMAGE_EXTENSIONS,
    SUPPORTED_VIDEO_EXTENSION,
)


def is_empty(directory: Union[str, Path]) -> bool:
    """
    Check if a directory is empty or not.

    Args:
        directory (Union[str, Path]): Path to the directory.

    Returns:
        bool: True if the directory is empty, False otherwise.
    """
    directory = Path(directory)

    return not any(directory.iterdir())


def get_files(
    directory: Union[str, Path],
    recursive: bool = True,
    extension: Union[list[str], str, None] = None,
    include_directories: bool = False,
) -> list[Path]:
    """
    Retrieves a list of files in a directory, optionally filtered by extension.

    Args:
        directory (Union[str, Path]): Path to the directory.
        recursive (bool, optional): Whether to search recursively or not. Defaults to True.
        extension (Union[list[str], str, None], optional): File extension(including ".") to filter the files by. Defaults to None.
        include_directories (bool, optional): Whether to include directories in the list or not. Defaults to False.

    Returns:
        list: List of file paths.
    """
    directory = Path(directory)

    files = directory.glob(f"**/*" if recursive else "*")
    files = list(
        filter(lambda file: include_directories or file.is_file(), files)
    )
    if extension:
        if isinstance(extension, str):
            extension = [extension]
        extension = [ext.lower() for ext in extension]

        filtered_files = []
        for file in files:
            if file.suffix.lower() in extension or file.is_dir():
                filtered_files.append(file)
        files = filtered_files

    return natsorted(set(files))


def get_directories(
    directory: Union[str, Path],
    recursive: bool = True,
    only_empty: bool = False,
) -> list:
    """
    Retrieves a list of directories in a directory, optionally returns only empty directories.

    Args:
        directory (Union[str, Path]): Path to the directory.
        recursive (bool, optional): Whether to search recursively or not. Defaults to True.
        only_empty (bool, optional): Only empty directories are returned or not. Defaults to False.

    Returns:
        list: List of directory paths.
    """
    directory = Path(directory)

    files = directory.glob(f"**/*" if recursive else "*")
    files = list(
        filter(
            lambda file: file.is_dir() and is_empty(file)
            if only_empty
            else file.is_dir(),
            files,
        )
    )

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
