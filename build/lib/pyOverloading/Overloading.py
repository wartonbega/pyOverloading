import functools
import inspect
from collections import *
import typing
import types
import inspect

import pyOverloading.useful as uf

FUNCTIONS: dict[dict[tuple[str, str], function]] = {}


def _get_full_type(obj):
    base_type = type(obj)

    if isinstance(obj, (list, set)):
        if not obj:
            return base_type

        inner_types = {_get_full_type(item) for item in obj}

        if len(inner_types) == 1:
            return base_type[next(iter(inner_types))]
        else:
            return base_type[typing.Union[tuple(inner_types)]]

    elif isinstance(obj, dict):
        if not obj:
            return dict

        key_types = {_get_full_type(k) for k in obj.keys()}
        val_types = {_get_full_type(v) for v in obj.values()}

        k_type = next(iter(key_types)) if len(
            key_types) == 1 else typing.Union[tuple(key_types)]
        v_type = next(iter(val_types)) if len(
            val_types) == 1 else typing.Union[tuple(val_types)]

        return dict[k_type, v_type]

    elif isinstance(obj, tuple):
        return tuple[tuple(_get_full_type(item) for item in obj)]

    return base_type


def _type_instance_rec(t1: object, t2: object) -> bool:
    if t2 is typing.Any or t2 is object:
        return True
    if isinstance(t2, str):
        return t1.__name__ == t2

    orig1 = typing.get_origin(t1) or t1
    orig2 = typing.get_origin(t2) or t2
    args1 = typing.get_args(t1)
    args2 = typing.get_args(t2)
    if orig2 is typing.Union or (hasattr(types, "UnionType") and orig2 is types.UnionType):
        for union_arg in args2:
            if _type_instance_rec(t1, union_arg):
                return True
        return False

    try:
        if not orig1 == orig2:
            # if not issubclass(orig1, orig2):
            return False
    except TypeError:
        if orig1 != orig2:
            return False

    if args2:
        if not args1:
            return True

        if args1.__len__() != args2.__len__():
            return False

        for sub_t1, sub_t2 in zip(args1, args2):
            if not _type_instance_rec(sub_t1, sub_t2):
                return False

    return True


def _get_function_from_argtypes(function_key: tuple[str, str], args: list):
    arg_types = tuple(_get_full_type(a) for a in args)

    if arg_types in FUNCTIONS[function_key]:
        return FUNCTIONS[function_key][arg_types]
    for sig_types, func in FUNCTIONS[function_key].items():
        if len(sig_types) != len(arg_types):
            continue
        if all(_type_instance_rec(arg, t) for arg, t in zip(arg_types, sig_types)):
            return func

    raise TypeError(
        f"Function overloaded not found {function_key[0]}.{function_key[1]}({uf._arg_tuple_to_str(arg_types)})")


def overload(f: function) -> function:
    """Registers the function for a possible arguement type overloading.
    Two functions can therefore share the same name, but when called with different 
    types, doesn't call the same function.
    For example:
    ```python
    @overload
    def foo(x: int, y: int) -> int:
        return x + y

    @overload 
    def foo(x: float, y: float) -> float:
        return x - y

    foo(1, 2) # returns 3
    foo(1.0, 2.0) # returns -1.0
    ```
    For this 'trick' to work, the function must have the arguments decorated (otherwise they'll be considered as 'any').


    Args:
        f (function): The function that needs to be overloaded

    Returns:
        function: the overloaded function wrapper (still has the same name)
    """

    signature = inspect.signature(f)
    parameters = tuple(k.annotation if k.annotation is not inspect._empty else object for k in signature.parameters.values())

    # Registering the function
    function_key = (f.__module__, f.__qualname__)

    FUNCTIONS[function_key] = FUNCTIONS.get(function_key, {})
    FUNCTIONS[function_key][parameters] = f

    @functools.wraps(f)
    def func_overload(*args):
        funcname = func_overload.__qualname__
        funcmodu = func_overload.__module__    
        return _get_function_from_argtypes((funcmodu, funcname), args)(*args)

    return func_overload
