#!/bin/bash
# Post-install script for Streamlit Cloud
# Downloads spaCy model after dependencies are installed

echo "📦 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

echo "✅ spaCy model downloaded successfully!"

