# ⚡ Quick Deploy to Hugging Face Spaces

## 🚀 Fastest Way (3 Steps)

### Step 1: Create Space (2 minutes)

1. Go to **[huggingface.co/spaces](https://huggingface.co/spaces)**
2. Click **"Create new Space"**
3. Fill in:
   - **Space name**: `sentiment-analysis-ml`
   - **SDK**: **Streamlit**
   - **Visibility**: **Public**
   - **Hardware**: **CPU basic** (free)
4. Click **"Create Space"**

### Step 2: Push Code (1 minute)

```bash
# Add Hugging Face as remote (replace YOUR_USERNAME)
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-ml

# Push to Hugging Face
git push huggingface main
```

**Or upload files via web interface:**
- Go to your Space → "Files and versions" → "Add file" → "Upload files"

### Step 3: Wait (2-5 minutes)

Hugging Face will automatically build your Space. Monitor progress in the "Logs" tab.

## ✅ Done!

Your app is live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-ml
```

## 📋 Required Files

Make sure these files are in your Space:
- ✅ `streamlit_app.py` (main app)
- ✅ `requirements.txt` (dependencies)
- ✅ `README.md` (with YAML frontmatter)
- ✅ All Python modules
- ✅ `models/model.joblib` (your trained model)
- ✅ `.streamlit/config.toml` (optional)

## 🎉 That's It!

Your app is now:
- ✅ Live on Hugging Face Spaces
- ✅ Free forever
- ✅ Auto-updates on git push
- ✅ Publicly accessible

---

**Need detailed instructions?** See [HUGGINGFACE_DEPLOY.md](HUGGINGFACE_DEPLOY.md)

