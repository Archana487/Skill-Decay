@echo off
echo Starting Skill Decay Tracker...
echo.

:: Check for requirements.txt
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Open the browser after a short delay
echo Opening dashboard...
start "" "http://127.0.0.1:5000"

:: Start the Flask app
echo Launching application...
python app.py

pause
