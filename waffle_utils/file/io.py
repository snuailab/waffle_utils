import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, Union

import yaml


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
    src: Union[list, str, Path],
    dst: Union[str, Path],
    create_directory: bool = False,
):
    """Copy files to directory

    Args:
        src (Union[list, str, Path]): 'file list' or 'file' or 'directory'.
        dst (Union[str, Path]): destination directory.
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Raises:
        FileNotFoundError: if src is unknown
        ValueError: if dst is not directory format
        FileNotFoundError: if dst is not exists. you can bypass this error with create_directory argument.
    """

    src_list = None
    if isinstance(src, list):
        src_prefix = os.path.commonpath(src)
        src_list = list(map(Path, src))
    elif isinstance(src, str) or isinstance(src, Path):
        src = Path(src)
        if src.is_file():
            src = Path(src)
            src_list = [src]
            src_prefix = src.parent
        elif src.is_dir():
            src = Path(src)
            src_list = src.glob("**/*")
            src_prefix = src

    if src_list is None:
        raise FileNotFoundError(f"unknown source {src}")

    dst = Path(dst)
    if dst.suffix != "":
        raise ValueError(
            f"dst should be directory format. but got {dst.suffix}"
        )
    elif create_directory:
        make_directory(dst)

    if not dst.exists():
        raise FileNotFoundError(
            f"{dst} directory does not exist. please set 'create_directory' argument to be True to make directory."
        )

    for src_file in src_list:
        dst_file = Path(str(src_file).replace(str(src_prefix), str(dst)))
        make_directory(dst_file.parent)
        if src_file.is_file():
            shutil.copy(src_file, dst_file)


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


def remove_directory(src: Union[str, Path]):
    """Remove Directory

    Args:
        src (str): file to remove
    """
    shutil.rmtree(str(src))


def unzip(src: str, dst: str, create_directory: bool = False):

    if create_directory:
        make_directory(dst)

    with zipfile.ZipFile(src, "r") as f:
        f.extractall(dst)


def zip(src: Union[str, list], dst: str):
    file_list = [src] if isinstance(src, str) else src
    try:
        with zipfile.ZipFile(dst, "w") as f:
            for file_path in file_list:
                if os.path.isdir(file_path):
                    for path, dir, files in os.walk(file_path):
                        for file in files:
                            arcname = os.path.join(
                                os.path.relpath(
                                    path, os.path.dirname(file_path)
                                ),
                                file,
                            )
                            f.write(
                                os.path.join(path, file),
                                arcname=arcname,
                                compress_type=zipfile.ZIP_DEFLATED,
                            )
                else:
                    f.write(
                        file_path,
                        arcname=os.path.basename(file_path),
                        compress_type=zipfile.ZIP_DEFLATED,
                    )
    except Exception as e:
        if os.path.exists(dst):
            remove_file(dst)
        raise e
