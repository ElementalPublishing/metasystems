:: filepath: c:\Users\storage\metasystems\build_fastmath.bat
@echo off
cd /d "%~dp0"

REM Clean previous build artifacts
del /q fastmath.c 2>nul
del /q fastmath.cp*.pyd 2>nul
del /q fastmath.*.so 2>nul
rmdir /s /q build 2>nul

REM Re-generate the C file from the .pyx
python -m cython fastmath.pyx

REM Build the extension in-place
python setup.py build_ext --inplace

pause