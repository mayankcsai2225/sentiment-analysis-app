"""
Configuration settings for the Sentiment Analysis Application
"""
import os
from pathlib import Path

# Environment detection
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Base Directory
BASE_DIR = Path(__file__).parent

# Model Paths
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "model.joblib"
FASTTEXT_MODEL_PATH = MODELS_DIR / "fasttext_model.bin"
TRANSFORMERS_MODEL_PATH = MODELS_DIR / "transformers_model"

# Data Paths
CSV_DIR = BASE_DIR / "csv_files"
TRAINING_DATA = CSV_DIR / "training.csv"

# Database
DB_PATH = BASE_DIR / "feedback.db"

# Model Settings (with environment variable overrides)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "logistic_regression")
TRANSFORMERS_MODEL_NAME = os.getenv(
    "TRANSFORMERS_MODEL_NAME", 
    "distilbert-base-uncased-finetuned-sst-2-english"
)
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.6"))

# Feature Extraction Settings
TOP_FEATURES_PERCENT = 0.05  # Top 5% of features
SIMILARITY_THRESHOLD = 0.64
ASSOCIATION_CONFIDENCE = 0.4

# Stopwords and preprocessing
STOPWORDS_ENABLED = True

# UI Configuration
APP_TITLE = "🎯 Product Review Sentiment Analysis"
APP_ICON = "🎯"
THEME = {
    "primaryColor": "#FF4B4B",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": "#262730",
    "font": "sans serif"
}

# Export Settings
EXPORT_FORMATS = ["CSV", "JSON", "PDF"]
MAX_UPLOAD_SIZE_MB = 200

# Performance
ENABLE_CACHING = os.getenv("ENABLE_CACHING", "True").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TITLE = "Sentiment Analysis API"
API_VERSION = "1.0.0"

# Explainability
ENABLE_SHAP = os.getenv("ENABLE_SHAP", "True").lower() == "true"
ENABLE_LIME = os.getenv("ENABLE_LIME", "True").lower() == "true"
MAX_SHAP_SAMPLES = int(os.getenv("MAX_SHAP_SAMPLES", "100"))

# Multilingual
ENABLE_MULTILINGUAL = os.getenv("ENABLE_MULTILINGUAL", "True").lower() == "true"
SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "it", "pt"]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create directories if they don't exist
MODELS_DIR.mkdir(exist_ok=True)
CSV_DIR.mkdir(exist_ok=True)
