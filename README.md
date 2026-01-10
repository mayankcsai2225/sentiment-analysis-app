---
title: Sentiment Analysis ML
emoji: 🎯
colorFrom: red
colorTo: purple
sdk: streamlit
sdk_version: 1.52.2
app_file: streamlit_app.py
pinned: false
license: mit
---

# 🎯 Product Review Sentiment Analysis

An advanced ML-powered sentiment analysis application that analyzes product reviews using multiple machine learning models. Built with Streamlit, featuring rich visualizations, batch processing, and model explainability.

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.25+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🤖 Multiple ML Models**: Choose between Custom Logistic Regression or DistilBERT (Hugging Face Transformers)
- **📊 Rich Visualizations**: Interactive charts, word clouds, and sentiment breakdowns
- **📝 Single Review Analysis**: Analyze individual product reviews with detailed insights
- **📁 Batch Processing**: Upload CSV files for bulk sentiment analysis
- **🔬 Model Explainability**: LIME-based explanations to understand model predictions
- **🎯 Feature Extraction**: Automatically detects and analyzes product features mentioned in reviews
- **🌐 Multilingual Support**: Language detection and support for multiple languages
- **📈 Analytics Dashboard**: Comprehensive statistics and feedback tracking

## 🚀 Live Demo

This app is deployed on Hugging Face Spaces! Try it out:
**[🔗 Open the App](https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis-ml)**

*Replace YOUR_USERNAME with your Hugging Face username*

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features in Detail](#features-in-detail)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sentiment-analysis-ml.git
   cd sentiment-analysis-ml
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`

## 💻 Usage

### Single Review Analysis

1. Select "Single Review" mode in the sidebar
2. Enter or paste a product review in the text area
3. Choose your preferred model (Logistic Regression or DistilBERT)
4. Click "Analyze Review"
5. View detailed sentiment analysis, feature extraction, and visualizations

### Batch CSV Analysis

1. Select "Batch CSV Upload" mode
2. Upload a CSV file with reviews (format: `reviewText, rating`)
3. Click "Analyze All Reviews"
4. Explore comprehensive analytics and export results

### Model Comparison

1. Select "Model Comparison" mode
2. Enter a review text
3. Compare predictions from different models side-by-side

## 🎨 Features in Detail

### Sentiment Analysis
- Sentence-level sentiment classification
- Overall sentiment aggregation
- Confidence scores for predictions

### Feature Extraction
- Automatic detection of product features (camera, battery, display, etc.)
- Feature-specific sentiment analysis
- Related terms identification

### Visualizations
- Sentiment distribution pie charts
- Feature frequency bar charts
- Feature-sentiment heatmaps
- Word clouds for positive/negative reviews

### Model Explainability
- LIME-based explanations
- Word importance visualization
- Prediction reasoning

## 🚀 Deployment

### Hugging Face Spaces (Recommended - Free)

1. **Create a Hugging Face account** at [huggingface.co](https://huggingface.co)

2. **Create a new Space**:
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Select "Streamlit" as SDK
   - Set visibility to "Public"

3. **Upload your code**:
   - Use Git: `git push huggingface main`
   - Or upload files via web interface

4. **Your app will be live in 2-5 minutes!**

For detailed instructions, see [HUGGINGFACE_DEPLOY.md](HUGGINGFACE_DEPLOY.md).

### Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set Main file path to: `streamlit_app.py`
6. Click "Deploy"

For detailed instructions, see [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md).

## 📁 Project Structure

```
sentiment_analysis_ml_part-master/
│
├── streamlit_app.py          # Main Streamlit application
├── analyzer.py                # Core sentiment analysis engine
├── preprocess.py              # Text preprocessing utilities
├── feature_extraction.py      # Feature extraction module
├── classifiation.py           # Classification logic
├── visualizations.py          # Visualization functions
├── utils.py                   # Utility functions
├── config.py                  # Configuration settings
│
├── models/                    # ML model files
│   └── model.joblib          # Trained logistic regression model
│
├── csv_files/                 # Sample CSV data files
│
├── requirements.txt           # Python dependencies
├── README.md                  # This file (with HF Spaces config)
│
└── .streamlit/
    └── config.toml           # Streamlit configuration
```

## 🔧 Technologies Used

### Core ML Libraries
- **scikit-learn**: Machine learning models
- **spaCy**: NLP and text processing
- **FastText**: Word embeddings
- **Transformers**: Hugging Face models (DistilBERT)

### Web Framework
- **Streamlit**: Web application framework

### Visualization
- **Plotly**: Interactive charts
- **Matplotlib**: Static visualizations
- **WordCloud**: Word cloud generation

### Model Explainability
- **LIME**: Local interpretable model explanations

### Data Processing
- **pandas**: Data manipulation
- **numpy**: Numerical computing

## 📊 Model Information

### Custom Logistic Regression Model
- Trained on product review dataset
- Feature-based sentiment classification
- Fast inference time
- Good interpretability

### DistilBERT Model
- Pre-trained on SST-2 dataset
- Fine-tuned for sentiment analysis
- High accuracy
- Requires more computational resources

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Hugging Face](https://huggingface.co/) for pre-trained models and Spaces hosting
- [spaCy](https://spacy.io/) for NLP tools
- [FastText](https://fasttext.cc/) for word embeddings

## 📧 Contact

For questions or support, please open an issue on GitHub or Hugging Face.

---

**Made with ❤️ using Streamlit and Python**
