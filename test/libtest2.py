

import pyOverloading

@pyOverloading.overload
def toto(x: int):
    return x + 1

@pyOverloading.overload
def toto(x: float):
    return -x + 1
