# 🚀 Hugging Face Spaces Setup Guide

Your code is now in: **https://github.com/mayankcsai2225/sentiment-analysis-app**

## 📋 Two Ways to Deploy to Hugging Face Spaces

### Option 1: Direct Push to Hugging Face (Recommended)

Hugging Face Spaces has its own git repository. You can push directly to it.

#### Step 1: Create Space on Hugging Face

1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)**
2. Click **"Create new Space"**
3. Fill in:
   - **Space name**: `sentiment-analysis-app`
   - **SDK**: **Streamlit**
   - **Visibility**: **Public**
   - **Hardware**: **CPU basic** (free tier)
4. Click **"Create Space"**

#### Step 2: Push Code to Hugging Face Space

After creating the Space, Hugging Face will show you the git URL. Then run:

```bash
# Add Hugging Face Space as remote
git remote add huggingface https://huggingface.co/spaces/mayankcsai2225/sentiment-analysis-app

# Push to Hugging Face
git push huggingface main
```

**Note**: You'll need to authenticate with Hugging Face. Use a **User Access Token**:
- Get one at: https://huggingface.co/settings/tokens
- Use it as password when pushing

### Option 2: Connect GitHub Repo to Hugging Face

1. Create the Space (same as Option 1, Step 1)
2. In Space Settings → **"Repository"** → **"Connect to GitHub"**
3. Select your repository: `mayankcsai2225/sentiment-analysis-app`
4. Hugging Face will sync automatically

## ✅ Required Files for Hugging Face Spaces

Your repository already has all necessary files:

- ✅ `streamlit_app.py` - Main application
- ✅ `requirements.txt` - Dependencies (with spaCy model)
- ✅ `README.md` - With Hugging Face YAML frontmatter
- ✅ All Python modules
- ✅ Model files

## 🎯 Quick Deploy Commands

```bash
# Make sure you're in the project directory
cd C:\sentiment_analysis_ml_part-master

# Add Hugging Face remote (after creating Space)
git remote add huggingface https://huggingface.co/spaces/mayankcsai2225/sentiment-analysis-app

# Push to Hugging Face
git push huggingface main
```

## 📝 Important Notes

1. **Authentication**: You'll need a Hugging Face User Access Token
   - Create at: https://huggingface.co/settings/tokens
   - Use token as password when git asks

2. **README.md**: Already configured with Hugging Face YAML frontmatter

3. **Model Files**: 
   - `model.joblib` should be included (it's small)
   - FastText model will download automatically

4. **Build Time**: First build takes 3-5 minutes

## 🎉 After Deployment

Your app will be live at:
```
https://huggingface.co/spaces/mayankcsai2225/sentiment-analysis-app
```

## 🔄 Updating Your Space

To update your Space after making changes:

```bash
# Make changes locally
git add .
git commit -m "Update app"
git push huggingface main
```

Or if connected to GitHub, just push to GitHub and it auto-syncs!

---

**Need help?** See [HUGGINGFACE_DEPLOY.md](HUGGINGFACE_DEPLOY.md) for detailed instructions.

