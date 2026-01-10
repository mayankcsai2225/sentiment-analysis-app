#!/bin/bash
# Setup script for Streamlit Cloud deployment
# Downloads spacy model and prepares environment

echo "🚀 Setting up environment for Streamlit Cloud..."

# Download spacy model
echo "📦 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete!"
