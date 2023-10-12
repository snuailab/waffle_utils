import json
import os
import shutil
import zipfile
from pathlib import Path, PurePath
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
    recursive: bool = True,
    exts: Union[str, list] = None,
):
    """Copy files to directory

    Args:
        src (Union[list, str, Path]): 'file list' or 'file' or 'directory'.
        dst (Union[str, Path]): destination directory.
        create_directory (bool, optional): create destination directory or not. Defaults to False.
        recursive (bool, optional): copy recursively or not when copying directory. Defaults to True.
        exts (Union[str, list], optional): copy only specific extension(including "."). Defaults to None.

    Raises:
        FileNotFoundError: if src is unknown
        ValueError: if dst is not directory format
        FileNotFoundError: if dst is not exists. you can bypass this error with create_directory argument.
    """

    src_list = None
    if isinstance(src, list):
        src_prefix = os.path.commonpath(src)
        src_list = list(map(Path, src))
    elif isinstance(src, (str, PurePath)):
        src = Path(src)
        if src.is_file():
            src_list = [src]
            src_prefix = src.parent
        elif src.is_dir():
            src_list = list(src.glob("**/*" if recursive else "*"))
            if exts:
                if isinstance(exts, str):
                    exts = [exts]
                src_list = list(filter(lambda x: x.suffix in exts, src_list))
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


def zip(
    src: Union[str, PurePath, list], dst: str, create_directory: bool = False
) -> str:
    """Zip file(s) or directory(s)

    Args:
        src (Union[str, PurePath, list]): file(s) or directory(s)
        dst (str): destination file path
        create_directory (bool, optional): create destination directory or not. Defaults to False.

    Returns:
        str: destination file path
    """

    def parse_path(src: Union[str, PurePath]) -> tuple[Path, list]:
        if Path(src).is_file():
            base_dir = Path(src).parent
            file_list = [Path(src)]
        elif Path(src).is_dir():
            base_dir = Path(src)
            file_list = list(Path(src).glob("**/*"))
        else:
            raise FileNotFoundError(f"{src} does not exists")
        return base_dir, file_list

    if isinstance(src, (str, PurePath)):
        base_dir, file_list = parse_path(src)
    elif isinstance(src, list):
        src = list(map(lambda x: Path(x).absolute(), src))
        base_dir = Path(os.path.commonpath(src))
        file_list = []
        for file_path in src:
            _, _file_list = parse_path(file_path)
            file_list.extend(_file_list)

    if create_directory:
        make_directory(Path(dst).parent)

    with zipfile.ZipFile(dst, "w") as f:
        for file_path in file_list:
            arcname = str(file_path.relative_to(base_dir))
            f.write(
                file_path,
                arcname=arcname,
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
