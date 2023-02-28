from waffle_utils.utils import type_validator
from pathlib import Path


class VideoTools:
    def __init__(self, input_video_path: str, output_dir: str = None):
        self.input_video_path = self._input_video_path = input_video_path
        self.root_dir = self._root_dir = Path(output_dir)  # TODO: if root_dir else

    @property
    def input_video_path(self):
        return self._input_video_path

    @input_video_path.setter
    @type_validator(str)
    def input_video_path(self, v):
        self._input_video_path = v

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    @type_validator(Path)
    def root_dir(self, v):
        self._root_dir = v

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
