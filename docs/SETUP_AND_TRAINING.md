# Setup and Training Guide

## Prerequisites

### 1. Install Python 3.10 or 3.11
Download and install Python from: https://www.python.org/downloads/

**Important during installation:**
- ✅ Check "Add Python to PATH"
- ✅ Install for all users (recommended)

### 2. Verify Python Installation
Open a new PowerShell window and run:
```powershell
python --version
```
You should see: `Python 3.10.x` or `Python 3.11.x`

## Installation Steps

### 1. Create Virtual Environment
```powershell
cd "c:\Users\user\Downloads\cnn-pytorch\cnn-pytorch-main"
python -m venv venv
```

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- PyTorch (for deep learning)
- torchvision (for image processing)
- Pillow (for image handling)
- matplotlib (for visualization)
- streamlit (for web app)
- pytest (for testing)

## Training the Model

### Quick Start - Train on 3 Rice Leaf Disease Classes

**The training script has been configured to train on:**
- Bacterialblight (1,584 images)
- Blast (1,440 images)
- Brownspot (1,600 images)

**Total: 4,624 images**

### Run Training
```powershell
# Make sure virtual environment is activated
python scripts/train_model.py
```

### Training Configuration
- **Batch Size:** 16
- **Epochs:** 30
- **Learning Rate:** 0.001
- **Validation Split:** 20%
- **Input Size:** 224x224 pixels
- **Data Augmentation:** Enabled (random flips, rotations, color jitter)

### Expected Training Time
- **CPU only:** ~2-4 hours
- **With GPU (CUDA):** ~20-40 minutes

### What Happens During Training
1. Dataset is loaded and split into train (80%) and validation (20%)
2. Model trains for 30 epochs
3. Best model is saved based on validation accuracy
4. Training metrics are plotted and saved
5. Class names are updated in config files

### Output Files After Training
- `models/crop_disease_model.pth` - Final trained model
- `models/best_model.pth` - Best model during training
- `models/training_history.png` - Loss and accuracy plots
- `models/training_history.json` - Training metrics
- `config/class_names.json` - Updated with the 3 classes

## Verify Setup (Before Training)

Run the verification script to check everything is ready:
```powershell
python scripts/verify_setup.py
```

## Training on All 4 Classes

If you want to train on all 4 rice leaf disease classes (including Tungro), edit:
`scripts/train_model.py` line 211:
```python
SELECTED_CLASSES = ['Bacterialblight', 'Blast', 'Brownspot', 'Tungro']
```

## Monitoring Training Progress

During training, you'll see:
```
Epoch [1/30] (45.2s)
  Train Loss: 0.8234 | Train Acc: 0.6842
  Val Loss:   0.7156 | Val Acc:   0.7321
  ✓ New best model saved! (Val Acc: 0.7321)
```

## Troubleshooting

### Issue: "CUDA out of memory"
**Solution:** Reduce batch size in `train_model.py`:
```python
BATCH_SIZE = 8  # or even 4
```

### Issue: Training is very slow
**Solution:** 
- Reduce `NUM_EPOCHS = 10` for faster testing
- Or reduce `num_workers=0` in DataLoader

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Next Steps After Training

1. **Test the model:** Run inference on test images
2. **Complete the Streamlit web app:** Integrate the trained model
3. **Deploy:** Make it accessible to users

---

**Ready to train?** Once Python is installed, follow the steps above!
