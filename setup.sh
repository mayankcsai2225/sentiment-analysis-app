#!/bin/bash
# Setup script for Streamlit Cloud deployment
# Downloads spacy model and FastText model

echo "🚀 Setting up environment for Streamlit Cloud..."

# Download spacy model
echo "📦 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# FastText model will be downloaded automatically by the application
# on first run if not present (handled in ft.py)
echo "ℹ️  FastText model will be downloaded automatically on first use"

echo "✅ Setup complete!"
