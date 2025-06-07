from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("gitdestroyer_cykernel.pyx")
)