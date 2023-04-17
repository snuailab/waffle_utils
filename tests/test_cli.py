import subprocess
from pathlib import Path

import pytest

from waffle_utils.file.io import remove_directory
from waffle_utils.image import DEFAULT_IMAGE_EXTENSION
from waffle_utils.video import DEFAULT_VIDEO_EXTENSION


def run(cmd):
    # Run a subprocess command with check=True
    subprocess.run(cmd.split(), check=True)


@pytest.fixture(scope="module")
def tmp_path_module():
    # Create a temporary directory
    tmp_path = Path("tmp_tests")

    # Yield the temporary directory to the test function
    yield tmp_path

    # Clean up the temporary directory after the test run
    remove_directory(tmp_path)


# Define fixtures for temporary paths and variables
@pytest.fixture(scope="module")
def zip_file(tmp_path_module):
    return tmp_path_module / "mnist.zip"


@pytest.fixture(scope="module")
def extract_dir(tmp_path_module):
    return tmp_path_module / "tmp/extract"


@pytest.fixture(scope="module")
def coco_root_dir(extract_dir):
    return extract_dir / "images"


@pytest.fixture(scope="module")
def coco_file(extract_dir):
    return extract_dir / "coco.json"


# Define tests for dataset-related functions
def test_get_file_from_url(zip_file):
    run(
        f"python -m waffle_utils.run get_file_from_url --url https://raw.githubusercontent.com/snuailab/assets/main/waffle/sample_dataset/mnist.zip --file-path {zip_file}"
    )


def test_unzip(zip_file, extract_dir):
    run(
        f"python -m waffle_utils.run unzip --file-path {zip_file} --output-dir {extract_dir}"
    )


# Define fixtures and tests for video-related functions
@pytest.fixture(scope="module")
def input_path():
    return Path("tests/video/test.mp4")


@pytest.fixture(scope="module")
def output_dir(tmp_path_module):
    return tmp_path_module / "test_frames"


@pytest.fixture(scope="module")
def input_dir(output_dir):
    return output_dir


@pytest.fixture(scope="module")
def output_path(tmp_path_module):
    return tmp_path_module / f"test.{DEFAULT_VIDEO_EXTENSION}"


# Define tests for video-related functions
def test_extract_frames(input_path, output_dir):
    run(
        f"python -m waffle_utils.run extract_frames --input-path {input_path} --output-dir {output_dir} --num-of-frames 3 --interval-second 3 --output-image-extension {DEFAULT_IMAGE_EXTENSION}"
    )


def test_create_video(input_dir, output_path):
    run(
        f"python -m waffle_utils.run create_video --input-dir {input_dir} --output-path {output_path} --frame-rate 30"
    )
