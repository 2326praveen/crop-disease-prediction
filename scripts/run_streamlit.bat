@echo off
REM Launch Streamlit Application for Crop Disease Prediction

echo Starting Crop Disease Prediction System...
echo.

cd /d "%~dp0"

"C:\Users\user\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run app.py

pause
