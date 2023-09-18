import os

from waffle_utils.file import io, network


def test_io():
    dummy_data = {"dummy": "hi"}
    dummy_json = os.path.join("tmp", "a.json")
    dummy_yaml = os.path.join("tmp", "a.yaml")

    dummy_src = "tmp"
    dummy_dst = "tmp_copy"

    io.save_json(dummy_data, dummy_json, create_directory=True)
    io.save_yaml(dummy_data, dummy_yaml, create_directory=True)
    assert io.load_json(dummy_json) == io.load_yaml(dummy_yaml)

    io.copy_files_to_directory(dummy_src, dummy_dst, create_directory=True)

    # zip file Test
    dummy_zip_dir = "tmp_zip"
    dummy_zip_name = "tmp.waffle"
    io.zip([dummy_src, dummy_dst, dummy_yaml], dummy_zip_name)
    assert os.path.exists(dummy_zip_name), "Error: zip func"

    io.unzip(dummy_zip_name, dummy_zip_dir, create_directory=True)
    assert os.path.exists(dummy_zip_dir), "Error: unzip dir is not found"
    assert (
        io.load_yaml(os.path.join(dummy_zip_dir, "a.yaml")) == dummy_data
    ), "Error: unzip file is not same"
    assert (
        io.load_yaml(os.path.join(dummy_zip_dir, dummy_yaml)) == dummy_data
    ), "Error: unzip file in directory is not same"

    io.remove_file(dummy_json)
    io.remove_file(dummy_zip_name)
    assert not os.path.exists(dummy_json), "Error: remove_file func"
    assert not os.path.exists(dummy_zip_name), "Error: remove_file func"

    io.remove_directory(dummy_src)
    io.remove_directory(dummy_dst)
    assert not (
        os.path.exists(dummy_src) and os.path.exists(dummy_dst)
    ), "Error: remove_directory func"
