# FRC Driver Station Launcher (Windows PowerShell)

Write-Host "FRC Driver Station - Setup and Launch" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

# Launch driver station
Write-Host "Launching FRC Driver Station..." -ForegroundColor Green
python main.py $args
