from waffle_utils.file import network


def test_get_file_from_url(tmpdir):
    url = "https://github.com/snuailab/assets/blob/main/waffle/icons/waffle.png?raw=true"
    file_path = tmpdir / "waffle.png"
    network.get_file_from_url(url, file_path)
    assert file_path.exists()

    file_path = tmpdir / "waffle" / "waffle.png"
    network.get_file_from_url(url, file_path, create_directory=True)
    assert file_path.exists()
