from pathlib import Path
from typing import Union

import cv2
from natsort import natsorted

from waffle_utils.file.io import make_directory
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
)


def extract_frames(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    frame_rate: int = DEFAULT_FRAME_RATE,
    output_image_extension: str = DEFAULT_IMAGE_EXTENSION,
    verbose: bool = False,
) -> None:
    f"""Extract Frames as Individual Images from a Video File

    Args:
        input_path (Union[str, Path]): Path to the input video file.
        output_dir (Union[str, Path]): Path to the output directory where the frame images will be saved.
        frame_rate (int, optional): Frame rate of the output images. Defaults to {DEFAULT_FRAME_RATE}.
        output_image_extension (str, optional): Extension of the output frame images. Defaults to {DEFAULT_IMAGE_EXTENSION}.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    if output_image_extension not in SUPPORTED_IMAGE_EXTENSION:
        raise ValueError(
            f"Invalid output_image_extension: {output_image_extension}.\n"
            "Must be one of {SUPPORTED_IMAGE_EXTENSION}."
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
        if count % frame_interval == 0:
            output_path = output_dir / f"{count}.{output_image_extension}"
            save_image(output_path, image)

            if verbose:
                print(f"{input_path} ({count}) -> {output_path}.")

        success, image = video_capture.read()

    video_capture.release()
    print(f"Output: {output_dir}/")


def create_video(
    input_dir: Union[str, Path],
    output_path: Union[str, Path],
    frame_rate: int = DEFAULT_FRAME_RATE,
    verbose: bool = False,
) -> None:
    f"""Create a Video File from a Directory of Frame Images.

    Args:
        input_dir (Union[str, Path]): Path to the input directory containing the frame images.
        output_path (Union[str, Path]): Path to the output video file.
        frame_rate (int, optional): Frame rate of the output video. Defaults to {DEFAULT_FRAME_RATE}.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
    """
    input_dir = Path(input_dir)
    output_path = Path(output_path)

    # Check if all files have the same extension
    files = list(input_dir.glob("*"))
    file_extensions = set()

    for file in files:
        file_extensions.add(file.suffix)

    if len(file_extensions) != 1:
        raise ValueError(
            f"The files in {input_dir} do not have a consistent extension."
        )

    # Check if the extension of the files is supported
    unique_extension = file_extensions.pop()[1:]  # Get the unique extension existing.
    if unique_extension not in SUPPORTED_IMAGE_EXTENSION:
        raise ValueError(
            f"File extension in {input_dir}: {file_extensions}.\n"
            "Must be one of {SUPPORTED_IMAGE_EXTENSION}."
        )

    # Create output directory if it doesn't exist
    if not output_path.parent.exists():
        make_directory(input_dir)

    # Get a sorted list of frame image files
    image_files = natsorted(input_dir.glob(f"*.{unique_extension}"))

    # Load the first frame to get dimensions
    first_frame = load_image(image_files[0])
    height, width, _ = first_frame.shape

    # Initialize video writer with the desired codec, frame rate, and frame size
    output_extension = output_path.suffix

    # Determine the appropriate fourcc codec for the output video format
    if output_extension == ".mp4":
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    elif output_extension == ".avi":
        if cv2.VideoWriter_fourcc(*"MJPG") == -1:
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
        else:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    elif output_extension == ".wmv":
        fourcc = cv2.VideoWriter_fourcc(*"WMV2")
    elif output_extension == ".mov":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    elif output_extension == ".flv":
        fourcc = cv2.VideoWriter_fourcc(*"FLV1")
    elif output_extension == ".mkv":
        fourcc = cv2.VideoWriter_fourcc(*"VP80")
    elif output_extension == ".mpeg" or output_extension == ".mpg":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    else:
        raise ValueError(
            f"The extension {output_extension} is not supported.\n"
            f"Supported extensions are {SUPPORTED_VIDEO_EXTENSION}."
        )

    out = create_video_writer(
        output_path,
        fourcc,
        frame_rate,
        (width, height),
    )

    # Iterate through frames and write to the video file
    for i, frame in enumerate(image_files):
        if verbose:
            print(f"{frame} -> {output_path} ({i+1}/{len(image_files)})")
        image = load_image(frame)
        out.write(image)

    # Release the video writer and print a success message if verbose output is enabled
    out.release()
    print(f"Output: {output_path}")
