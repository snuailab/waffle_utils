import tempfile
from pathlib import Path

from waffle_utils.file.io import copy_file, remove_directory
from waffle_utils.video.config import (
    SUPPORTED_IMAGE_EXTENSION,
    SUPPORTED_VIDEO_EXTENSION,
)
from waffle_utils.video.tools import create_video, extract_frames


def test_tools():
    # Create a temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        input_path = Path("tests/video/test.mp4")
        input_path_copy = temp_dir / "test.mp4"
        output_dir = temp_dir / "frames"

        # Copy the input file to the temporary directory
        copy_file(input_path, input_path_copy)

        # Test extract_frames() with all supported image extensions
        for extension in SUPPORTED_IMAGE_EXTENSION:
            # Extract and save individual image frames from video
            extract_frames(
                input_path_copy,
                output_dir,
                frame_rate=30,
                output_image_extension=extension,
                verbose=True,
            )

            # Check that the frames were extracted correctly
            assert len(list(output_dir.glob("*." + extension))) == 209
            assert all(frame.is_file() for frame in output_dir.glob("*." + extension))

        # Create a video file from the extracted frames with different extensions
        # TODO: Add test for all the extensions
        input_dir = output_dir
        for extension in SUPPORTED_VIDEO_EXTENSION:
            output_path = temp_dir / f"test_create_video.{extension}"
            create_video(input_dir, output_path, frame_rate=10, verbose=True)

            # Check that the video file was created correctly
            assert output_path.is_file()
            assert output_path.stat().st_size > 0

        # Clean up
        remove_directory(temp_dir)


if __name__ == "__main__":
    test_tools()
