@echo off
setlocal
cd /d "%~dp0"
py -3.12 --version >nul 2>&1
if errorlevel 1 (
  echo Install Python 3.12 for Windows with the Python launcher, then retry.
  exit /b 1
)
where rubberband >nul 2>&1
if errorlevel 1 (
  echo Install the Rubber Band Windows command-line utility and add rubberband.exe to PATH.
  echo Download: https://breakfastquay.com/rubberband/
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  py -3.12 -m venv .venv
  if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
echo Ready. Run start.cmd and configure API keys on the page.
