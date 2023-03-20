from pathlib import Path

from waffle_utils.run import (
    _get_file_from_url,
    _unzip,
    _from_coco,
    _split_train_val,
    _export,
    _extract_frames,
    _create_video,
)


def test_get_file_from_url(tmpdir: Path):

    url = "https://github.com/snuailab/waffle_utils/raw/main/mnist.zip"
    file_path = tmpdir / "mnist.zip"
    create_directory = True

    _get_file_from_url(url, str(file_path), create_directory)

    # TODO: Add assert


def test_unzip(tmpdir: Path):
    raise NotImplementedError("Not implemented yet.")


def test_from_coco(tmpdir: Path):
    raise NotImplementedError("Not implemented yet.")


def test_split_train_val(tmpdir: Path):
    raise NotImplementedError("Not implemented yet.")


def test_export(tmpdir: Path):
    raise NotImplementedError("Not implemented yet.")


def test_extract_frames(tmpdir: Path):
    raise NotImplementedError("Not implemented yet.")


def test_create_video(tmpdir: Path):
    raise NotImplementedError("Not implemented yet.")
