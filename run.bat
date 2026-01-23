@echo off
echo Starting Skill Decay Tracker...
echo.

:: Check for requirements.txt
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Start the Flask app in a new window/process
echo Launching application...
start /b python app.py

:: Open the browser after a short delay
echo Waiting for server to initialize...
timeout /t 3 /nobreak > nul
echo Opening dashboard...
start "" "http://localhost:5000"

pause
