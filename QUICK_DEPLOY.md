# 🚀 Quick Deployment Guide

## Fastest Way: Streamlit Cloud (5 minutes)

### Step 1: Prepare Your Code

1. **Allow model files in git** (temporarily):
   ```bash
   # Backup your current .gitignore
   cp .gitignore .gitignore.backup
   
   # Use deployment-friendly .gitignore
   cp .gitignore.deploy .gitignore
   ```

2. **Add and commit everything:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository
5. Set **Main file path:** `streamlit_app.py`
6. Click **"Deploy"**
7. Wait 5-10 minutes for first deployment

### Step 3: Access Your App

Your app will be live at: `https://your-repo-name.streamlit.app`

---

## Alternative: Render (Free Tier)

1. Go to **[render.com](https://render.com)**
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your repository
5. Use these settings:
   - **Build Command:** `pip install -r requirements-deploy.txt && python -m spacy download en_core_web_sm`
   - **Start Command:** `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
6. Click **"Create Web Service"**

---

## ⚠️ Important Notes

- **Model files must be committed** for deployment (they're excluded in default .gitignore)
- First deployment takes longer (installing dependencies)
- Streamlit Cloud has a 1GB limit per app
- Your app auto-updates when you push to GitHub

---

## 🐛 Troubleshooting

**"Module not found" error:**
- Make sure `requirements-deploy.txt` has all dependencies
- Check that spacy model downloads correctly

**App won't start:**
- Check deployment logs
- Ensure `streamlit_app.py` is in root directory
- Verify model files are present

**Need help?** Check `DEPLOYMENT.md` for detailed instructions.

