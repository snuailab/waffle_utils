import tempfile
from pathlib import Path

from waffle_utils.file.io import copy_file, remove_directory
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

        # Extract and save individual image frames from video
        extract_frames(input_path, output_dir, frame_rate=30, verbose=True)

        # Check that the frames were extracted correctly
        assert len(list(output_dir.glob("*.jpg"))) == 209
        assert all(frame.is_file() for frame in output_dir.glob("*.jpg"))

        # Create a video file from the extracted frames
        input_dir = output_dir
        output_path = temp_dir / "test_create_video.mp4"
        create_video(input_dir, output_path, frame_rate=10, verbose=True)

        # Check that the video file was created correctly
        assert output_path.is_file()
        assert output_path.stat().st_size > 0

        # Clean up
        remove_directory(temp_dir)


if __name__ == "__main__":
    test_tools()
