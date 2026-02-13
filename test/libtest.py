

import pyOverloading

@pyOverloading.overload
def toto(x: int):
    return x

@pyOverloading.overload
def toto(x: float):
    return -x
