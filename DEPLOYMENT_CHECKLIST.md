# ✅ Deployment Checklist

Use this checklist to ensure your project is ready for Streamlit Cloud deployment.

## 📁 File Structure

- [ ] `streamlit_app.py` exists in root directory
- [ ] `requirements.txt` exists and is up to date
- [ ] `.streamlit/config.toml` exists
- [ ] `README.md` exists (documentation)
- [ ] `packages.txt` exists (if system dependencies needed)
- [ ] `setup.sh` exists (for post-install scripts)

## 🔧 Configuration

- [ ] All dependencies listed in `requirements.txt`
- [ ] spaCy model download handled (via `setup.sh` or manual)
- [ ] File paths in `config.py` are relative (not absolute)
- [ ] No hardcoded secrets in code

## 📦 Model Files

- [ ] `models/model.joblib` exists
- [ ] `models/fasttext_model_cbow.bin` exists
- [ ] Model files are ready to be committed (check `.gitignore`)
- [ ] Model file sizes are reasonable (< 500MB total recommended)

## 🗂️ Git Repository

- [ ] Repository is on GitHub
- [ ] All code is committed
- [ ] `.gitignore` allows model files (for deployment)
- [ ] Main branch is `main` or `master`

## 🧪 Testing

- [ ] App runs locally: `streamlit run streamlit_app.py`
- [ ] All imports work correctly
- [ ] Models load successfully
- [ ] No critical errors in console

## 📝 Documentation

- [ ] `README.md` is complete
- [ ] Deployment instructions are clear
- [ ] Dependencies are documented

## 🚀 Ready to Deploy?

If all items are checked, you're ready!

1. **Prepare repository** (if not done):
   ```bash
   cp .gitignore.deploy .gitignore
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy"

3. **Wait 5-10 minutes** for first deployment

4. **Access your app** at `https://your-repo-name.streamlit.app`

---

**Need help?** See [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md) for detailed instructions.

