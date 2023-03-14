import tempfile
from pathlib import Path

from waffle_utils.file.io import copy_file
from waffle_utils.image import DEFAULT_IMAGE_EXTENSION
from waffle_utils.video import DEFAULT_VIDEO_EXTENSION
from waffle_utils.video.tools import create_video, extract_frames


def test_tools(tmpdir: Path):
    input_path = Path("tests/video/test.mp4")
    input_path_copy = tmpdir / "test.mp4"

    # Copy the input file to the temporary directory
    copy_file(input_path, input_path_copy)

    # Iterate over all combinations of image and video format
    image_extension = DEFAULT_IMAGE_EXTENSION
    video_extension = DEFAULT_VIDEO_EXTENSION

    # Create a subdirectory for this combination
    subdir_name = f"{image_extension}_to_{video_extension}"
    output_dir = tmpdir / subdir_name
    output_dir.mkdir()

    # Extract and save individual image frames from video
    extract_frames(
        input_path_copy,
        output_dir,
        frame_rate=30,
        output_image_extension=image_extension,
        verbose=True,
    )

    # Create a video file from the extracted frames
    input_dir = output_dir  # Use the images directory as input
    output_path = Path(
        tmpdir / f"test_{subdir_name}.{video_extension}"
    )
    create_video(input_dir, output_path, frame_rate=10, verbose=True)

    # Check that the video file was created correctly
    assert output_path.is_file()
    assert output_path.stat().st_size > 0


if __name__ == "__main__":
    test_tools()
