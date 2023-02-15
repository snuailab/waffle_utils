def type_validator(_type: type):
    def type_check(f):
        def input_check(self, v, *args, **kwargs):
            if v is not None:
                if not isinstance(v, _type):
                    raise TypeError(f"value should be {_type}")
            return f(self, v, *args, **kwargs)

        return input_check

    return type_check
