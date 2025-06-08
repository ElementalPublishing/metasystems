from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

ext_modules = cythonize([
    Extension(
        "cython_ext.fuzzy_cython",
        ["cython_ext/fuzzy_cython.pyx"],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        "cython_ext.replace_cython",
        ["cython_ext/replace_cython.pyx"],
        # No numpy needed unless you use it in replace_cython.pyx
    ),
    Extension(
        "cython_ext.search_cython",
        ["cython_ext/search_cython.pyx"],
        # No numpy needed unless you use it in search_cython.pyx
    ),
])

setup(
    name="greaper-fuzzy-test",
    ext_modules=ext_modules,
)