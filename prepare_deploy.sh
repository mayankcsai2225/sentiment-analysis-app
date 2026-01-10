#!/bin/bash
# Bash script to prepare for deployment
# This script helps prepare your repository for deployment

echo "🚀 Preparing repository for deployment..."

# Backup current .gitignore
if [ -f .gitignore ]; then
    cp .gitignore .gitignore.backup
    echo "✅ Backed up .gitignore"
fi

# Use deployment-friendly .gitignore
if [ -f .gitignore.deploy ]; then
    cp .gitignore.deploy .gitignore
    echo "✅ Updated .gitignore for deployment"
else
    echo "⚠️  .gitignore.deploy not found, skipping..."
fi

# Check if models exist
if [ -f "models/model.joblib" ]; then
    echo "✅ Found model.joblib"
else
    echo "⚠️  model.joblib not found in models/ directory"
fi

if [ -f "models/fasttext_model_cbow.bin" ]; then
    echo "✅ Found fasttext_model_cbow.bin"
else
    echo "⚠️  fasttext_model_cbow.bin not found in models/ directory"
fi

echo ""
echo "📋 Next steps:"
echo "1. Review the changes: git status"
echo "2. Add all files: git add ."
echo "3. Commit: git commit -m 'Ready for deployment'"
echo "4. Push: git push origin main"
echo "5. Deploy on Streamlit Cloud: https://share.streamlit.io"
echo ""
echo "✨ Ready to deploy!"

