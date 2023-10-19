from waffle_utils.file import search


def test_is_empty(
    dummy_empty_directory,
):
    assert search.is_empty(dummy_empty_directory["path"])


def test_get_files(
    dummy_directory,
):
    files = search.get_files(dummy_directory["path"])
    assert len(files) == dummy_directory["length"]

    files = search.get_files(dummy_directory["path"], recursive=False)
    assert len(files) == len(dummy_directory["file_tree"][1])

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


def test_get_directories(
    dummy_directory,
):
    files = search.get_directories(dummy_directory["path"])
    assert sorted(files) == sorted(
        sum(dummy_directory["directory_tree"].values(), [])
    )

    files = search.get_directories(dummy_directory["path"], recursive=False)
    assert sorted(files) == sorted(dummy_directory["directory_tree"][1])

    files = search.get_directories(dummy_directory["path"], only_empty=True)
    assert len(files) == 1


def test_get_files_and_directories(
    dummy_directory,
):
    files = search.get_files_and_directories(dummy_directory["path"])
    assert sorted(files) == sorted(
        sum(dummy_directory["directory_tree"].values(), [])
        + sum(dummy_directory["file_tree"].values(), [])
    )

    files = search.get_files_and_directories(
        dummy_directory["path"], recursive=False
    )
    assert sorted(files) == sorted(
        dummy_directory["directory_tree"][1] + dummy_directory["file_tree"][1]
    )

    files = search.get_files_and_directories(
        dummy_directory["path"], extension=".png"
    )
    assert len(files) == len(
        list(
            filter(lambda x: x.suffix == ".png", dummy_directory["file_list"])
        )
    ) + len(sum(dummy_directory["directory_tree"].values(), []))

    files = search.get_files_and_directories(
        dummy_directory["path"], extension=[".png", ".jpg"]
    )
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix in [".png", ".jpg"],
                dummy_directory["file_list"],
            )
        )
    ) + len(sum(dummy_directory["directory_tree"].values(), []))

    files = search.get_files_and_directories(
        dummy_directory["path"], extension=[".PNG", ".jpg"]
    )
    assert len(files) == len(
        list(
            filter(
                lambda x: x.suffix in [".png", ".jpg"],
                dummy_directory["file_list"],
            )
        )
    ) + len(sum(dummy_directory["directory_tree"].values(), []))


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
                dummy_directory["file_tree"][1],
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
                dummy_directory["file_tree"][1],
            )
        )
    )
