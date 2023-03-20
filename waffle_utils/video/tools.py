import logging
from pathlib import Path
from typing import Union

from waffle_utils.file.io import make_directory
from waffle_utils.file.search import get_image_files
from waffle_utils.image import (
    DEFAULT_IMAGE_EXTENSION,
    SUPPORTED_IMAGE_EXTENSION,
)
from waffle_utils.image.io import load_image, save_image
from waffle_utils.video.io import create_video_capture, create_video_writer

logger = logging.getLogger(__name__)

DEFAULT_FRAME_RATE = 30


def extract_frames(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    frame_rate: int = DEFAULT_FRAME_RATE,
    output_image_extension: str = DEFAULT_IMAGE_EXTENSION,
    verbose: bool = False,
) -> None:
    f"""
    Extracts frames as individual images from a video file.

    Args:
        input_path (Union[str, Path]): Path to the input video file.
        output_dir (Union[str, Path]): Path to the output directory where the frame images will be saved.
        frame_rate (int, optional): Frame rate of the output images. Defaults to {DEFAULT_FRAME_RATE}.
        output_image_extension (str, optional): Extension of the output frame images. Defaults to {DEFAULT_IMAGE_EXTENSION}.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
    """
    # Convert input_path and output_dir to Path objects
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Check if the output image extension is supported
    if output_image_extension not in SUPPORTED_IMAGE_EXTENSION:
        raise ValueError(
            f"Invalid output_image_extension: {output_image_extension}.\n"
            f"Must be one of {SUPPORTED_IMAGE_EXTENSION}."
        )

    # Create output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # Extract frames from the video file
    video_capture, meta = create_video_capture(input_path)

    fps = meta["fps"]
    frame_interval = int(round(fps / frame_rate))

    count = 0
    while True:
        success, image = video_capture.read()
        if not success:
            break

        # Only extract frames at the specified frame rate
        if count % frame_interval == 0:
            output_path = output_dir / f"{count}.{output_image_extension}"
            save_image(output_path, image)

            if verbose:
                logger.info(f"{input_path} ({count}) -> {output_path}.")

        count += 1

    # Release the video capture
    video_capture.release()
    logger.info(f"Output: {output_dir}/")


def create_video(
    input_dir: Union[str, Path],
    output_path: Union[str, Path],
    frame_rate: int = DEFAULT_FRAME_RATE,
    verbose: bool = False,
) -> None:
    f"""
    Creates a video file from a directory of frame images.

    Args:
        input_dir (Union[str, Path]): Path to the input directory containing the frame images.
        output_path (Union[str, Path]): Path to the output video file.
        frame_rate (int, optional): Frame rate of the output video. Defaults to {DEFAULT_FRAME_RATE}.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
    """
    # Convert input_dir and output_path to Path objects
    input_dir = Path(input_dir)
    output_path = Path(output_path)

    # Get image files
    image_files = get_image_files(input_dir)

    # Create output directory if it doesn't exist
    if not output_path.parent.exists():
        make_directory(input_dir)

    # Load the first frame to get dimensions
    first_frame = load_image(image_files[0])
    height, width = first_frame.shape[:2]

    # Determine the appropriate fourcc codec for the output video format
    out = create_video_writer(output_path, frame_rate, (width, height))

    # Iterate through frames and write to the video file
    for i, frame in enumerate(image_files):
        if verbose:
            logger.info(f"{frame} -> {output_path} ({i+1}/{len(image_files)})")
        image = load_image(frame)
        out.write(image)

    # Release the video writer
    out.release()
    logger.info(f"Output: {output_path}")
