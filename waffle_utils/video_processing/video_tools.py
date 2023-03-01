import os
from pathlib import Path

import cv2

from waffle_utils.utils import type_validator


class VideoTools:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = self._input_path = input_path
        self.output_path = self._output_path = output_path

    # properties
    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    @type_validator(str)
    def input_path(self, v):
        self._input_path = v

    @property
    def output_path(self):
        return self._output_path

    @output_path.setter
    @type_validator(str)
    def output_path(self, v):
        self._output_path = v

    # factories
    @classmethod
    def from_video(
        cls,
        input_path: str,
        output_path: str,
    ) -> "VideoTools":
        """Create a `VideoTools` Instance from a Video File.

        Args:
            input_path (str): Path to the input video file.
            output_path (str): Path to the output video or image files.

        Raises:
            ValueError: If the input file type is not supported.

        Example:
            # Create a VideoTools instance from a video file
            vt = VideoTools.from_video(
                "path/to/input.mp4",
                "path/to/images",
            )

        Returns:
            VideoTools: A VideoTools instance with the input and output paths.
        """
        # Check if input file is a supported video format
        supported_formats = (".mp4", ".avi", ".mov", ".wmv")
        if not input_path.lower().endswith(supported_formats):
            raise ValueError(
                f"Unsupported file type: {input_path}\n"
                f"Supported file types are: {supported_formats}"
            )

        return cls(input_path, output_path)

    @classmethod
    def from_images(
        cls,
        input_path: str,
        output_path: str,
    ) -> "VideoTools":
        """Create a `VideoTools` Instance from a Directory of images.

        Args:
            input_path (str): Path to the directory of input images.
            output_path (str): Path to the output video file.

        Raises:
            ValueError: If the input file type is not supported.

        Example:
            # Create a VideoTools instance from a directory of images
            vt = VideoTools.from_images(
                "path/to/images",
                "path/to/output.avi",
            )

        Returns:
            VideoTools: A VideoTools instance with the input and output paths.
        """
        return cls(input_path, output_path)

    def extract_frames(
        self,
        frame_rate: int = 30,
        verbose: bool = False,
    ) -> None:
        """Extract Frames fom a Video

        Args:
            frame_rate (int, optional): Frame rate. Defaults to 30.
            verbose (bool, optional): Verbose. Defaults to False.
        """
        # Create output directory if it doesn't exist
        if not Path(self.output_path).exists():
            os.makedirs(str(self.output_path))

        # Extract frames from the video file
        video_capture = cv2.VideoCapture(self.input_path)
        success, image = video_capture.read()
        count = 0
        while success:
            count += 1
            if count % frame_rate == 0:
                output_file_path = Path(self.output_path) / f"{count}.jpg"
                cv2.imwrite(str(output_file_path), image)

                if verbose:
                    print(f"Extracted frame {count} to {output_file_path}.")

            success, image = video_capture.read()

        video_capture.release()

    def create_video(self, fps: int = 30, verbose: bool = False) -> None:
        """Create a Video from Frames

        Args:
            fps (int, optional): Frames per second. Defaults to 30.
            verbose (bool, optional): Verbos. Defaults to False.
        """
        # Create output directory if it doesn't exist
        if not Path(self.output_path).parent.exists():
            os.makedirs(str(Path(self.output_path).parent))

        # Get the list of frames
        if "*" in self.input_path:  # if input path has wildcard (*)
            frames = sorted(Path(self.input_path).parent.glob("*.jpg"))
        else:  # if input path does not have wildcard (*)
            if Path(self.input_path).is_file():
                frames = [Path(self.input_path)]
            else:
                frames = sorted(Path(self.input_path).glob("*.jpg"))

        # Load the first frame to get dimensions
        first_frame = cv2.imread(str(frames[0]))
        height, width, _ = first_frame.shape

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            str(self.output_path),
            fourcc,
            fps,
            (width, height),
        )

        # Iterate through frames and write to video
        for i, frame in enumerate(frames):
            if verbose:
                print(f"Processing frame {i+1}/{len(frames)}")
            image = cv2.imread(str(frame))
            out.write(image)

        # Release video writer and print success message
        out.release()
        if verbose:
            print(f"Video saved to {self.output_path}")

    def split_video(self, output_dir, chunk_duration) -> "VideoTools":
        raise NotImplementedError("`split_video()` is not yet implemented.")

    def merge_videos(self, input_files, output_file) -> "VideoTools":
        raise NotImplementedError("`merge_split() is not yet implemented")
