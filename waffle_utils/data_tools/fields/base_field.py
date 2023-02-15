from abc import ABC, abstractmethod


class BaseField(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass
