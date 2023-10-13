from waffle_utils.file import search


def test_get_files(
    dummy_directory,
):
    files = search.get_files(dummy_directory["path"])
    assert len(files) == dummy_directory["length"]

    files = search.get_files(dummy_directory["path"], recursive=False)
    assert len(files) == len(dummy_directory["tree"][1])

    files = search.get_files(dummy_directory["path"], extension=".png")
    assert len(files) == len(
        list(
            filter(lambda x: x.suffix == ".png", dummy_directory["file_list"])
        )
    )

    files = search.get_files(
        dummy_directory["path"], extension=[".png", ".jpg"]
    )
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix in [".png", ".jpg"],
                dummy_directory["file_list"],
            )
        )
    )

    files = search.get_files(
        dummy_directory["path"], extension=[".PNG", ".jpg"]
    )
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix in [".png", ".jpg"],
                dummy_directory["file_list"],
            )
        )
    )


def test_get_image_files(
    dummy_directory,
):
    files = search.get_image_files(dummy_directory["path"])
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix.lower()
                in search.SUPPORTED_IMAGE_EXTENSIONS,
                dummy_directory["file_list"],
            )
        )
    )

    files = search.get_image_files(dummy_directory["path"], recursive=False)
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix.lower()
                in search.SUPPORTED_IMAGE_EXTENSIONS,
                dummy_directory["tree"][1],
            )
        )
    )


def test_get_video_files(
    dummy_directory,
):
    files = search.get_video_files(dummy_directory["path"])
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix.lower() in search.SUPPORTED_VIDEO_EXTENSION,
                dummy_directory["file_list"],
            )
        )
    )

    files = search.get_video_files(dummy_directory["path"], recursive=False)
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix.lower() in search.SUPPORTED_VIDEO_EXTENSION,
                dummy_directory["tree"][1],
            )
        )
    )
