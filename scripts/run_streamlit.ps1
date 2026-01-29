# Launch Streamlit Application for Crop Disease Prediction

Write-Host "Starting Crop Disease Prediction System..." -ForegroundColor Green
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

& "C:\Users\user\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run app.py

Read-Host "Press Enter to exit"
