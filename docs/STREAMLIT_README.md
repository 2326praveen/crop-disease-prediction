  # Streamlit Web Application - Quick Start Guide

## Overview
This Streamlit application provides a complete web interface for the Crop Disease Prediction System with user authentication, image upload, and AI-powered disease prediction.

## Features

### ✅ Implemented Features
- **User Authentication**: Login and registration with SQLite database
- **Home Page**: Welcome page with system overview
- **Upload & Predict Page**: Image upload and disease prediction
- **About Page**: System information and model details
- **Secure Logout**: Session management

### 🔐 Authentication
- SQLite database for user credential storage
- Password hashing using SHA-256
- Session-based authentication
- Registration with username validation

### 📤 Prediction Features
- Multiple image upload support (JPG, JPEG, PNG)
- Real-time disease prediction
- Confidence scores and probability distributions
- Disease information and treatment recommendations
- Support for 3 rice diseases: Bacterial Blight, Blast, Brown Spot

## Running the Application

### 1. Ensure Model is Trained
Make sure you have a trained model at:
```
models/best_model.pth
```

### 2. Install Dependencies
```powershell
pip install streamlit torch torchvision pillow numpy matplotlib
```

### 3. Run the Application
```powershell
streamlit run app.py
```

Or from any directory:
```powershell
cd "c:\Users\user\Downloads\cnn-pytorch\cnn-pytorch-main"
streamlit run app.py
```

### 4. Access the Application
The application will open in your browser at:
```
http://localhost:8501
```

## First Time Usage

### Create an Account
1. Click on the **Register** tab
2. Enter a username and password (minimum 4 characters)
3. Optionally add an email
4. Click **Register**

### Login
1. Enter your username and password
2. Click **Login**

### Upload and Predict
1. Navigate to **Upload & Predict** in the sidebar
2. Upload rice leaf images (supports multiple files)
3. Click **Analyze Images**
4. View predictions, confidence scores, and treatment recommendations

## Application Structure

```
app.py           - Main Streamlit application with UI
auth.py          - Authentication module (login/register/logout)
database.py      - SQLite database operations
predictor.py     - Model loading and prediction logic
users.db         - SQLite database (auto-created on first run)
```

## Pages

### Home Page
- Welcome message with user greeting
- Feature overview
- Disease information cards
- Model performance statistics

### Upload & Predict Page
- File upload widget (supports multiple images)
- Progress bar during analysis
- Results display with:
  - Image preview
  - Predicted disease class
  - Confidence score
  - All class probabilities
  - Disease information
  - Treatment recommendations

### About Page
- Model architecture details
- How it works explanation
- Technology stack information
- System statistics

## Database

The application uses SQLite for user management:

**Table: users**
- id (PRIMARY KEY)
- username (UNIQUE)
- password (hashed)
- email
- created_at (timestamp)

Database file: `users.db` (auto-created on first run)

## Security Notes

- Passwords are hashed using SHA-256 before storage
- Session state managed by Streamlit
- Database file excluded from git via .gitignore
- No plain-text password storage

## Troubleshooting

### Model Not Found Error
If you see "Error loading model", ensure:
- `models/best_model.pth` exists
- `config/class_names.json` exists
- Model was trained with 3 classes

### Database Issues
If login/registration fails:
- Delete `users.db` to reset the database
- Restart the application

### Port Already in Use
If port 8501 is busy, specify a different port:
```powershell
streamlit run app.py --server.port 8502
```

## Customization

### Change Supported Image Formats
Edit `app.py` line with `file_uploader`:
```python
type=['jpg', 'jpeg', 'png', 'bmp']  # Add more formats
```

### Modify Disease Information
Edit `predictor.py` in the `get_disease_info()` method

### Adjust Theme
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#4CAF50"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"
```

## Performance

- Model loads once per session (cached in session_state)
- Fast predictions (~0.1-0.5s per image on CPU)
- Supports batch processing of multiple images
- Lightweight SQLite database

## Future Enhancements

Possible improvements:
- Video upload and frame-by-frame analysis
- Export results to PDF/CSV
- Prediction history dashboard
- User profile management
- Admin panel for user management
- Multi-language support

## Notes

- First user registration creates the database automatically
- Session persists until logout or browser refresh
- Images are processed in memory (not saved to disk)
- Compatible with both CPU and GPU (automatically detected)
