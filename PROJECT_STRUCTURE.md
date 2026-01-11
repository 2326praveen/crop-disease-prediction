# 📂 Project Structure Guide

## 🎯 Overview

This document provides a comprehensive overview of the project structure after SOLID refactoring and organization.

## 📊 Directory Tree

```
cnn-pytorch-main/
│
├── 📱 APPLICATION LAYER (User Interface)
│   ├── app.py                      # Main Streamlit web application
│   ├── auth.py                     # Authentication facade
│   ├── database.py                 # Database facade
│   └── predictor.py                # Prediction facade
│
├── 🔌 INTERFACES LAYER (Abstractions - DIP)
│   └── interfaces/
│       ├── __init__.py
│       ├── auth_interfaces.py      # IAuthenticationService, ISessionManager, IPasswordValidator
│       ├── data_interfaces.py      # IUserRepository, IPasswordHasher, IDatabaseConnection
│       └── prediction_interfaces.py # IModelLoader, IPredictionService, IDiseaseInfoProvider
│
├── ⚙️ SERVICES LAYER (Implementations - SRP, OCP)
│   └── services/
│       ├── __init__.py
│       ├── auth_services.py        # AuthenticationService, StreamlitSessionManager
│       ├── data_services.py        # UserRepository, SQLiteConnection, SHA256PasswordHasher
│       └── prediction_services.py  # PredictionService, PyTorchModelLoader, ImagePreprocessor
│
├── 🧠 MODEL LAYER (Deep Learning)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── model.py                # CropDiseaseClassifier CNN architecture
│   │   └── transforms.py           # ImageTransformer for preprocessing
│   │
│   ├── models/
│   │   ├── .gitkeep
│   │   ├── best_model.pth          # Trained ResNet18 model (3.1 MB)
│   │   ├── crop_disease_model.pth  # Alternative model
│   │   └── training_history*.json  # Training metrics and history
│   │
│   └── scripts/
│       ├── README.md               # Scripts documentation
│       ├── train_model.py          # Basic CNN training script
│       ├── train_model_transfer.py # Transfer learning with ResNet18
│       ├── verify_model.py         # Model verification utility
│       ├── test_single_image.py    # Single image prediction test
│       ├── plot_training_history.py # Visualize training metrics
│       ├── prepare_*.py            # Dataset preparation scripts
│       └── verify_setup.py         # Environment verification
│
├── 📊 DATA LAYER (Storage & Configuration)
│   ├── config/
│   │   ├── class_names.json        # Disease class definitions
│   │   └── model_config.json       # Model hyperparameters
│   │
│   ├── data/
│   │   └── users.db                # SQLite user database (runtime)
│   │
│   └── datasets/
│       ├── mixed_dataset/          # Combined training data
│       │   ├── train/              # Training images
│       │   ├── val/                # Validation images
│       │   └── test/               # Test images
│       ├── rice_leaf_subset/       # Rice-only dataset
│       └── praveen_kumar_reddy/    # Original dataset source
│
├── 🧪 TESTING LAYER (Quality Assurance)
│   └── tests/
│       ├── __init__.py
│       ├── test_transforms.py      # Image transformation tests
│       └── test_predictor.py       # Prediction module tests
│
├── 📚 DOCUMENTATION LAYER (Knowledge Base)
│   └── docs/
│       ├── README.md                        # Main project documentation
│       ├── QUICK_START.txt                  # Quick start guide
│       ├── SETUP_AND_TRAINING.md            # Installation & training guide
│       ├── STREAMLIT_README.md              # Web interface documentation
│       ├── SOLID_REFACTORING_SUMMARY.md     # Complete SOLID guide
│       ├── SOLID_QUICK_REFERENCE.md         # SOLID principles reference
│       ├── SOLID_VERIFICATION_CHECKLIST.md  # Quality checklist
│       ├── TRAINING_SUMMARY.md              # Training results
│       └── TRAINING_FIXES_SUMMARY.md        # Training troubleshooting
│
├── 🚀 DEPLOYMENT LAYER (Launch Scripts)
│   ├── run_streamlit.ps1          # PowerShell launcher
│   ├── run_streamlit.bat          # Batch launcher
│   ├── install_and_train.ps1      # Setup & training (PowerShell)
│   └── install_and_train.bat      # Setup & training (Batch)
│
├── ⚙️ CONFIGURATION FILES (Project Setup)
│   ├── .gitignore                 # Git ignore rules
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Project overview
│
└── 🔧 ENVIRONMENT (Development)
    ├── .vscode/                   # VS Code settings
    └── venv/                      # Python virtual environment (local)
```

## 📋 File Counts

| Category | Files | Purpose |
|----------|-------|---------|
| Application Layer | 4 | User-facing components |
| Interfaces | 3 | Abstract contracts |
| Services | 3 | Business logic implementations |
| Model Layer | 15+ | ML model and training |
| Data & Config | 5+ | Storage and settings |
| Documentation | 9 | Guides and references |
| Tests | 2+ | Quality assurance |
| Scripts | 2-4 | Deployment utilities |

## 🎨 Layer Responsibilities

### 1️⃣ Application Layer
**Purpose**: User interface and interaction
**Files**: `app.py`, `auth.py`, `database.py`, `predictor.py`
**Depends On**: Services Layer
**SOLID**: Facade pattern, DIP

### 2️⃣ Interfaces Layer
**Purpose**: Define contracts and abstractions
**Files**: `interfaces/*.py`
**Depends On**: Nothing (pure abstractions)
**SOLID**: ISP, DIP

### 3️⃣ Services Layer
**Purpose**: Business logic implementation
**Files**: `services/*.py`
**Depends On**: Interfaces Layer
**SOLID**: SRP, OCP, DIP, LSP

### 4️⃣ Model Layer
**Purpose**: Deep learning model and training
**Files**: `src/*.py`, `scripts/*.py`, `models/*.pth`
**Depends On**: PyTorch, Configuration
**SOLID**: SRP

### 5️⃣ Data Layer
**Purpose**: Data storage and configuration
**Files**: `config/*.json`, `data/*.db`, `datasets/`
**Depends On**: Nothing
**SOLID**: SRP

### 6️⃣ Testing Layer
**Purpose**: Automated testing
**Files**: `tests/*.py`
**Depends On**: All layers
**SOLID**: DIP (uses mocks)

### 7️⃣ Documentation Layer
**Purpose**: Knowledge and guides
**Files**: `docs/*.md`
**Depends On**: Nothing
**SOLID**: N/A

## 🔄 Dependency Flow

```
┌─────────────────────────────────────┐
│      Application Layer (UI)         │
│  app.py, auth.py, predictor.py      │
└────────────┬────────────────────────┘
             │ depends on
             ↓
┌─────────────────────────────────────┐
│       Services Layer (Logic)        │
│  AuthService, UserRepo, Predictor   │
└────────────┬────────────────────────┘
             │ implements
             ↓
┌─────────────────────────────────────┐
│    Interfaces Layer (Contracts)     │
│  IAuthService, IRepository, etc.    │
└─────────────────────────────────────┘

        ┌─────────────┐
        │ Model Layer │ ← used by Services
        └─────────────┘

        ┌─────────────┐
        │ Data Layer  │ ← used by Services
        └─────────────┘
```

## 📁 Quick Access Guide

### 🎯 Want to...

**Run the application?**
→ `run_streamlit.ps1` or `app.py`

**Train a new model?**
→ `scripts/train_model_transfer.py`

**Test predictions?**
→ `scripts/test_single_image.py`

**Learn SOLID principles?**
→ `docs/SOLID_QUICK_REFERENCE.md`

**Understand architecture?**
→ `docs/SOLID_REFACTORING_SUMMARY.md`

**Add new features?**
→ Create in `interfaces/` → implement in `services/` → use in `app.py`

**Configure model?**
→ `config/model_config.json`

**View training results?**
→ `models/training_history.json`

**Check user database?**
→ `data/users.db`

## 🧹 Clean Structure Benefits

✅ **Easy Navigation** - Logical folder organization
✅ **Clear Separation** - Each layer has distinct responsibility
✅ **SOLID Compliance** - Follows all SOLID principles
✅ **Scalable** - Easy to add new features
✅ **Maintainable** - Quick to locate and modify code
✅ **Testable** - Clear testing boundaries
✅ **Professional** - Enterprise-grade structure

## 📊 File Organization Rules

1. **Application files** (app.py, auth.py, etc.) → Root
2. **Interfaces** → `interfaces/` folder
3. **Services** → `services/` folder
4. **Model code** → `src/` folder
5. **Training scripts** → `scripts/` folder
6. **Trained models** → `models/` folder
7. **Configuration** → `config/` folder
8. **Runtime data** → `data/` folder
9. **Documentation** → `docs/` folder
10. **Tests** → `tests/` folder

## 🎓 Best Practices

- Keep root directory clean (only essential files)
- Group related files in folders
- Use clear, descriptive folder names
- Maintain separation of concerns
- Follow SOLID principles
- Document changes in appropriate docs
- Use .gitignore for generated files

---

**Last Updated**: December 17, 2025
**Structure Version**: 2.0 (SOLID Refactored)
