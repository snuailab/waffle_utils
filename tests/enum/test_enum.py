# Copyright The PyTorch Lightning team.
# Licensed under the Apache License, Version 2.0 (the "License");
#     http://www.apache.org/licenses/LICENSE-2.0
#
from enum import Enum

from waffle_utils.enum import StrEnum


def test_consistency():
    class MyEnum(StrEnum):
        FOO = "FOO"
        BAR = "BAR"
        BAZ = "BAZ"
        NUM = "32"

    # normal equality, case invariant
    assert MyEnum.FOO == "FOO"
    assert MyEnum.FOO == "foo"

    # int support
    assert MyEnum.NUM == 32
    assert MyEnum.NUM in (32, "32")

    # key-based
    assert MyEnum.from_str("num") == MyEnum.NUM

    # collections
    assert MyEnum.BAZ not in ("FOO", "BAR")
    assert MyEnum.BAZ in ("FOO", "BAZ")
    assert MyEnum.BAZ in ("baz", "FOO")
    assert MyEnum.BAZ not in {"BAR", "FOO"}
    # hash cannot be case invariant
    assert MyEnum.BAZ not in {"BAZ", "FOO"}
    assert MyEnum.BAZ in {"baz", "FOO"}


def test_comparison_with_other_enum():
    class MyEnum(StrEnum):
        FOO = "FOO"

    class OtherEnum(Enum):
        FOO = 123

    assert not MyEnum.FOO.__eq__(OtherEnum.FOO)


def test_create_from_string():
    class MyEnum(StrEnum):
        t1 = "T/1"
        T2 = "t:2"

    assert MyEnum.from_str("T1", source="key")
    assert MyEnum.try_from_str("T1", source="value") is None
    assert MyEnum.from_str("T1", source="any")

    assert MyEnum.try_from_str("T:2", source="key") is None
    assert MyEnum.from_str("T:2", source="value")
    assert MyEnum.from_str("T:2", source="any")


# additional custom test code
def test_iter():
    class MyEnum(StrEnum):
        FOO = "FOO"
        BAR = "BAR"
        BAZ = "BAZ"
        NUM = "32"

    assert list(MyEnum) == [MyEnum.FOO, MyEnum.BAR, MyEnum.BAZ, MyEnum.NUM]

    members = []
    for member in MyEnum:
        members.append(member)
    assert members == [MyEnum.FOO, MyEnum.BAR, MyEnum.BAZ, MyEnum.NUM]

    assert MyEnum.FOO in MyEnum

    assert MyEnum.FOO in {
        MyEnum.FOO: "something",
    }


def test_str_util():
    class MyEnum(StrEnum):
        FOO = "FOO"

    assert MyEnum.FOO.lower() == "foo"
    assert MyEnum.FOO.upper() == "FOO"
