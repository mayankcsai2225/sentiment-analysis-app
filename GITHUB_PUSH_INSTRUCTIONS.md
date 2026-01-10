# 🚀 GitHub Push & Deployment Instructions

## Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in:
   - **Repository name**: `sentiment-analysis-ml` (or your preferred name)
   - **Description**: "Advanced ML-powered sentiment analysis application"
   - **Visibility**: Public (required for free Streamlit Cloud)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add your GitHub repository as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sentiment-analysis-ml.git

# Push to GitHub
git push -u origin main
```

**Or if you prefer SSH:**
```bash
git remote add origin git@github.com:YOUR_USERNAME/sentiment-analysis-ml.git
git push -u origin main
```

## Step 3: Deploy on Streamlit Cloud

Once your code is on GitHub:

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click **"New app"** button
   - You'll see a deployment form

3. **Configure Your App**
   - **Repository**: Select `YOUR_USERNAME/sentiment-analysis-ml`
   - **Branch**: Select `main`
   - **Main file path**: Enter `streamlit_app.py`
   - **Python version**: Select `3.11` (or latest available)
   - **Advanced settings** (optional):
     - You can add secrets/environment variables if needed

4. **Deploy**
   - Click **"Deploy"** button
   - Wait 5-10 minutes for the first deployment
   - Watch the build logs in real-time

5. **Access Your App**
   - Once deployment completes, your app will be live at:
   - `https://sentiment-analysis-ml.streamlit.app` (or similar)
   - You can share this URL with anyone!

## ✅ Verification

After pushing, verify:
- [ ] All files are visible on GitHub
- [ ] `requirements.txt` is present
- [ ] `streamlit_app.py` is in the root
- [ ] `.streamlit/config.toml` exists
- [ ] Model files are included (check `models/` folder)

## 🎉 Success!

Your app will:
- ✅ Auto-update when you push to GitHub
- ✅ Be publicly accessible
- ✅ Be completely free (no credit card needed)
- ✅ Scale automatically

## 🆘 Troubleshooting

**Git push fails:**
- Make sure you've created the GitHub repository first
- Check your GitHub username is correct
- Verify you're authenticated (GitHub may ask for credentials)

**Streamlit Cloud build fails:**
- Check build logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `streamlit_app.py` is in the root directory

**App won't start:**
- Check logs in Streamlit Cloud
- Verify model files are committed
- Check file paths are relative (not absolute)

---

**Need help?** See [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md) for detailed troubleshooting.

