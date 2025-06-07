from setuptools import setup
from Cython.Build import cythonize

setup(
    name="smoothmath",
    ext_modules=cythonize("smoothmath.pyx", language_level=3),
    zip_safe=False,
)