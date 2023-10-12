import zipfile
from pathlib import Path

import pytest

from waffle_utils.file import io, network


def test_save_json(dummy_json, tmpdir):
    data = dummy_json["data"]
    fp = Path(tmpdir, "test.json")
    io.save_json(data, fp)
    assert Path(fp).exists()

    fp = Path(tmpdir, "sub", "test.json")
    io.save_json(data, fp, create_directory=True)
    assert Path(fp).exists()


def test_load_json(
    dummy_json,
):
    fp = dummy_json["path"]
    data = dummy_json["data"]
    assert io.load_json(fp) == data


def test_save_yaml(dummy_yaml, tmpdir):
    data = dummy_yaml["data"]
    fp = Path(tmpdir, "test.yaml")
    io.save_yaml(data, fp)
    assert Path(fp).exists()

    fp = Path(tmpdir, "sub", "test.yaml")
    io.save_yaml(data, fp, create_directory=True)
    assert Path(fp).exists()


def test_load_yaml(
    dummy_yaml,
):
    fp = dummy_yaml["path"]
    data = dummy_yaml["data"]
    assert io.load_yaml(fp) == data


def test_copy_files_to_directory(
    dummy_directory, dummy_directory_clone, tmpdir
):
    # copy directory without create_directory
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test1")

    with pytest.raises(FileNotFoundError):
        io.copy_files_to_directory(src, dst)
    assert not dst.exists()

    # copy file to directory
    src = dummy_directory["file_list"][0]
    dst = Path(tmpdir, "test2")

    io.copy_files_to_directory(src, dst, create_directory=True)
    assert len(list(dst.glob("**/*"))) == 1

    # copy without recursive
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test3")

    io.copy_files_to_directory(
        src, dst, create_directory=True, recursive=False
    )
    assert len(dummy_directory["tree"][1]) == len(list(dst.glob("**/*")))

    # copy with recursive
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test4")

    io.copy_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert dummy_directory["length"] == len(
        list(filter(lambda x: x.is_file(), dst.glob("**/*")))
    )

    # copy with exts
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test5")

    io.copy_files_to_directory(
        src, dst, create_directory=True, recursive=False, extension=".txt"
    )
    assert len(list(filter(lambda x: x.is_file(), dst.glob("**/*")))) == 1

    io.copy_files_to_directory(
        src, dst, create_directory=True, recursive=True, extension=".txt"
    )
    assert len(list(filter(lambda x: x.is_file(), dst.glob("**/*")))) == 2

    # copy file and directory to directory
    src = dummy_directory["file_list"] + [dummy_directory_clone["path"]]
    dst = Path(tmpdir, "test6")

    io.copy_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy_directory["length"] + dummy_directory_clone["length"]
    )


def test_copy_file(dummy_text, tmpdir):
    src = dummy_text["path"]
    dst = Path(tmpdir, "test.txt")

    io.copy_file(src, dst)
    assert dst.exists()

    dst = Path(tmpdir, "sub", "test.txt")
    io.copy_file(src, dst, create_directory=True)
    assert dst.exists()


def test_make_directory(tmpdir):
    directory = Path(tmpdir, "test")
    io.make_directory(directory)
    assert directory.exists()

    directory = Path(tmpdir, "sub", "test")
    io.make_directory(directory)
    assert directory.exists()


def test_remove_file(tmpdir):
    fp = Path(tmpdir, "test.txt")
    fp.touch()
    io.remove_file(fp)
    assert not fp.exists()

    fp = Path(tmpdir, "sub", "test.txt")
    fp.parent.mkdir()
    fp.touch()
    io.remove_file(fp)
    assert not fp.exists()


def test_remove_directory(tmpdir):
    directory = Path(tmpdir, "test")
    directory.mkdir()
    Path(directory, "test.txt").touch()
    with pytest.raises(FileExistsError):
        io.remove_directory(directory)

    io.remove_directory(directory, recursive=True)
    assert not directory.exists()


def test_zip(dummy_directory, dummy_directory_clone, tmpdir):
    # test zip directory
    directory = dummy_directory["path"]
    fp = Path(tmpdir, "dummy1.zip")
    io.zip(directory, fp, create_directory=True)
    assert fp.exists()

    # check zip file
    extract_dir = Path(tmpdir, "extracted1")
    extract_dir.mkdir()
    with zipfile.ZipFile(fp, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    for file in dummy_directory["file_relative_path_list"]:
        assert Path(extract_dir, file).exists()

    # test zip files
    files = dummy_directory["file_list"]
    fp = Path(tmpdir, "dummy2.zip")
    io.zip(files, fp, create_directory=True)
    assert fp.exists()

    # check zip file
    extract_dir = Path(tmpdir, "extracted2")
    extract_dir.mkdir()
    with zipfile.ZipFile(fp, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    for file in dummy_directory["file_relative_path_list"]:
        assert Path(extract_dir, file).exists()

    # test file and directory
    files = dummy_directory["file_list"] + [dummy_directory_clone["path"]]
    fp = Path(tmpdir, "dummy3.zip")
    io.zip(files, fp, create_directory=True)
    assert fp.exists()

    # check zip file
    extract_dir = Path(tmpdir, "extracted3")
    extract_dir.mkdir()
    with zipfile.ZipFile(fp, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    for file in dummy_directory["file_relative_path_list"]:
        assert Path(
            extract_dir, dummy_directory["path"].name, file
        ).exists(), file
    for file in dummy_directory_clone["file_relative_path_list"]:
        assert Path(
            extract_dir, dummy_directory_clone["path"].name, file
        ).exists(), file


def test_unzip(dummy_zip, tmpdir):
    directory = Path(tmpdir, "dummy_files")
    io.unzip(dummy_zip["path"], directory, create_directory=True)

    for file in dummy_zip["file_relative_path_list"]:
        assert Path(directory, file).exists(), file
