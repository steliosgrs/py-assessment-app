"""
Configuration settings for the application.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SHARED_DIR = PROJECT_ROOT / "shared"
STORAGE_DIR = PROJECT_ROOT / "storage"

# Application settings
APP_NAME = "Multi-Framework App"
APP_VERSION = "0.1.0"

# Security settings
SECRET_KEY = os.environ.get("SECRET_KEY", "development-secret-key-change-in-production")
SESSION_COOKIE_NAME = "app_session"
SESSION_EXPIRY_DAYS = 30

# Firebase settings
FIREBASE_CREDENTIALS = os.environ.get(
    "FIREBASE_CREDENTIALS", "firebase-credentials.json"
)
FIREBASE_STORAGE_BUCKET = os.environ.get(
    "FIREBASE_STORAGE_BUCKET", "your-project-id.appspot.com"
)

# Streamlit settings
STREAMLIT_PORT = int(os.environ.get("STREAMLIT_PORT", "8501"))
STREAMLIT_THEME = {
    "primaryColor": "#1E88E5",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F5F5F5",
    "textColor": "#212121",
    "font": "sans-serif",
}

# Taipy settings (for future use)
TAIPY_PORT = int(os.environ.get("TAIPY_PORT", "5000"))
