# 🚀 Streamlit Cloud Deployment Guide

Complete step-by-step guide to deploy your Sentiment Analysis app on Streamlit Cloud (100% Free).

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] GitHub account
- [ ] Project pushed to a GitHub repository
- [ ] Model files ready (`models/model.joblib` and `models/fasttext_model_cbow.bin`)
- [ ] All dependencies listed in `requirements.txt`
- [ ] `.streamlit/config.toml` file exists
- [ ] `streamlit_app.py` is in the root directory

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Repository

#### Option A: Use the Helper Script (Windows)

```powershell
# Run the preparation script
.\prepare_deploy.ps1

# Review changes
git status

# Add all files
git add .

# Commit
git commit -m "Ready for Streamlit Cloud deployment"

# Push to GitHub
git push origin main
```

#### Option B: Manual Preparation

1. **Temporarily allow model files in git:**

   ```bash
   # Backup your current .gitignore
   cp .gitignore .gitignore.backup
   
   # Use deployment-friendly .gitignore
   cp .gitignore.deploy .gitignore
   ```

2. **Add and commit all files:**

   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App**
   - Click the **"New app"** button
   - You'll see a form to configure your app

3. **Configure Your App**
   - **Repository**: Select your GitHub repository
   - **Branch**: Select `main` (or `master`)
   - **Main file path**: Enter `streamlit_app.py`
   - **Python version**: Select `3.11` (or latest available)
   - **Advanced settings** (optional):
     - You can add secrets/environment variables if needed
     - See `.streamlit/secrets.toml.example` for reference

4. **Deploy**
   - Click **"Deploy"** button
   - Wait 5-10 minutes for the first deployment
   - You'll see build logs in real-time

### Step 3: Access Your App

Once deployment completes:
- Your app URL will be: `https://your-repo-name.streamlit.app`
- You can share this URL with anyone
- The app auto-updates when you push to GitHub

## 🔧 Configuration Files

### Required Files

1. **`streamlit_app.py`** - Your main app file (must be in root)
2. **`requirements.txt`** - Python dependencies
3. **`.streamlit/config.toml`** - Streamlit configuration

### Optional Files

- **`packages.txt`** - System dependencies (if needed)
- **`setup.sh`** - Post-install script (for spacy model download)
- **`.streamlit/secrets.toml`** - Secrets (configured in Streamlit Cloud UI)

## 📝 Streamlit Cloud Settings

### Advanced Settings (Optional)

In Streamlit Cloud, you can configure:

1. **Secrets** (`.streamlit/secrets.toml`):
   - API keys
   - Database credentials
   - Environment variables

2. **Python Version**:
   - Select Python 3.11 (recommended)
   - Or latest available version

3. **Auto-redeploy**:
   - Enabled by default
   - App updates automatically on git push

## 🐛 Troubleshooting

### Build Fails

**Issue**: Build fails with "Module not found"
- **Solution**: Ensure all dependencies are in `requirements.txt`
- Check build logs for specific missing packages

**Issue**: spaCy model not found
- **Solution**: Add to `setup.sh` or use post-install command:
  ```bash
  python -m spacy download en_core_web_sm
  ```

### App Crashes on Startup

**Issue**: App crashes immediately
- **Solution**: 
  - Check logs in Streamlit Cloud dashboard
  - Verify model files are present
  - Ensure file paths are relative (not absolute)

**Issue**: "Model file not found"
- **Solution**: 
  - Ensure models are committed to git
  - Check `.gitignore` doesn't exclude model files
  - Verify model paths in `config.py`

### Performance Issues

**Issue**: App is slow to load
- **Solution**: 
  - First load is always slower (dependencies installation)
  - Consider using lighter models
  - Enable caching in your code

**Issue**: Memory errors
- **Solution**: 
  - Streamlit Cloud free tier has memory limits
  - Optimize model loading
  - Use smaller models if possible

## 📊 Monitoring

### View Logs

1. Go to your app on Streamlit Cloud
2. Click **"Manage app"**
3. View **"Logs"** tab for real-time logs
4. Check **"Metrics"** for performance data

### Update Your App

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Streamlit Cloud automatically redeploys
4. Wait 1-2 minutes for update

## 🔒 Security Best Practices

1. **Never commit secrets**:
   - Use `.streamlit/secrets.toml` (gitignored)
   - Configure secrets in Streamlit Cloud UI

2. **Keep dependencies updated**:
   - Regularly update `requirements.txt`
   - Check for security vulnerabilities

3. **Limit file uploads**:
   - Set max upload size in `config.py`
   - Validate user inputs

## 💡 Tips

1. **First Deployment**: Takes 5-10 minutes (installing dependencies)
2. **Subsequent Updates**: Usually 1-2 minutes
3. **Model Files**: Must be committed (Streamlit Cloud has 1GB limit per app)
4. **Auto-Updates**: Enabled by default when you push to GitHub
5. **Custom Domain**: Not available on free tier

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Deployment Troubleshooting](https://docs.streamlit.io/streamlit-cloud/troubleshooting)

## 🎉 Success!

Once deployed, your app will be:
- ✅ Publicly accessible
- ✅ Auto-updating on git push
- ✅ Free forever (no credit card needed)
- ✅ Scalable (handles traffic automatically)

---

**Need help?** Check the [DEPLOYMENT.md](DEPLOYMENT.md) for alternative platforms or open an issue on GitHub.

