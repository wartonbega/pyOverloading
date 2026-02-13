from setuptools import setup, find_packages

long_desc = ""
try:
    with open("README.md", "r") as file:
        long_desc = file.read()
except FileNotFoundError:
    long_desc = "ERROR reading readme.md"

setup(
    name="pyOverloading",
    version="2026.2.13",
    author="Anton Appel",
    description="A Python library for function overloading",
    long_description="",
    long_description_content_type="text/markdown",
    packages=long_desc,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)