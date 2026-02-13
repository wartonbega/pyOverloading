import typing

def _arg_to_str(arg: type) -> str:
    ret = arg.__name__
    if sub := typing.get_args(arg):
        ret += f"[{_arg_tuple_to_str(sub)}]"
    return ret

def _arg_tuple_to_str(argtuple: tuple[any]) -> str:
    ret = ", ".join(map(_arg_to_str, argtuple))
    return ret