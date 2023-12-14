class BaseCallback:
    def __init__(self) -> None:
        pass

    @property
    def state_key(self) -> str:
        """Return the state key.

        Can be overwritten by subclasses.
        """
        return self.__class__.__qualname__

    def __eq__(self, other: object) -> bool:
        """Compare two instances."""
        if issubclass(other.__class__, BaseCallback):
            return self.state_key == other.state_key
        return False
