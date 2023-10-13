import inspect
from typing import Optional, Union


def setter_type_validator(_type: type, strict: bool = True):
    def type_check(f):
        def input_check(self, v, *args, **kwargs):
            if v is not None:
                if not strict:
                    try:
                        v = _type(v)
                    except:
                        raise TypeError(
                            f"Cannot convert {v} to {_type} automatically"
                        )
                elif not isinstance(v, _type):
                    raise TypeError(f"value {v} should be {_type}")
            return f(self, v, *args, **kwargs)

        return input_check

    return type_check


def type_checker(f):
    """Validate arguments

    Raises:
        TypeError: if strict is True and argument type is not matched, else convert type.
    """

    # get type annotations
    annotations = f.__annotations__

    # get default arguments
    default_arguments = inspect.signature(f).parameters
    default_arguments = {
        key: value.default
        for key, value in default_arguments.items()
        if value.default is not inspect.Parameter.empty
    }

    def inner(*args, **kwargs):
        # get arguments
        arguments = inspect.signature(f).bind(*args, **kwargs).arguments

        # update arguments
        for key, value in default_arguments.items():
            if key not in arguments:
                arguments[key] = value

        # check arguments
        for key, value in arguments.items():
            if key in annotations:
                _type = annotations[key]
                if value is not None:
                    # check if _type is Union or Optional
                    if hasattr(_type, "__origin__"):
                        if _type.__origin__ == Union:
                            _type = _type.__args__
                        elif _type.__origin__ == Optional:
                            _type = _type.__args__[0]
                        else:
                            raise TypeError(f"Unknown type {_type} for {key}")
                    if not isinstance(value, _type):
                        raise TypeError(
                            f"{key} should be {_type} type, but got {type(value)} type"
                        )

        return f(**arguments)

    return inner
