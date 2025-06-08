from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy

ext_modules = cythonize([
    Extension(
        "cython_ext.fuzzy_cython",
        ["cython_ext/fuzzy_cython.pyx"],
    ),
    Extension(
        "cython_ext.search_cython",
        ["cython_ext/search_cython.pyx"],
    ),
])

setup(
    name="greaper",
    version="1.2.0",
    packages=find_packages(),
    ext_modules=ext_modules,
    install_requires=[
        "numpy",
        "cython",
        "re2; platform_system != 'Windows'",
    ],
    zip_safe=False,
)