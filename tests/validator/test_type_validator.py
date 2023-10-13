from typing import Optional, Union

import numpy as np
import pytest

from waffle_utils.validator import setter_type_validator, type_checker


def test_setter_type_validator():
    class Test:
        @property
        def a(self):
            return self._a

        @a.setter
        @setter_type_validator(int)
        def a(self, v):
            self._a = v

        @property
        def b(self):
            return self._b

        @b.setter
        @setter_type_validator(int, strict=False)
        def b(self, v):
            self._b = v

    test = Test()

    test.a = 1
    assert test.a == 1

    with pytest.raises(TypeError):
        test.a = "a"

    test.b = 1
    assert test.b == 1

    test.b = "1"
    assert test.b == 1

    with pytest.raises(TypeError):
        test.b = "not int"


def test_type_checker():
    @type_checker
    def test1(a: int, b: str, c: float = 1.0):
        pass

    test1(1, "a")
    test1(1, "a", 1.0)

    with pytest.raises(TypeError):
        test1("a", "a")

    with pytest.raises(TypeError):
        test1(1, 1)

    with pytest.raises(TypeError):
        test1(1, "a", "a")

    @type_checker
    def test2(a: Union[int, float]):
        pass

    test2(1)
    test2(1.0)

    with pytest.raises(TypeError):
        test2("a")

    @type_checker
    def test3(a: Union[int, float, np.ndarray]):
        pass

    test3(1)
    test3(1.0)
    test3(np.array([1]))

    with pytest.raises(TypeError):
        test3("a")

    @type_checker
    def test4(a: Optional[int] = None):
        pass

    test4(1)
    test4(None)
    test4()
