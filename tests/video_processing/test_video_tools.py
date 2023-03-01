import os
import shutil
import tempfile

from waffle_utils.video_processing.video_tools import VideoTools


def test_video_tools():
    # Create a temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join("tests/video_processing/test.mp4")
        input_file_copy = os.path.join(temp_dir, "test.mp4")
        output_dir = os.path.join(temp_dir, "frames")

        # Copy the input file to the temporary directory
        shutil.copy(input_file, input_file_copy)

        # Create a VideoTools instance from a video file
        vt = VideoTools.from_video(input_file_copy, output_dir)

        # Check that the input and output paths are correct
        assert vt.input_path == input_file_copy
        assert vt.output_path == output_dir

        # Extract frames from the video file
        vt.extract_frames(frame_rate=10, verbose=True)

        # Check that the frames were extracted correctly
        assert len(os.listdir(output_dir)) == 20

        # Create a video from the extracted frames using wildcard (*)
        input_dir = output_dir + "/*.jpg"
        output_file = os.path.join(temp_dir, "test_output.mp4")
        vt = VideoTools.from_images(input_dir, output_file)
        vt.create_video(fps=10, verbose=True)

        # Check that the video was created correctly
        assert os.path.isfile(output_file)

        # Create a video from the extracted frames not using wildcard (*)
        input_dir = output_dir
        output_file = os.path.join(temp_dir, "test_output.mp4")
        vt = VideoTools.from_images(input_dir, output_file)
        vt.create_video(fps=10, verbose=True)

        # Check that the video was created correctly
        assert os.path.isfile(output_file)

        # Clean up
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_video_tools()
