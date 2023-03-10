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
                print(f"Extracted frame {count} to {output_path}.")

        success, image = video_capture.read()

    video_capture.release()


def create_video(
    input_dir: Union[str, Path],
    output_path: Union[str, Path],
    frame_rate: int = DEFAULT_FRAME_RATE,
    input_image_extension: str = DEFAULT_IMAGE_EXTENSION,
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

    if input_image_extension not in SUPPORTED_IMAGE_EXTENSION:
        raise ValueError(
            f"Invalid input_image_extension: {input_image_extension}.\n"
            "Must be one of {SUPPORTED_IMAGE_EXTENSION}."
        )

    # TODO: Raise error when the files in the `input_dir` doesn't have consistant extension.
    # TODO: Raise error when the files in the `input_dir` doesn't have the supported image extension.
    # HACK
    for supported_image_extension in SUPPORTED_IMAGE_EXTENSION:
        image_files = list(input_dir.glob(f"*.{supported_image_extension}"))

    # Create output directory if it doesn't exist
    if not output_path.parent.exists():
        make_directory(input_dir)

    # Get a sorted list of frame image files
    image_files = natsorted(input_dir.glob(f"*.{input_image_extension}"))

    # Load the first frame to get dimensions
    first_frame = load_image(image_files[0])
    height, width, _ = first_frame.shape

    # Initialize video writer with the desired codec, frame rate, and frame size
    ext = output_path.suffix

    if ext == ".mp4":
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    elif ext == ".avi":
        if cv2.VideoWriter_fourcc(*"MJPG") == -1:
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
        else:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    elif ext == ".wmv":
        fourcc = cv2.VideoWriter_fourcc(*"WMV2")
    elif ext == ".mov":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    elif ext == ".flv":
        fourcc = cv2.VideoWriter_fourcc(*"FLV1")
    elif ext == ".mkv":
        fourcc = cv2.VideoWriter_fourcc(*"VP80")
    elif ext == ".mpeg" or ext == ".mpg":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    else:
        raise ValueError(
            f"The extension {ext} is not supported.\n"
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
            print(f"Processing frame {i+1}/{len(image_files)}")
        image = load_image(frame)
        out.write(image)

    # Release the video writer and print a success message if verbose output is enabled
    out.release()
    if verbose:
        print(f"Video saved to {output_path}")
