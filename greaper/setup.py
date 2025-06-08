from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy

setup(
    name="greaper",
    version="0.1.0",
    packages=find_packages(),  # Automatically find all packages
    ext_modules=cythonize([
        Extension(
            "cython_ext.fuzzy_cython",
            ["cython_ext/fuzzy_cython.pyx"],
            include_dirs=[numpy.get_include()],
        ),
    ]),
    install_requires=[
        "numpy",  # Ensure numpy is installed as a dependency
        "cython", # Ensure cython is installed as a dependency
    ],
    zip_safe=False,
)