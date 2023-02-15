import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_now() -> str:
    """Return string of datetime now

    Returns:
        str: datetime (%Y-%m-%d %H:%M:%S)
    """
    return datetime.datetime.now().strftime(DATE_FORMAT)
