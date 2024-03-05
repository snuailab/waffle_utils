import shutil
import zipfile
from pathlib import Path

import pytest

from waffle_utils.file import io


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
    assert len(dummy_directory["file_tree"][1]) == len(list(dst.glob("**/*")))

    # copy with recursive
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test4")

    io.copy_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert dummy_directory["file_num"] == len(
        list(filter(lambda x: x.is_file(), dst.glob("**/*")))
    )

    # copy with exts
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test5")

    io.copy_files_to_directory(
        src, dst, create_directory=True, recursive=False, extension=".txt"
    )
    assert len(list(filter(lambda x: x.is_file(), dst.glob("**/*")))) == len(
        list(
            filter(
                lambda x: x.suffix == ".txt", dummy_directory["file_tree"][1]
            )
        )
    )

    io.copy_files_to_directory(
        src, dst, create_directory=True, recursive=True, extension=".txt"
    )
    assert len(list(filter(lambda x: x.is_file(), dst.glob("**/*")))) == len(
        list(
            filter(lambda x: x.suffix == ".txt", dummy_directory["file_list"])
        )
    )

    # copy file with including root directory
    src = dummy_directory["file_tree"][1][0]
    dst1 = Path(tmpdir, "test6-1")
    io.copy_files_to_directory(
        src, dst1, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst1.glob("**/*")))) == 1
    src = dummy_directory_clone["file_tree"][3][0]
    dst2 = Path(tmpdir, "test6-2")
    io.copy_files_to_directory(
        src, dst2, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst2.glob("**/*")))) == 1
    assert sorted([p.relative_to(dst1) for p in dst1.glob("**/*")]) == sorted(
        [p.relative_to(dst2) for p in dst2.glob("**/*")]
    )

    # copy files with including root directory
    src = dummy_directory["file_tree"][1]
    dst1 = Path(tmpdir, "test7-1")
    io.copy_files_to_directory(
        src, dst1, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst1.glob("**/*")))) == len(
        src
    )
    src = dummy_directory["file_tree"][3]
    dst2 = Path(tmpdir, "test7-2")
    io.copy_files_to_directory(
        src, dst2, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst2.glob("**/*")))) == len(
        src
    )
    assert sorted([p.relative_to(dst1) for p in dst1.glob("**/*")]) == sorted(
        [p.relative_to(dst2) for p in dst2.glob("**/*")]
    )

    src = dummy_directory["file_tree"][1] + dummy_directory["file_tree"][2]
    dst3 = Path(tmpdir, "test7-3")
    io.copy_files_to_directory(
        src, dst3, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst3.glob("**/*")))) == len(
        src
    )
    src = dummy_directory["file_tree"][1] + dummy_directory["file_tree"][3]
    dst4 = Path(tmpdir, "test7-4")
    io.copy_files_to_directory(
        src, dst4, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst4.glob("**/*")))) == len(
        src
    )
    assert sorted([p.relative_to(dst3) for p in dst3.glob("**/*")]) != sorted(
        [p.relative_to(dst4) for p in dst4.glob("**/*")]
    )  # different root directory
    assert (
        len(
            set(
                [p.relative_to(dst3) for p in dst3.glob("**/*") if p.is_file()]
                + [
                    p.relative_to(dst4)
                    for p in dst4.glob("**/*")
                    if p.is_file()
                ]
            )
        )
        == dummy_directory["file_num"]
    )  # no duplicate

    # copy directory to directory without including root directory
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test8")
    io.copy_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy_directory["file_num"]
    )
    assert sorted(
        [p.relative_to(dst) for p in dst.glob("**/*") if p.is_file()]
    ) == sorted(dummy_directory["file_relative_path_list"])

    # copy directory to directory with including root directory
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test9")
    io.copy_files_to_directory(
        src,
        dst,
        create_directory=True,
        recursive=True,
        include_root_directory=True,
    )
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy_directory["file_num"]
    )
    assert sorted(
        [p.relative_to(dst) for p in dst.glob("**/*") if p.is_file()]
    ) == sorted(
        [
            Path(dummy_directory["path"].stem) / rel_p
            for rel_p in dummy_directory["file_relative_path_list"]
        ]
    )

    # copy files and directory to directory
    src = dummy_directory["file_list"] + [dummy_directory_clone["path"]]
    dst = Path(tmpdir, "test10")
    io.copy_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy_directory["file_num"]
    )
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy_directory_clone["file_num"]
    )

    # copy files and directory to directory with including root directory
    src = dummy_directory["file_list"] + [dummy_directory_clone["path"]]
    dst = Path(tmpdir, "test11")
    io.copy_files_to_directory(
        src,
        dst,
        create_directory=True,
        recursive=True,
        include_root_directory=True,
    )
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy_directory["file_num"] + dummy_directory_clone["file_num"]
    )

    # copy including directories
    src = dummy_directory["path"]
    dst = Path(tmpdir, "test12")
    io.copy_files_to_directory(
        src,
        dst,
        create_directory=True,
        recursive=True,
        include_directories=True,
    )
    assert (
        len(list(filter(lambda x: x.is_dir(), dst.glob("**/*"))))
        == dummy_directory["dir_num"]
    )


def test_copy_file(dummy_text, tmpdir):
    src = dummy_text["path"]
    dst = Path(tmpdir, "test.txt")

    io.copy_file(src, dst)
    assert dst.exists()

    dst = Path(tmpdir, "sub", "test.txt")
    io.copy_file(src, dst, create_directory=True)
    assert dst.exists()


def test_move_files(dummy_directory, tmpdir):
    def dummy_factory(dst):
        Path(dst).mkdir(exist_ok=True)
        shutil.copytree(dummy_directory["path"], dst, dirs_exist_ok=True)
        return {
            "path": dst,
            "file_list": list(
                map(
                    lambda x: Path(dst, x),
                    dummy_directory["file_relative_path_list"],
                )
            ),
            "file_relative_path_list": dummy_directory[
                "file_relative_path_list"
            ],
            "file_num": dummy_directory["file_num"],
            "file_tree": {
                k: list(
                    map(
                        lambda x: Path(
                            str(x).replace(
                                str(dummy_directory["path"]), str(dst)
                            )
                        ),
                        v,
                    )
                )
                for k, v in dummy_directory["file_tree"].items()
            },
            "dir_list": list(
                map(
                    lambda x: Path(dst, x),
                    dummy_directory["dir_relative_path_list"],
                )
            ),
            "dir_relative_path_list": dummy_directory[
                "dir_relative_path_list"
            ],
            "dir_num": dummy_directory["dir_num"],
            "directory_tree": {
                k: list(
                    map(
                        lambda x: Path(
                            str(x).replace(
                                str(dummy_directory["path"]), str(dst)
                            )
                        ),
                        v,
                    )
                )
                for k, v in dummy_directory["directory_tree"].items()
            },
        }

    # move directory without create_directory
    src = dummy_factory(Path(tmpdir, "src1"))
    dst = Path(tmpdir, "test1")

    with pytest.raises(FileNotFoundError):
        io.move_files_to_directory(src["path"], dst)
    assert not dst.exists()

    # move file to directory
    src = dummy_factory(Path(tmpdir, "src2"))
    dst = Path(tmpdir, "test2")

    io.move_files_to_directory(src["file_list"][0], dst, create_directory=True)
    assert len(list(dst.glob("**/*"))) == 1

    # move without recursive
    src = dummy_factory(Path(tmpdir, "src3"))
    dst = Path(tmpdir, "test3")

    io.move_files_to_directory(
        src["path"], dst, create_directory=True, recursive=False
    )
    assert len(src["file_tree"][1]) == len(list(dst.glob("**/*")))

    # move with recursive
    src = dummy_factory(Path(tmpdir, "src4"))
    dst = Path(tmpdir, "test4")

    io.move_files_to_directory(
        src["path"], dst, create_directory=True, recursive=True
    )
    assert src["file_num"] == len(
        list(filter(lambda x: x.is_file(), dst.glob("**/*")))
    )

    # move with exts
    src = dummy_factory(Path(tmpdir, "src5"))
    dst = Path(tmpdir, "test5")

    io.move_files_to_directory(
        src["path"],
        dst,
        create_directory=True,
        recursive=False,
        extension=".txt",
    )
    assert len(list(filter(lambda x: x.is_file(), dst.glob("**/*")))) == len(
        list(filter(lambda x: x.suffix == ".txt", src["file_tree"][1]))
    )

    src = dummy_factory(Path(tmpdir, "src6"))
    dst = Path(tmpdir, "test6")
    io.move_files_to_directory(
        src["path"],
        dst,
        create_directory=True,
        recursive=True,
        extension=".txt",
    )
    assert len(list(filter(lambda x: x.is_file(), dst.glob("**/*")))) == len(
        list(filter(lambda x: x.suffix == ".txt", src["file_list"]))
    )

    # move file with including root directory
    src = dummy_factory(Path(tmpdir, "src7-1"))["file_tree"][1][0]
    dst1 = Path(tmpdir, "test7-1")
    io.move_files_to_directory(
        src, dst1, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst1.glob("**/*")))) == 1
    src = dummy_factory(Path(tmpdir, "src7-2"))["file_tree"][3][0]
    dst2 = Path(tmpdir, "test7-2")
    io.move_files_to_directory(
        src, dst2, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst2.glob("**/*")))) == 1
    assert sorted([p.relative_to(dst1) for p in dst1.glob("**/*")]) == sorted(
        [p.relative_to(dst2) for p in dst2.glob("**/*")]
    )

    # move files with including root directory
    src = dummy_factory(Path(tmpdir, "src8-1"))["file_tree"][1]
    dst1 = Path(tmpdir, "test8-1")
    io.move_files_to_directory(
        src, dst1, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst1.glob("**/*")))) == len(
        src
    )
    src = dummy_factory(Path(tmpdir, "src8-2"))["file_tree"][3]
    dst2 = Path(tmpdir, "test8-2")
    io.move_files_to_directory(
        src, dst2, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst2.glob("**/*")))) == len(
        src
    )
    assert sorted([p.relative_to(dst1) for p in dst1.glob("**/*")]) == sorted(
        [p.relative_to(dst2) for p in dst2.glob("**/*")]
    )

    dummy = dummy_factory(Path(tmpdir, "src8-3"))
    src = dummy["file_tree"][1] + dummy["file_tree"][2]
    dst3 = Path(tmpdir, "test8-3")
    io.move_files_to_directory(
        src, dst3, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst3.glob("**/*")))) == len(
        src
    )
    dummy = dummy_factory(Path(tmpdir, "src8-4"))
    src = dummy["file_tree"][1] + dummy["file_tree"][3]
    dst4 = Path(tmpdir, "test8-4")
    io.move_files_to_directory(
        src, dst4, create_directory=True, include_root_directory=True
    )
    assert len(list(filter(lambda x: x.is_file(), dst4.glob("**/*")))) == len(
        src
    )
    assert sorted([p.relative_to(dst3) for p in dst3.glob("**/*")]) != sorted(
        [p.relative_to(dst4) for p in dst4.glob("**/*")]
    )  # different root directory
    assert (
        len(
            set(
                [p.relative_to(dst3) for p in dst3.glob("**/*") if p.is_file()]
                + [
                    p.relative_to(dst4)
                    for p in dst4.glob("**/*")
                    if p.is_file()
                ]
            )
        )
        == dummy["file_num"]
    )  # no duplicate

    # move directory to directory without including root directory
    dummy = dummy_factory(Path(tmpdir, "src9"))
    src = dummy["path"]
    dst = Path(tmpdir, "test9")
    io.move_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy["file_num"]
    )
    assert sorted(
        [p.relative_to(dst) for p in dst.glob("**/*") if p.is_file()]
    ) == sorted(dummy["file_relative_path_list"])

    # move directory to directory with including root directory
    dummy = dummy_factory(Path(tmpdir, "src10"))
    src = dummy["path"]
    dst = Path(tmpdir, "test10")
    io.move_files_to_directory(
        src,
        dst,
        create_directory=True,
        recursive=True,
        include_root_directory=True,
    )
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy["file_num"]
    )
    assert sorted(
        [p.relative_to(dst) for p in dst.glob("**/*") if p.is_file()]
    ) == sorted(
        [
            Path(dummy["path"].stem) / rel_p
            for rel_p in dummy["file_relative_path_list"]
        ]
    )

    # move files and directory to directory
    dummy1 = dummy_factory(Path(tmpdir, "src11-1"))
    dummy2 = dummy_factory(Path(tmpdir, "src11-2"))
    src = dummy1["file_list"] + [dummy2["path"]]
    dst = Path(tmpdir, "test11")
    io.move_files_to_directory(src, dst, create_directory=True, recursive=True)
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy1["file_num"]
    )
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy2["file_num"]
    )

    # move files and directory to directory with including root directory
    dummy1 = dummy_factory(Path(tmpdir, "src12-1"))
    dummy2 = dummy_factory(Path(tmpdir, "src12-2"))
    src = dummy1["file_list"] + [dummy2["path"]]
    dst = Path(tmpdir, "test12")
    io.move_files_to_directory(
        src,
        dst,
        create_directory=True,
        recursive=True,
        include_root_directory=True,
    )
    assert (
        len(list(filter(lambda x: x.is_file(), dst.glob("**/*"))))
        == dummy1["file_num"] + dummy2["file_num"]
    )

    # move including directories
    src = dummy_factory(Path(tmpdir, "src13"))
    dst = Path(tmpdir, "test13")

    io.move_files_to_directory(
        src["path"],
        dst,
        create_directory=True,
        recursive=True,
        include_directories=True,
    )
    assert (
        len(list(filter(lambda x: x.is_dir(), dst.glob("**/*"))))
        == src["dir_num"]
    )


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
