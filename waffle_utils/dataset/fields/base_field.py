from abc import ABC, abstractmethod


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
    @abstractmethod
    def from_dict(cls):
        pass

    @classmethod
    @abstractmethod
    def from_json(cls):
        pass
