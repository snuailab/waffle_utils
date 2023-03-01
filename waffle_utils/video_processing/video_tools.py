from waffle_utils.utils import type_validator
from pathlib import Path


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
    def video_to_frames(
        cls, input_video_path: str, output_dir: str = None
    ) -> "VideoTools":
        return cls(input_video_path, output_dir)

    @classmethod
    def frames_to_video(cls, fream_dir, output_file) -> "VideoTools":
        raise NotImplementedError("`frames_to_video()` is not yet implemented")

    @classmethod
    def split_video(cls, output_dir, chunk_duration) -> "VideoTools":
        raise NotImplementedError("`split_video()` is not yet implemented.")

    @classmethod
    def merge_videos(cls, input_files, output_file) -> "VideoTools":
        raise NotImplementedError("`merge_split() is not yet implemented")

    def extract_frames(self, frame_rate) -> None:
        # TODO: Implement
        raise NotImplementedError("`extract_frames()` is not yet implemented")
