from waffle_utils.utils import type_validator
from pathlib import Path


class VideoTools:
    def __init__(self, name: str, root_dir: str = None):
        self.name = self._name = name
        self.root_dir = self._root_dir = Path(root_dir)  # TODO: if root_dir else

    @property
    def name(self):
        return self._name

    @name.setter
    @type_validator(str)
    def name(self, v):
        self._name = v

    @property
    def root_dir(self):
        return self._root_dir

    @root_dir.setter
    @type_validator(Path)
    def root_dir(self, v):
        self._root_dir = v

    # factories
    @classmethod
    def video_to_frames(cls, name: str, root_dir: str = None) -> None:
        print("This is a test for the function `extract_frames()`")
        # TODO: Implement

    @classmethod
    def frames_to_video(cls, fream_dir, output_file) -> None:
        raise NotImplementedError("`frames_to_video()` is not yet implemented")

    @classmethod
    def split_video(cls, output_dir, chunk_duration) -> None:
        raise NotImplementedError("`split_video()` is not yet implemented.")

    @classmethod
    def merge_videos(cls, input_files, output_file) -> None:
        raise NotImplementedError("`merge_split() is not yet implemented")
