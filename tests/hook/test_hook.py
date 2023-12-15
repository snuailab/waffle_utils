import pytest

from waffle_utils.callback import BaseCallback
from waffle_utils.hook import BaseHook


def test_run_hook():
    data = {}

    class Foo(BaseHook):
        def on_event_1(self):
            data["default_event_1"] = True

    class CustomCallback1(BaseCallback):
        def on_event_1(self, *args, **kwargs):
            data["event_1"] = True

    class CustomCallback2(BaseCallback):
        def on_event_2(self, *args, **kwargs):
            data["event_2"] = True

    #
    data.clear()
    foo = Foo(callbacks=[CustomCallback1()])
    foo.run_default_hook("on_event_1")
    assert "default_event_1" in data
    assert "event_1" not in data

    foo.run_callback_hooks("on_event_1")
    assert "event_1" in data

    foo.run_callback_hooks("on_event_2")
    assert "event_2" not in data

    #
    data.clear()
    foo = Foo(callbacks=[CustomCallback1(), CustomCallback2()])
    foo.run_callback_hooks("on_event_1")
    assert "event_1" in data

    foo.run_callback_hooks("on_event_2")
    assert "event_2" in data

    #
    data.clear()
    foo = Foo(callbacks=[CustomCallback1()])
    foo.run_callback_hooks("on_event_1")
    assert "event_1" in data

    foo.run_callback_hooks("on_event_2")
    assert "event_2" not in data

    foo.register_callback(CustomCallback2())
    foo.run_callback_hooks("on_event_2")
    assert "event_2" in data

    data.clear()
    foo.unregister_callback(1)
    foo.run_callback_hooks("on_event_2")
    assert "event_2" not in data


def test_callback():
    class CustomCallback(BaseCallback):
        pass

    callback1 = CustomCallback()
    callback2 = CustomCallback()

    assert callback1 == callback2

    with pytest.raises(ValueError):
        BaseHook(callbacks=[callback1, callback1])

    class CustomCallback(BaseCallback):
        def __init__(self, name):
            self.name = name

        @property
        def state_key(self):
            return self.name

    callback1 = CustomCallback("callback1")
    callback2 = CustomCallback("callback2")

    assert callback1 != callback2

    BaseHook(callbacks=[callback1, callback2])
