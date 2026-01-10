# 🚀 Quick Push & Deploy Guide

## ✅ Step 1: Create GitHub Repository

1. Go to **[github.com/new](https://github.com/new)**
2. Fill in:
   - **Repository name**: `sentiment-analysis-ml`
   - **Description**: "Advanced ML-powered sentiment analysis application"
   - **Visibility**: ✅ **Public** (required for free Streamlit Cloud)
   - ❌ **DO NOT** check "Add a README file"
   - ❌ **DO NOT** check "Add .gitignore"
   - ❌ **DO NOT** check "Choose a license"
3. Click **"Create repository"**

## ✅ Step 2: Push to GitHub

**Copy and run these commands** (replace `YOUR_USERNAME` with your GitHub username):

```powershell
# Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/sentiment-analysis-ml.git

# Push to GitHub
git push -u origin main
```

**If you get authentication errors**, GitHub may ask for:
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)
  - Create one at: https://github.com/settings/tokens
  - Select scope: `repo`

## ✅ Step 3: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: **[share.streamlit.io](https://share.streamlit.io)**
   - Click **"Sign in"** → Sign in with GitHub

2. **Create New App**
   - Click **"New app"** button

3. **Configure**
   - **Repository**: Select `YOUR_USERNAME/sentiment-analysis-ml`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **Python version**: `3.11` (or latest)

4. **Deploy**
   - Click **"Deploy"**
   - Wait 5-10 minutes (first deployment takes longer)

5. **Access Your App**
   - Your app will be live at: `https://sentiment-analysis-ml.streamlit.app`

## 🎉 Done!

Your app is now:
- ✅ On GitHub
- ✅ Deployed on Streamlit Cloud
- ✅ Publicly accessible
- ✅ Auto-updates on git push

---

**Need help?** See [GITHUB_PUSH_INSTRUCTIONS.md](GITHUB_PUSH_INSTRUCTIONS.md) for detailed troubleshooting.

