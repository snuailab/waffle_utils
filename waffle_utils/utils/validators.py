def type_validator(_type: type, strict: bool = True):
    def type_check(f):
        def input_check(self, v, *args, **kwargs):
            if v is not None:
                if not strict:
                    v = _type(v)
                elif not isinstance(v, _type):
                    raise TypeError(f"value {v} should be {_type}")
            return f(self, v, *args, **kwargs)

        return input_check

    return type_check
