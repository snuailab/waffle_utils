from pathlib import Path
from typing import Union

import cv2
from natsort import natsorted

from waffle_utils.file.io import make_directory
from waffle_utils.file.search import get_file_extensions
from waffle_utils.opencv.io import (
    create_video_capture,
    create_video_writer,
    load_image,
    save_image,
)
from waffle_utils.video.config import (
    DEFAULT_FRAME_RATE,
    DEFAULT_IMAGE_EXTENSION,
    SUPPORTED_IMAGE_EXTENSION,
    SUPPORTED_VIDEO_EXTENSION,
    FOURCC_MAP,
)


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
    video_capture = create_video_capture(input_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    success, image = video_capture.read()
    count = 0
    frame_interval = int(round(fps / frame_rate))
    while success:
        count += 1
        # Only extract frames at the specified frame rate
        if count % frame_interval == 0:
            output_path = output_dir / f"{count}.{output_image_extension}"
            save_image(output_path, image)

            if verbose:
                print(f"{input_path} ({count}) -> {output_path}.")

        success, image = video_capture.read()

    # Release the video capture
    video_capture.release()
    print(f"Output: {output_dir}/")


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

    # Get the file extension of the input frame images
    extension = get_file_extensions(input_dir, single=True)

    # Check if the file extension is supported for image files
    if extension not in SUPPORTED_IMAGE_EXTENSION:
        raise ValueError(
            f"File extension in {input_dir}: {extension}.\n"
            f"Must be one of {SUPPORTED_IMAGE_EXTENSION}."
        )

    # Get the file extension of the output video file
    output_extension = output_path.suffix[1:]

    # Check if the file extension is supported for video file
    if output_extension not in SUPPORTED_VIDEO_EXTENSION:
        raise ValueError(
            f"Output video extension: {output_extension}.\n"
            f"Must be one of {SUPPORTED_VIDEO_EXTENSION}."
        )

    # Create output directory if it doesn't exist
    if not output_path.parent.exists():
        make_directory(input_dir)

    # Get a sorted list of frame image files
    image_files = natsorted(input_dir.glob(f"*.{extension}"))

    # Load the first frame to get dimensions
    first_frame = load_image(image_files[0])
    height, width, _ = first_frame.shape

    # Determine the appropriate fourcc codec for the output video format
    fourcc = FOURCC_MAP[output_extension]
    out = create_video_writer(output_path, fourcc, frame_rate, (width, height))

    # Iterate through frames and write to the video file
    for i, frame in enumerate(image_files):
        if verbose:
            print(f"{frame} -> {output_path} ({i+1}/{len(image_files)})")
        image = load_image(frame)
        out.write(image)

    # Release the video writer
    out.release()
    print(f"Output: {output_path}")
