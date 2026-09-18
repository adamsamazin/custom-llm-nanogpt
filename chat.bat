@echo off
rem Double-click launcher for the terminal chat with the trained model (expanded corpus run).
rem Each run writes a new timestamped transcript under results\expanded\chat\.
setlocal
cd /d "%~dp0"
set PY=C:\venvs\nanogpt\Scripts\python.exe
if not exist "%PY%" set PY=python
if not exist results\expanded\chat mkdir results\expanded\chat
for /f "tokens=1-6 delims=/:. " %%a in ("%date% %time%") do set STAMP=%%c%%a%%b_%%d%%e%%f
set STAMP=%STAMP: =0%
echo Model: results\expanded\model.pt   (transcript: results\expanded\chat\chat_%STAMP%.json)
echo.
"%PY%" chat.py --model results\expanded\model.pt --transcript results\expanded\chat\chat_%STAMP%.json
echo.
pause
