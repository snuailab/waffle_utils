from abc import ABC, abstractmethod

from waffle_utils.file import io

class BaseField(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def new(cls):
        pass

    @classmethod
    def from_dict(cls, d: dict):
        """Create Field Instance from dictionary"""
        return cls(**d)

    @classmethod
    def from_json(cls, f: str):
        """Create Field Instance from json file"""
        d: dict = io.load_json(f)
        return cls.from_dict(d)
