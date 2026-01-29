# Installation and Training Script for Crop Disease Detection
# Run this script after installing Python 3.10 or 3.11

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Crop Disease Detection - Setup & Training" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "`nPlease install Python 3.10 or 3.11 from:" -ForegroundColor Red
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "`nMake sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

# Navigate to project directory
$projectDir = "c:\Users\user\Downloads\cnn-pytorch\cnn-pytorch-main"
Set-Location $projectDir
Write-Host "`nProject directory: $projectDir" -ForegroundColor Cyan

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "`nInstalling dependencies (this may take several minutes)..." -ForegroundColor Yellow
Write-Host "Installing: PyTorch, torchvision, Pillow, matplotlib, streamlit, pytest..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ All dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n✗ Installation failed. Please check the error messages above." -ForegroundColor Red
    exit 1
}

# Verify installation
Write-Host "`nVerifying installation..." -ForegroundColor Yellow
python -c "import torch; import torchvision; import PIL; import streamlit; print('✓ All packages imported successfully')"

# Display training information
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! Ready to Train" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nTraining Configuration:" -ForegroundColor Yellow
Write-Host "  • Dataset: Rice Leaf Diseases (3 classes)" -ForegroundColor White
Write-Host "  • Classes: Bacterialblight, Blast, Brownspot" -ForegroundColor White
Write-Host "  • Total Images: ~4,624" -ForegroundColor White
Write-Host "  • Epochs: 30" -ForegroundColor White
Write-Host "  • Batch Size: 16" -ForegroundColor White

Write-Host "`nTo start training, run:" -ForegroundColor Yellow
Write-Host "  python scripts/train_model.py" -ForegroundColor Cyan

Write-Host "`nWould you like to start training now? (Y/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Starting Model Training..." -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan
    python scripts/train_model.py
} else {
    Write-Host "`nSetup complete! Run training manually when ready:" -ForegroundColor Green
    Write-Host "  python scripts/train_model.py" -ForegroundColor Cyan
}
