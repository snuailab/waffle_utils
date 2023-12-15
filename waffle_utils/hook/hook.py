from waffle_utils.callback import BaseCallback


class BaseHook:
    def __init__(self, callbacks: list[BaseCallback] = None):
        self.callbacks = []
        if callbacks is not None:
            for callback in callbacks:
                self.register_callback(callback)
        self.hooks = []

    @property
    def callbacks(self):
        return self._callbacks

    @callbacks.setter
    def callbacks(self, value):
        self._callbacks = value

    def register_callback(self, callback: BaseCallback):
        """Register a callback."""
        if self._check_callback_exist(callback):
            raise ValueError("Callback already exist.")
        self.callbacks.append(callback)

    def unregister_callback(self, callback_idx: int):
        """Unregister a callback."""
        del self.callbacks[callback_idx]

    def _check_callback_exist(self, callback: BaseCallback) -> bool:
        for _callback in self.callbacks:
            if _callback == callback:
                return True
        return False

    def run_callback_hooks(self, hook_name, *args, **kwargs):
        """Run callback hooks."""
        for callback in self.callbacks:
            fn = getattr(callback, hook_name, None)
            if fn is not None:
                fn(*args, **kwargs)

    def run_default_hook(self, hook_name, *args, **kwargs):
        """Run default hook."""
        fn = getattr(self, hook_name, None)
        if fn is not None:
            fn(*args, **kwargs)
