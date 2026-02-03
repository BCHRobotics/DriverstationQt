@echo off
REM FRC Driver Station Launcher (Windows Batch)

echo FRC Driver Station - Setup and Launch
echo ======================================

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

REM Launch driver station
echo Launching FRC Driver Station...
python main.py %*

pause
