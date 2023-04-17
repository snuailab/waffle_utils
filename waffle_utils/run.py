import logging

import typer

from waffle_utils.file.io import unzip
from waffle_utils.file.network import get_file_from_url
from waffle_utils.image import (
    DEFAULT_IMAGE_EXTENSION,
    SUPPORTED_IMAGE_EXTENSIONS,
)
from waffle_utils.log import initialize_logger
from waffle_utils.video import SUPPORTED_VIDEO_EXTENSION
from waffle_utils.video.tools import (
    DEFAULT_FRAME_RATE,
    create_video,
    extract_frames,
)

initialize_logger(
    "logs/cli.log", root_level=logging.DEBUG, console_level=logging.DEBUG
)
logger = logging.getLogger(__name__)

app = typer.Typer()

# coco docs
coco_file_docs = "COCO json file"
coco_root_dir_docs = "COCO image root directory"

# split docs
train_split_ratio_docs = (
    "train data ratio. val ratio will be set to (1-train_split_ratio)"
)


@app.command(name="get_file_from_url")
def _get_file_from_url(
    url: str = typer.Option(..., help="download link"),
    file_path: str = typer.Option(..., help="download output file"),
    create_directory: bool = True,
):
    get_file_from_url(url, file_path, create_directory=create_directory)
    logger.info(f"Downloading File {file_path} has been completed.")


@app.command(name="unzip")
def _unzip(
    file_path: str = typer.Option(..., help="zip file link"),
    output_dir: str = typer.Option(..., help="output directory"),
    create_directory: bool = True,
):
    unzip(file_path, output_dir, create_directory=create_directory)
    logger.debug(
        f"Extracting {file_path} under {output_dir} has been completed."
    )


# video processing docs
input_video_path_docs = "Path to input video file"
input_frames_dir_docs = "Directory to input frame image files"
output_frames_dir_docs = "Directory to output frame image files"
output_video_path_docs = f"Path for output video file. Example: path/to/video.mp4. Supported extensions: {SUPPORTED_VIDEO_EXTENSION}"
frame_rate_docs = "Frame rate"
output_image_extension_docs = (
    f"Output image extension. {SUPPORTED_IMAGE_EXTENSIONS}"
)
verbose_docs = "Verbose"


@app.command(name="extract_frames")
def _extract_frames(
    input_path: str = typer.Option(..., help=input_video_path_docs),
    output_dir: str = typer.Option(..., help=output_frames_dir_docs),
    num_of_frames: int = typer.Option(
        None, help="Number of frames to extract"
    ),
    interval_second: float = typer.Option(
        None, help="Distance between frames(second)"
    ),
    output_image_extension: str = typer.Option(
        DEFAULT_IMAGE_EXTENSION, help=output_image_extension_docs
    ),
    verbose: bool = typer.Option(False, help=verbose_docs),
):
    """Extract Frames from a Video File"""

    extract_frames(
        input_path,
        output_dir,
        num_of_frames,
        interval_second,
        output_image_extension,
        verbose,
    )


@app.command(name="create_video")
def _create_video(
    input_dir: str = typer.Option(..., help=input_frames_dir_docs),
    output_path: str = typer.Option(..., help=output_video_path_docs),
    frame_rate: int = typer.Option(DEFAULT_FRAME_RATE, help=frame_rate_docs),
    verbose: bool = typer.Option(False, help=verbose_docs),
):
    """Create a Video from Frame Image Files"""

    create_video(input_dir, output_path, frame_rate, verbose)


if __name__ == "__main__":
    app()
