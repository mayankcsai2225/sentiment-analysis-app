# Free Deployment Guide

This guide will help you deploy your Sentiment Analysis application for free using various platforms.

## 🚀 Option 1: Streamlit Cloud (Recommended - Easiest)

Streamlit Cloud is the easiest and most straightforward option for deploying Streamlit apps. It's completely free and requires no credit card.

### Prerequisites
- A GitHub account
- Your project pushed to a GitHub repository

### Steps

1. **Prepare your repository:**
   - Make sure your models are committed (temporarily remove them from `.gitignore` if needed)
   - Ensure `requirements.txt` or `requirements-deploy.txt` is in the root
   - Ensure `streamlit_app.py` is in the root
   - Ensure `.streamlit/config.toml` exists

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

3. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set Main file path to: `streamlit_app.py`
   - Click "Deploy"
   - Wait for deployment (first time may take 5-10 minutes)

4. **Your app will be live at:** `https://your-app-name.streamlit.app`

### Important Notes for Streamlit Cloud:
- Models must be committed to the repository (they have a 1GB limit per app)
- First deployment may take longer due to dependency installation
- The app will auto-update when you push to your main branch

---

## 🌐 Option 2: Render (Free Tier)

Render offers a free tier with some limitations (spins down after 15 minutes of inactivity).

### Steps

1. **Create a Render account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** sentiment-analysis (or your choice)
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements-deploy.txt && python -m spacy download en_core_web_sm`
     - **Start Command:** `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
   - Click "Create Web Service"

3. **Your app will be live at:** `https://your-app-name.onrender.com`

### Render Free Tier Limitations:
- Spins down after 15 minutes of inactivity
- Cold starts can take 30-60 seconds
- 750 hours/month free (enough for always-on if you're the only user)

---

## 🚂 Option 3: Railway (Free Tier with $5 Credit)

Railway offers $5 free credit monthly, which is usually enough for small apps.

### Steps

1. **Create a Railway account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect it's a Python app
   - Add environment variable: `PORT=8501`
   - Railway will automatically deploy

3. **Configure:**
   - In Settings → Deploy, set Start Command:
     ```
     streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
     ```

---

## 🦅 Option 4: Fly.io (Free Tier)

Fly.io offers a free tier with 3 shared-cpu VMs.

### Steps

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Login and Launch:**
   ```bash
   fly auth login
   fly launch
   ```

3. **Create `fly.toml`:**
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 8501
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[services]]
     protocol = "tcp"
     internal_port = 8501
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

---

## 📦 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All model files are in the `models/` directory
- [ ] `requirements.txt` or `requirements-deploy.txt` is up to date
- [ ] `.streamlit/config.toml` exists
- [ ] `streamlit_app.py` is in the root directory
- [ ] All dependencies are listed in requirements file
- [ ] Test locally: `streamlit run streamlit_app.py`

### Important: Model Files

For deployment, you may need to temporarily allow model files in git:

1. Edit `.gitignore` and comment out or remove:
   ```
   # models/*.joblib
   # models/*.bin
   ```

2. Commit models:
   ```bash
   git add models/
   git commit -m "Add model files for deployment"
   ```

3. After deployment, you can restore `.gitignore` if desired

---

## 🔧 Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check that spacy model is downloaded: `python -m spacy download en_core_web_sm`

2. **App crashes on startup:**
   - Check logs in the deployment platform
   - Ensure model files are present
   - Verify file paths in `config.py` are relative

3. **Slow loading:**
   - First load is always slower (dependencies installation)
   - Consider using lighter models for faster startup

4. **Memory issues:**
   - Some platforms have memory limits on free tier
   - Consider optimizing model loading or using smaller models

---

## 🎯 Recommended: Streamlit Cloud

For this project, **Streamlit Cloud is the best choice** because:
- ✅ Completely free
- ✅ No credit card required
- ✅ Easy setup (just connect GitHub)
- ✅ Auto-deploys on git push
- ✅ Built specifically for Streamlit apps
- ✅ No cold starts
- ✅ Generous free tier

---

## 📝 Quick Start (Streamlit Cloud)

```bash
# 1. Ensure models are tracked (temporarily)
# Edit .gitignore to allow models

# 2. Commit everything
git add .
git commit -m "Ready for deployment"
git push origin main

# 3. Go to share.streamlit.io and deploy!
```

Your app will be live in ~5-10 minutes! 🎉

