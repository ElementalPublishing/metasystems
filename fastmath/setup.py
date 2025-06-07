from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension("fastmath", ["fastmath.c"])
    ]
)