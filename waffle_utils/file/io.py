import json
import os
import shutil
import zipfile
from pathlib import Path, PurePath
from typing import Any, Union

import yaml

from waffle_utils.file import search


def save_json(obj: Any, fp: Union[str, Path], create_directory: bool = False):
    """save json file

    Args:
        obj (Any): Any object that can be converted to json format.
        fp (Union[str, Path]): file path.
        create_directory (bool, optional): this determines whether create parent directory or not. Default to False.
    """

    fp = Path(fp)
    if create_directory:
        make_directory(fp.parent)

    with open(fp, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def load_json(fp: Union[str, Path]) -> dict:
    """load json file

    Args:
        fp (Union[str, Path]): file path.

    Returns:
        dict: dictionary
    """

    fp = Path(fp)

    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")

    with open(fp) as f:
        d = json.load(f)

    return d


def save_yaml(obj: Any, fp: Union[str, Path], create_directory: bool = False):
    """save yaml file

    Args:
        obj (Any): Any object that can be converted to yaml format.
        fp (Union[str, Path]): file path.
        create_directory (bool, optional): this determines whether create parent directory or not. Default to False.
    """

    fp = Path(fp)
    if create_directory:
        make_directory(fp.parent)

    with open(fp, "w") as f:
        yaml.safe_dump(obj, f, indent=4, sort_keys=False)


def load_yaml(fp: Union[str, Path]) -> dict:
    """load yaml file

    Args:
        fp (Union[str, Path]): file path.

    Returns:
        dict: dictionary
    """

    fp = Path(fp)

    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exists")

    with open(fp) as f:
        d = yaml.safe_load(f)

    return d


def copy_files_to_directory(
    src: Union[list, str, PurePath],
    dst: Union[str, PurePath],
    recursive: bool = True,
    extension: Union[str, list] = None,
    include_directories: bool = False,
    create_directory: bool = False,
):
    """Copy files to directory

    Args:
        src (Union[list, str, PurePath]): 'file list' or 'file' or 'directory'.
        dst (Union[str, PurePath]): destination directory.
        recursive (bool, optional): copy recursively or not when copying directory. Defaults to True.
        extension (Union[str, list], optional): copy only specific extension(including "."). Defaults to None.
        include_directories (bool, optional): Whether to include directories in the list or not. Defaults to False.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Raises:
        FileNotFoundError: if src is unknown
        ValueError: if dst is not directory format
        FileNotFoundError: if dst is not exists. you can bypass this error with create_directory argument.
    """
    if not isinstance(src, list):
        src = [src]
    src = [Path(src_path).absolute() for src_path in src]

    src_list = []
    for src_path in src:
        if Path(src_path).is_file():
            src_list.append(Path(src_path))
        elif Path(src_path).is_dir():
            src_list.extend(
                search.get_files(
                    src_path,
                    recursive=recursive,
                    extension=extension,
                    include_directories=include_directories,
                )
            )
        else:
            raise FileNotFoundError(f"{src_path} does not exists")

    if len(src_list) == 1:
        src_prefix = src_list[0].parent
    elif len(src_list) > 1:
        src_prefix = Path(os.path.commonpath(src_list))
    else:
        raise FileNotFoundError("src_list is empty")

    dst = Path(dst)

    if dst.exists() and dst.is_file():
        raise ValueError(f"dst should be directory. {dst} is not directory.")

    if create_directory:
        make_directory(dst)

    if not dst.exists():
        raise FileNotFoundError(
            f"{dst} directory does not exist. please set 'create_directory' argument to be True to make directory."
        )

    for src_file in src_list:
        if src_file.is_file():
            dst_file = Path(str(src_file).replace(str(src_prefix), str(dst)))
            make_directory(dst_file.parent)
            shutil.copy(src_file, dst_file)
        elif src_file.is_dir():
            dst_file = Path(str(src_file).replace(str(src_prefix), str(dst)))
            make_directory(dst_file)


def copy_file(
    src: Union[str, Path],
    dst: Union[str, Path],
    create_directory: bool = False,
):
    """Copy file

    Args:
        src (Union[str, Path]): source file path.
        dst (Union[str, Path]): destination file path.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Raises:
    """
    dst = Path(dst)

    if create_directory:
        make_directory(dst.parent)

    shutil.copy(src, dst)


def make_directory(src: Union[str, Path]):
    """Create Directory

    Args:
        src (str): directory
    """
    Path(src).mkdir(mode=0o766, parents=True, exist_ok=True)


def remove_file(src: str):
    """Remove File

    Args:
        src (str): file to remove
    """
    os.remove(src)


def remove_directory(src: Union[str, Path], recursive: bool = False):
    """Remove Directory

    Args:
        src (str): file to remove
        recursive (bool, optional): remove recursively. Defaults to False.
    """
    if not recursive:
        if Path(src).glob("**/*"):
            raise FileExistsError(
                f"{src} is not empty. please set recursive argument to be True to remove directory."
            )
    shutil.rmtree(src)


def move_files_to_directory(
    src: Union[list, str, PurePath],
    dst: Union[str, PurePath],
    recursive: bool = True,
    extension: Union[str, list] = None,
    include_directories: bool = False,
    create_directory: bool = False,
):
    """Move files

    Args:
        src (Union[list, str, PurePath]): 'file list' or 'file' or 'directory' or 'directory list'.
        dst (Union[str, PurePath]): destination directory.
        recursive (bool, optional): move recursively or not when moving directory. Defaults to True.
        extension (Union[str, list], optional): move only specific extension(including "."). Defaults to None.
        include_directories (bool, optional): Whether to include directories in the list or not. Defaults to False.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Raises:
        FileNotFoundError: if src is unknown
        ValueError: if dst is not directory format
        FileNotFoundError: if dst is not exists. you can bypass this error with create_directory argument.
    """
    if not isinstance(src, list):
        src = [src]
    src = [Path(src_path).absolute() for src_path in src]

    src_list = []
    for src_path in src:
        if Path(src_path).is_file():
            src_list.append(Path(src_path))
        elif Path(src_path).is_dir():
            src_list.extend(
                search.get_files(
                    src_path,
                    recursive=recursive,
                    extension=extension,
                    include_directories=include_directories,
                )
            )
        else:
            raise FileNotFoundError(f"{src_path} does not exists")

    if len(src_list) == 1:
        src_prefix = src_list[0].parent
    elif len(src_list) > 1:
        src_prefix = Path(os.path.commonpath(src_list))
    else:
        raise FileNotFoundError("src_list is empty")

    dst = Path(dst)

    if dst.exists() and dst.is_file():
        raise ValueError(f"dst should be directory. {dst} is not directory.")

    if create_directory:
        make_directory(dst)

    if not dst.exists():
        raise FileNotFoundError(
            f"{dst} directory does not exist. please set 'create_directory' argument to be True to make directory."
        )

    for src_file in src_list:
        dst_file = Path(str(src_file).replace(str(src_prefix), str(dst)))
        if src_file.is_file():
            make_directory(dst_file.parent)
            shutil.move(src_file, dst_file)
        elif src_file.is_dir() and not dst_file.exists():
            shutil.move(src_file, dst_file)


def zip(
    src: Union[str, PurePath, list],
    dst: Union[str, PurePath],
    recursive: bool = True,
    extension: Union[str, list] = None,
    create_directory: bool = False,
) -> str:
    """Zip file(s) or directory(s)

    Args:
        src (Union[str, PurePath, list]): file(s) or directory(s)
        dst (str): destination file path
        recursive (bool, optional): zip recursively or not when zipping directory. Defaults to True.
        extension (Union[str, list], optional): zip only specific extension(including "."). Defaults to None.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Returns:
        str: destination file path
    """
    if not isinstance(src, list):
        src = [src]
    src = [Path(src_path).absolute() for src_path in src]

    src_list = []
    for src_path in src:
        if Path(src_path).is_file():
            src_list.append(Path(src_path))
        elif Path(src_path).is_dir():
            src_list.extend(
                search.get_files(
                    src_path, recursive=recursive, extension=extension
                )
            )
        else:
            raise FileNotFoundError(f"{src_path} does not exists")

    if len(src_list) == 1:
        src_prefix = src_list[0].parent
    elif len(src_list) > 1:
        src_prefix = Path(os.path.commonpath(src_list))
    else:
        raise FileNotFoundError("src_list is empty")

    if create_directory:
        make_directory(Path(dst).parent)

    if not Path(dst).parent.exists():
        raise FileNotFoundError(
            f"{dst} directory does not exist. please set 'create_directory' argument to be True to make directory."
        )

    with zipfile.ZipFile(dst, "w") as f:
        for src_file in src_list:
            f.write(
                src_file,
                arcname=str(src_file.relative_to(src_prefix)),
                compress_type=zipfile.ZIP_DEFLATED,
            )

    return str(dst)


def unzip(src: str, dst: str, create_directory: bool = False) -> str:
    """Unzip file

    Args:
        src (str): source file path
        dst (str): destination directory
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Returns:
        str: destination directory
    """

    if create_directory:
        make_directory(dst)

    with zipfile.ZipFile(src, "r") as f:
        f.extractall(dst)

    return str(dst)
