:: filepath: c:\Users\storage\metasystems\build_fastmath.bat
@echo off
cd /d "%~dp0"
python setup.py build_ext --inplace
pause