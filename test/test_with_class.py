from pyOverloading.Overloading import overload


class Test:
    def __init__(self):
        pass

    @overload
    def foo(self, x: int, y: int):
        return x + y
    
    @overload
    def foo(self, x: float, y: float):
        return x - y
    
t = Test()
print(t.foo(1, 2))
print(t.foo(1.0, 2.0))