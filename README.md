_No AI used during developpement, other than this readme_
# pyOverloading

A lightweight Python library that brings **true function overloading** to Python using type hints.

Unlike `functools.singledispatch`, `pyOverloading` supports multiple arguments and deep inspection of generic types (e.g., distinguishing between a `list[int]` and a `list[str]`).

## ✨ Features

* **Multi-argument dispatch**: Overload functions based on the types of all arguments.
* **Deep Type Inspection**: Recursive check for nested types in lists, dicts, sets, and tuples.
* **Union & Any Support**: Full compatibility with `typing.Union` and `typing.Any`.
* **Decorator-based**: No boilerplate, just use `@overload`.

---

## 🚀 Installation

From your project root:

```bash
pip install .

```

---

## 💡 Usage & Examples

### Basic Overloading

The most common use case: same function name, different scalar types.

```python
from pyOverloading.Overloading import overload

@overload
def process(x: int):
    return f"Processing integer: {x}"

@overload
def process(x: str):
    return f"Processing string: {x}"

print(process(10))    # Output: Processing integer: 10
print(process("hi"))  # Output: Processing string: hi

```

### Advanced: Deep Generic Inspection

`pyOverloading` goes beyond the surface. It can differentiate between collections based on their content.

```python
from pyOverloading.Overloading import overload
from typing import List

@overload
def handle_data(data: List[int]):
    return sum(data)

@overload
def handle_data(data: List[str]):
    return "-".join(data)

print(handle_data([1, 2, 3]))      # Output: 6
print(handle_data(["a", "b"]))    # Output: a-b

```

### Complex Types (Unions & Dicts)

You can handle complex data structures seamlessly.

```python
from pyOverloading.Overloading import overload
from typing import Union, Dict

@overload
def update_config(conf: Dict[str, int]):
    print("Updating numeric configuration")

@overload
def update_config(val: int | float):
    print(f"Updating single scale value: {val}")

update_config({"timeout": 30}) # Matches Dict[str, int]
update_config(1.5)             # Matches Union[int, float]

```

---

## 🛠 How it works

1. **Registration**: When you decorate a function with `@overload`, it's added to a global registry keyed by its module and qualified name.
2. **Signature Mapping**: The library extracts the `inspect.signature` to map specific types to the correct function implementation.
3. **Runtime Dispatch**: When called, the wrapper analyzes the types of the passed arguments (recursively for containers) and executes the best match.

---

## ⚠️ Notes

* **Performance**: Deep type checking (like `list[int]`) involves iterating over collection elements. For high-performance loops, prefer specific function names.
* **Type Hints Required**: Arguments without type hints are treated as `object` (matches anything).
