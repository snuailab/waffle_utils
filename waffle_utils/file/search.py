from pathlib import Path
from typing import List, Optional, Union


def get_files(directory: Union[str, Path], extension: Union[str, None] = None) -> list:
    """
    Retrieves a list of files in a directory, optionally filtered by extension.

    Args:
        directory (Union[str, Path]): Path to the directory.
        extension (Union[str, None], optional): File extension to filter the files by. Defaults to None.

    Returns:
        list: List of file paths.
    """
    raise NotImplementedError("`get_files` is not implemented yet.")


def get_image_files(directory: Union[str, Path]) -> list:
    """
    Retrieves a list of all image files in a directory.

    Args:
        directory (Union[str, Path]): Path to the directory.

    Returns:
        list: List of image file paths.
    """
    raise NotImplementedError("`get_image_files` is not implemented yet.")


def get_video_files(directory: Union[str, Path]) -> list:
    """
    Retrieves a list of all video files in a directory.

    Args:
        directory (Union[str, Path]): Path to the directory.

    Returns:
        list: List of video file paths.
    """
    raise NotImplementedError("`get_video_files` is not implemented yet.")


def get_file_extensions(
    directory: Union[str, Path], single: Optional[bool] = False
) -> Union[List[str], str]:
    """
    Returns either a list of all unique file extensions or a single file extension found in the specified directory.

    The function retrieves all file extensions in the directory using the `get_extensions()` function.
    If `single` is True, it then checks if there is only one extension among the files, and returns it
    without the leading dot. If there is not a single consistent extension in the directory, a `ValueError`
    is raised. If `single` is False (default), it returns a list of all unique file extensions found in the
    directory.

    Args:
        directory (Union[str, Path]): The directory to search for file extensions.
        single (Optional[bool]): Whether to return a single file extension (True) or a list of all unique file extensions (False). Defaults to False.

    Returns:
        Union[List[str], str]: Either a list of all unique file extensions or a single file extension found in the directory.

    Raises:
        ValueError: If `single` is True and there is not a single consistent file extension in the directory.
    """
    extensions = set()
    for file in Path(directory).iterdir():
        if file.is_file():
            extensions.add(file.suffix.lower())

    if single:
        distinct_extensions = set(extensions)
        if len(distinct_extensions) != 1:
            raise ValueError(
                f"The files in {directory} do not have a single file extension."
            )
        return distinct_extensions.pop()[1:]

    return list(extensions)
