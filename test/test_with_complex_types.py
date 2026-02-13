from .. import overload

@overload
def foo(x: int|float, y: tuple[int, int]):
    return 0

@overload
def foo(x: bool, y: tuple[int, int]):
    return 1

@overload
def foo(x: int|float, y: tuple[int|float, int]):
    return 2

print(foo(1, (1, 2)))
print(foo(False, (1, 2)))
print(foo(0.1, (1.1, 2)))
