from pathlib import Path
from typing import Union

import wget

from . import io


def get_file_from_url(
    url: str, out: Union[str, Path], create_directory: bool = False
):
    """Download file from url using wget

    Args:
        url (str): file url
        out (str): output file path
        create_directory (bool, optional): create destination directory or not. Defaults to False.
    """

    out = Path(out)

    if create_directory:
        io.make_directory(out.parent)

    # If the file already exists, do not download it again
    if out.exists():
        return

    wget.download(url, str(out))
