@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m venv .venv-face
if errorlevel 1 exit /b 1
".venv-face\Scripts\python.exe" -m pip install mediapipe==1.1.0 pillow==12.3.0 numpy==2.5.3
if errorlevel 1 exit /b 1
echo Face mesh worker ready.
