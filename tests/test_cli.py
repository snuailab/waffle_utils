import subprocess
from pathlib import Path

TMP_DIR = Path(tmpdir)  # TODO: Get `tmpdir` using a related library
ZIP_FILE = TMP_DIR / "mnist.zip"
DATA_ROOT_DIR = TMP_DIR / "tmp/dataset"
DATASET_NAME = "mnist"

EXTRACT_DIR = TMP_DIR / "tmp/extract"
COCO_ROOT_DIR = TMP_DIR / "tmp/extract/raw"
COCO_FILE = TMP_DIR / "tmp/extract/exports/coco.json"


def run(cmd):
    # Run a subprocess command with check=True
    subprocess.run(cmd.split(), check=True)


def test_get_file_from_url():
    run(
        f"python -m waffle_utils.run get_file_from_url --url https://github.com/snuailab/waffle_utils/raw/main/mnist.zip --file-path {ZIP_FILE}"
    )


def test_unzip():
    run(
        f"python -m waffle_utils.run unzip --file-path {ZIP_FILE} --output-dir {EXTRACT_DIR}"
    )


def test_from_coco():
    run(
        f"python -m waffle_utils.run from_coco --name {DATASET_NAME} --root-dir {COCO_FILE} --coco_file {COCO_ROOT_DIR} --coco-root-dir {DATA_ROOT_DIR}"
    )


def test_split_train_val():
    # run(f"python -m waffle_utils.run split_train_val")  # TODO: Full CLI


def test_export():
    # run(f"python -m waffle_utils.run export")  # TODO: Full CLI


def test_extract_frames():
    # run(f"python -m waffle_utils.run extract_frames")  # TODO: Full CLI


def test_create_video():
    # run(f"python -m waffle_utils.run create_video")  # TODO: Full CLI
