from waffle_utils.file import io


def test_io():
    dummy_data = {"dummy": "hi"}
    dummy_json = "tmp/a.json"
    dummy_yaml = "tmp/a.yaml"

    dummy_src = "tmp"
    dummy_dst = "tmp_copy"

    io.save_json(dummy_data, dummy_json, create_directory=True)
    io.save_yaml(dummy_data, dummy_yaml, create_directory=True)
    assert io.load_json(dummy_json) == io.load_yaml(dummy_yaml)

    io.copy_files_to_directory(dummy_src, dummy_dst, create_directory=True)

    io.remove_file(dummy_json)

    io.remove_directory(dummy_src)
    io.remove_directory(dummy_dst)
