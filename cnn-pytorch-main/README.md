# 🌾 Crop Disease Prediction System

A web-based application for detecting rice leaf diseases using deep learning, built with PyTorch and Streamlit.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Contributing](#contributing)

## ✨ Features

- 🔐 **User Authentication** - Secure login and registration system
- 🤖 **AI-Powered Prediction** - ResNet18-based disease classification
- 📤 **Batch Processing** - Analyze multiple images at once
- 📊 **Detailed Results** - Confidence scores and probability distributions
- 💡 **Treatment Advice** - Disease-specific treatment recommendations
- 🎨 **Modern UI** - Clean, responsive Streamlit interface

## 📁 Project Structure

```
cnn-pytorch-main/
│
├── 📱 Web Application
│   ├── app.py                 # Main Streamlit application
│   ├── auth.py                # Authentication module
│   ├── database.py            # Database operations
│   └── predictor.py           # Prediction module
│
├── 🔌 Interfaces (Abstractions)
│   └── interfaces/
│       ├── auth_interfaces.py      # Authentication contracts
│       ├── data_interfaces.py      # Data layer contracts
│       └── prediction_interfaces.py # Prediction contracts
│
├── ⚙️ Services (Implementations)
│   └── services/
│       ├── auth_services.py       # Auth implementations
│       ├── data_services.py       # Data implementations
│       └── prediction_services.py # Prediction implementations
│
├── 🧠 Model & Training
│   ├── src/
│   │   ├── model.py           # CNN model architecture
│   │   └── transforms.py      # Image transformations
│   ├── scripts/
│   │   ├── train_model.py           # Basic training script
│   │   ├── train_model_transfer.py  # Transfer learning script
│   │   ├── verify_model.py          # Model verification
│   │   └── test_single_image.py     # Single image testing
│   └── models/
│       └── best_model.pth           # Trained model weights
│
├── 📊 Data & Config
│   ├── config/
│   │   ├── class_names.json        # Disease class names
│   │   └── model_config.json       # Model configuration
│   ├── data/
│   │   └── users.db                # User database
│   └── datasets/                   # Training datasets
│
├── 📚 Documentation
│   └── docs/
│       ├── README.md                        # This file
│       ├── QUICK_START.txt                  # Quick start guide
│       ├── SETUP_AND_TRAINING.md            # Setup instructions
│       ├── STREAMLIT_README.md              # Streamlit guide
│       ├── SOLID_REFACTORING_SUMMARY.md     # SOLID principles guide
│       ├── SOLID_QUICK_REFERENCE.md         # SOLID quick reference
│       └── SOLID_VERIFICATION_CHECKLIST.md  # Verification checklist
│
├── 🧪 Tests
│   └── tests/
│       └── test_transforms.py      # Transform tests
│
└── 🚀 Launch Scripts
    ├── run_streamlit.ps1          # PowerShell launcher
    ├── run_streamlit.bat          # Batch launcher
    ├── install_and_train.ps1      # Setup & training (PS)
    └── install_and_train.bat      # Setup & training (Batch)
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Install

**Windows (PowerShell):**
```powershell
.\install_and_train.ps1
```

**Manual Installation:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python -m streamlit run app.py
```

## 💻 Usage

### Starting the Application

**Option 1: PowerShell Script**
```powershell
.\run_streamlit.ps1
```

**Option 2: Batch File**
```cmd
.\run_streamlit.bat
```

**Option 3: Direct Command**
```bash
python -m streamlit run app.py
```

The application will be available at: **http://localhost:8501**

### Using the Application

1. **Register/Login** - Create an account or login
2. **Upload Images** - Go to "Upload & Predict" page
3. **Analyze** - Upload rice leaf images (JPG, JPEG, PNG)
4. **View Results** - See predictions with confidence scores
5. **Get Treatment** - Read disease information and recommendations

## 🏗️ Architecture

### SOLID Principles

This project follows SOLID design principles:

- **S**ingle Responsibility - Each class has one job
- **O**pen/Closed - Open for extension, closed for modification
- **L**iskov Substitution - Interfaces are substitutable
- **I**nterface Segregation - Small, focused interfaces
- **D**ependency Inversion - Depend on abstractions

See [SOLID Documentation](docs/SOLID_REFACTORING_SUMMARY.md) for details.

### Technology Stack

- **Framework**: PyTorch
- **Web UI**: Streamlit
- **Database**: SQLite
- **Model**: ResNet18 (Transfer Learning)
- **Image Processing**: PIL, torchvision

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.txt) - Get started quickly
- [Setup & Training](docs/SETUP_AND_TRAINING.md) - Detailed setup instructions
- [Streamlit Guide](docs/STREAMLIT_README.md) - Web interface documentation
- [SOLID Principles](docs/SOLID_REFACTORING_SUMMARY.md) - Architecture guide
- [Quick Reference](docs/SOLID_QUICK_REFERENCE.md) - SOLID quick reference

## 🔬 Model Information

- **Architecture**: ResNet18 with transfer learning
- **Classes**: 3 (Bacterial Blight, Blast, Brown Spot)
- **Accuracy**: 66.7% on validation set
- **Input Size**: 224x224 RGB images
- **Parameters**: ~295K trainable parameters

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow SOLID principles
4. Add tests for new features
5. Submit a pull request

## 📝 License

This project is for educational and agricultural assistance purposes.

## ⚠️ Disclaimer

This tool is designed to assist in disease identification but should not replace professional agricultural advice. Always consult with agricultural experts for proper diagnosis and treatment.

## 📧 Support

For questions or issues, please check the documentation in the `docs/` folder.

---

Made with ❤️ for farmers and agricultural professionals
