@echo off
echo ========================================
echo Crop Disease Detection - Quick Setup
echo ========================================
echo.

cd /d "c:\Users\user\Downloads\cnn-pytorch\cnn-pytorch-main"

echo Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python not found!
    echo Please install Python 3.10 or 3.11 from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check 'Add Python to PATH' during installation!
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To train the model, run:
echo   python scripts\train_model.py
echo.
pause
