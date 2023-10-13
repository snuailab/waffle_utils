import json
import shutil
import zipfile
from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="session")
def dummy_empty_directory(tmpdir_factory):
    directory = Path(tmpdir_factory.mktemp("dummy_empty_directory"))
    Path(directory).mkdir(exist_ok=True)

    return {"path": directory}


@pytest.fixture(scope="session")
def dummy_text(tmpdir_factory):
    directory = Path(tmpdir_factory.mktemp("dummy_text_file"))
    dummy_file = Path(directory) / "dummy_text_file.txt"
    data = "dummy_text_file"
    with open(dummy_file, "w") as f:
        f.write(data)

    return {"path": dummy_file, "data": data}


@pytest.fixture(scope="session")
def dummy_json(tmpdir_factory):
    directory = Path(tmpdir_factory.mktemp("dummy_json_file"))
    dummy_file = Path(directory) / "dummy_json_file.json"
    data = {"dummy_json_file": "dummy_json_file"}
    with open(dummy_file, "w") as f:
        json.dump(data, f)

    return {"path": dummy_file, "data": data}


@pytest.fixture(scope="session")
def dummy_yaml(tmpdir_factory):
    directory = Path(tmpdir_factory.mktemp("dummy_yaml_file"))
    dummy_file = Path(directory) / "dummy_yaml_file.yaml"
    data = {"dummy_json_file": "dummy_json_file"}
    with open(dummy_file, "w") as f:
        yaml.dump(data, f)

    return {"path": dummy_file, "data": data}


@pytest.fixture(scope="session")
def dummy_image(tmpdir_factory):
    directory = Path(tmpdir_factory.mktemp("dummy_image_file"))
    dummy_file = Path(directory) / "dummy_image_file.png"
    dummy_file.touch()

    return {"path": dummy_file, "data": ""}


@pytest.fixture(scope="session")
def dummy_video(tmpdir_factory):
    directory = Path(tmpdir_factory.mktemp("dummy_video_file"))
    dummy_file = Path(directory) / "dummy_video_file.mp4"
    dummy_file.touch()

    return {"path": dummy_file, "data": ""}


@pytest.fixture(scope="session")
def dummy_file_list(
    dummy_text, dummy_json, dummy_yaml, dummy_image, dummy_video
):
    return [
        dummy_text["path"],
        dummy_json["path"],
        dummy_yaml["path"],
        dummy_image["path"],
        dummy_video["path"],
    ]


@pytest.fixture(scope="session")
def dummy_directory(tmpdir_factory, dummy_file_list):
    directory = Path(tmpdir_factory.mktemp("dummy_directory"))

    new_dummy_file_list_level1 = []
    for file_path in dummy_file_list:
        shutil.copy(file_path, directory)
        new_dummy_file_list_level1.append(
            Path(directory) / Path(file_path).name
        )

    sub_directory = Path(directory) / "sub"
    sub_directory.mkdir(exist_ok=True)
    new_dummy_file_list_level2 = []
    for file_path in dummy_file_list:
        shutil.copy(file_path, sub_directory)
        new_dummy_file_list_level2.append(
            Path(sub_directory) / Path(file_path).name
        )

    new_dummy_file_list = (
        new_dummy_file_list_level1 + new_dummy_file_list_level2
    )

    return {
        "path": directory,
        "file_list": new_dummy_file_list,
        "file_relative_path_list": [
            file.relative_to(directory) for file in new_dummy_file_list
        ],
        "length": len(new_dummy_file_list),
        "tree": {1: new_dummy_file_list_level1, 2: new_dummy_file_list_level2},
    }


@pytest.fixture(scope="session")
def dummy_directory_clone(tmpdir_factory, dummy_file_list):
    directory = Path(tmpdir_factory.mktemp("dummy_directory"))

    new_dummy_file_list_level1 = []
    for file_path in dummy_file_list:
        shutil.copy(file_path, directory)
        new_dummy_file_list_level1.append(
            Path(directory) / Path(file_path).name
        )

    sub_directory = Path(directory) / "sub"
    sub_directory.mkdir(exist_ok=True)
    new_dummy_file_list_level2 = []
    for file_path in dummy_file_list:
        shutil.copy(file_path, sub_directory)
        new_dummy_file_list_level2.append(
            Path(sub_directory) / Path(file_path).name
        )

    new_dummy_file_list = (
        new_dummy_file_list_level1 + new_dummy_file_list_level2
    )

    return {
        "path": directory,
        "file_list": new_dummy_file_list,
        "file_relative_path_list": [
            file.relative_to(directory) for file in new_dummy_file_list
        ],
        "length": len(new_dummy_file_list),
        "tree": {1: new_dummy_file_list_level1, 2: new_dummy_file_list_level2},
    }


@pytest.fixture(scope="session")
def dummy_zip(tmpdir_factory, dummy_directory):
    directory = Path(tmpdir_factory.mktemp("dummy_zip_file"))
    zip_file = Path(directory) / "dummy_zip_file.zip"

    with zipfile.ZipFile(zip_file, "w") as f:
        for file_path in dummy_directory["file_list"]:
            f.write(
                file_path,
                arcname=file_path.relative_to(dummy_directory["path"]),
            )

    return {
        "path": zip_file,
        "file_list": dummy_directory["file_list"],
        "file_relative_path_list": dummy_directory["file_relative_path_list"],
        "length": dummy_directory["length"],
        "tree": dummy_directory["tree"],
    }
