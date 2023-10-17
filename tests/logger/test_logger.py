import logging

from waffle_utils.logger import datetime_now, initialize_logger


def test_datetime_now():
    now = datetime_now()
    assert now is not None


def test_initialize_logger(tmpdir):
    initialize_logger(
        tmpdir.join("test.log"),
        console_level=logging.DEBUG,
        file_level=logging.DEBUG,
        root_level=logging.DEBUG,
    )

    logger = logging.getLogger()

    logger.info("test")
    logger.debug("test")

    with open(tmpdir.join("test.log")) as f:
        lines = f.readlines()
        assert len(lines) == 2
