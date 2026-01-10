# ⚡ Deploy to Hugging Face Spaces NOW

## 🚀 Quick Steps (5 minutes)

### Step 1: Create Hugging Face Account (if needed)
- Go to [huggingface.co](https://huggingface.co) and sign up (free!)

### Step 2: Create Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Settings:
   - **Name**: `sentiment-analysis-app`
   - **SDK**: **Streamlit** ⚠️ Important!
   - **Visibility**: **Public**
   - **Hardware**: **CPU basic**
4. Click **"Create Space"**

### Step 3: Get Your Access Token
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Name: `spaces-deploy`
4. Type: **Write** (needed to push)
5. Click **"Generate token"**
6. **Copy the token** (you'll need it!)

### Step 4: Push Your Code

Open PowerShell in your project directory and run:

```powershell
# Navigate to project
cd C:\sentiment_analysis_ml_part-master

# Add Hugging Face remote (replace YOUR_USERNAME if different)
git remote add huggingface https://huggingface.co/spaces/mayankcsai2225/sentiment-analysis-app

# Push to Hugging Face
# When asked for password, paste your access token
git push huggingface main
```

**When prompted:**
- **Username**: `mayankcsai2225` (your HF username)
- **Password**: Paste your access token (not your actual password!)

### Step 5: Wait for Build
- Go to your Space page
- Click **"Logs"** tab
- Wait 3-5 minutes for build to complete

## ✅ Done!

Your app is live at:
**https://huggingface.co/spaces/mayankcsai2225/sentiment-analysis-app**

## 🎯 What's Already Ready

✅ All code pushed to: https://github.com/mayankcsai2225/sentiment-analysis-app
✅ README.md configured for Hugging Face
✅ requirements.txt includes spaCy model
✅ All dependencies ready

## 🆘 Troubleshooting

**"Permission denied" when pushing:**
- Make sure you're using a **Write** token (not Read)
- Check your username is correct

**"Repository not found":**
- Make sure you created the Space first
- Check the Space name matches

**Build fails:**
- Check the Logs tab in your Space
- Verify all files are pushed correctly

---

**Ready?** Follow the steps above! 🚀

