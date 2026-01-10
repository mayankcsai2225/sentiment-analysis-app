# 🚀 Deploy to Hugging Face Spaces (Free)

This guide will help you deploy your Sentiment Analysis application to Hugging Face Spaces for free.

## ✅ Prerequisites

- A Hugging Face account (free at [huggingface.co](https://huggingface.co))
- Your project code ready

## 📋 Step-by-Step Deployment

### Step 1: Create a Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click **"Sign Up"** (or **"Log In"** if you already have an account)
3. Complete the registration (it's free!)

### Step 2: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"** button
3. Fill in the form:
   - **Space name**: `sentiment-analysis-ml` (or your preferred name)
   - **SDK**: Select **"Streamlit"**
   - **Visibility**: **Public** (required for free tier)
   - **Hardware**: **CPU basic** (free tier)
4. Click **"Create Space"**

### Step 3: Upload Your Code

You have two options:

#### Option A: Using Git (Recommended)

1. **Initialize git in your project** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Hugging Face Spaces"
   ```

2. **Add Hugging Face as remote**:
   ```bash
   git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-ml
   ```
   Replace `YOUR_USERNAME` with your Hugging Face username.

3. **Push to Hugging Face**:
   ```bash
   git push huggingface main
   ```

#### Option B: Using Web Interface

1. In your Space, click **"Files and versions"** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload all necessary files:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md` (or use the provided `README_HUGGINGFACE.md`)
   - All Python modules (`analyzer.py`, `utils.py`, etc.)
   - `models/` directory (with model files)
   - `.streamlit/config.toml`

### Step 4: Configure Your Space

1. **Update README.md**:
   - Copy content from `README_HUGGINGFACE.md` to your Space's `README.md`
   - Or use the web editor to create one with the YAML frontmatter

2. **Verify requirements.txt**:
   - Ensure all dependencies are listed
   - The spaCy model should be included as a direct URL

3. **Check file structure**:
   ```
   your-space/
   ├── streamlit_app.py
   ├── requirements.txt
   ├── README.md
   ├── analyzer.py
   ├── utils.py
   ├── config.py
   ├── models/
   │   └── model.joblib
   └── .streamlit/
       └── config.toml
   ```

### Step 5: Wait for Build

- Hugging Face will automatically build your Space
- This usually takes 2-5 minutes
- You can monitor progress in the "Logs" tab

### Step 6: Access Your App

Once built, your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-ml
```

## 🔧 Important Notes for Hugging Face Spaces

### File Size Limits

- **Free tier**: 50GB total storage per user
- **Model files**: Should be under reasonable size
- **FastText model**: Will download automatically (excluded from repo)

### Requirements

- Use `requirements.txt` (not `requirements-deploy.txt`)
- Python version is managed by Hugging Face (usually 3.10 or 3.11)
- No need for `runtime.txt` or `packages.txt`

### Model Files

- **Small models** (< 100MB): Can be committed to the Space
- **Large models**: Should use Hugging Face Model Hub or download on first run
- Your `model.joblib` should be fine to include

### Environment Variables

If needed, you can set environment variables in:
- Space Settings → Variables and secrets

## 🐛 Troubleshooting

### Build Fails

1. **Check logs** in the "Logs" tab
2. **Verify requirements.txt** has all dependencies
3. **Check file paths** are relative (not absolute)

### App Won't Start

1. **Check main file**: Should be `streamlit_app.py`
2. **Verify imports**: All modules should be present
3. **Check model paths**: Should be relative to project root

### Model Not Found

1. **Verify model files** are uploaded
2. **Check file paths** in `config.py`
3. **Ensure models directory** is included

## 📊 Comparison: Streamlit Cloud vs Hugging Face Spaces

| Feature | Streamlit Cloud | Hugging Face Spaces |
|---------|----------------|---------------------|
| **Free Tier** | ✅ Yes | ✅ Yes |
| **Auto-deploy** | ✅ On git push | ✅ On git push |
| **Storage** | 1GB per app | 50GB total |
| **Hardware** | Shared | CPU/GPU options |
| **Community** | Streamlit users | ML/AI community |
| **Best For** | Streamlit apps | ML/AI demos |

## 🎉 Success!

Your app is now live on Hugging Face Spaces! 

- ✅ Free hosting
- ✅ Auto-updates on git push
- ✅ Public URL to share
- ✅ Part of the Hugging Face ML community

---

**Need help?** Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces) or open an issue.

