"""
Advanced Sentiment Analysis Engine with Multiple Models
"""
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import spacy
from spacy.pipeline import Sentencizer
import warnings
warnings.filterwarnings('ignore')

# Import existing modules
from preprocess import preprocess, construct_spacy_obj
import ft
import train
from feature_extraction import feature_extraction
from classifiation import classify

# Import config
import config

# For Hugging Face Transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available. Install with: pip install transformers torch")

# For language detection
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("langdetect not available. Install with: pip install langdetect")

# For explainability
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("SHAP not available. Install with: pip install shap")

try:
    from lime.lime_text import LimeTextExplainer
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False
    print("LIME not available. Install with: pip install lime")


class SentimentAnalyzer:
    """
    Comprehensive sentiment analysis engine with multiple model support
    """
    
    def __init__(self, model_type: str = "logistic_regression"):
        """
        Initialize analyzer
        
        Args:
            model_type: Type of model to use ("logistic_regression" or "transformers")
        """
        self.model_type = model_type
        
        # Load Spacy
        self.nlp = spacy.load('en_core_web_sm')
        sentencizer = Sentencizer(punct_chars=[".", "!", "?", "\n", "\r", ";"])
        if 'sentencizer' not in self.nlp.pipe_names:
            self.nlp.add_pipe('sentencizer', last=True)
        
        # Load FastText model
        self.ft_model = ft.get_model()
        
        # Load or train custom model
        self.custom_model = train.get_model(self.nlp, self.ft_model)
        
        # Load Hugging Face model if requested
        self.transformers_pipeline = None
        if model_type == "transformers" and TRANSFORMERS_AVAILABLE:
            self._load_transformers_model()
        
        # Initialize explainer
        self.lime_explainer = None
        if LIME_AVAILABLE:
            self.lime_explainer = LimeTextExplainer(class_names=["Negative", "Positive"])
    
    def _load_transformers_model(self):
        """Load Hugging Face transformers model"""
        try:
            self.transformers_pipeline = pipeline(
                "sentiment-analysis",
                model=config.TRANSFORMERS_MODEL_NAME,
                return_all_scores=True
            )
            print(f"Loaded transformers model: {config.TRANSFORMERS_MODEL_NAME}")
        except Exception as e:
            print(f"Error loading transformers model: {e}")
            self.transformers_pipeline = None
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Input text
            
        Returns:
            Language code (e.g., 'en', 'es')
        """
        if not LANGDETECT_AVAILABLE:
            return "en"
        
        try:
            lang = detect(text)
            return lang
        except LangDetectException:
            return "en"
    
    def analyze_single_review(self, text: str, model_type: Optional[str] = None) -> Dict:
        """
        Analyze a single review text
        
        Args:
            text: Review text
            model_type: Optional model type override
            
        Returns:
            Analysis results dictionary
        """
        if model_type is None:
            model_type = self.model_type
        
        # Detect language
        language = self.detect_language(text)
        
        # Preprocess
        from preprocess import preprocess_text
        processed_text = preprocess_text(text, self.nlp)
        
        if pd.isna(processed_text) or not processed_text:
            return {
                "error": "Text too short or invalid after preprocessing",
                "original_text": text
            }
        
        # Create DataFrame
        df = pd.DataFrame({
            'reviewText': [processed_text],
            'rating': [5]  # Dummy rating for analysis
        })
        
        # Construct Spacy objects
        df = construct_spacy_obj(df, self.nlp)
        
        # Extract features
        features = feature_extraction(df, self.ft_model, self.nlp)
        
        # Classify using selected model
        if model_type == "transformers" and self.transformers_pipeline:
            # Use transformers for overall sentiment
            overall_sentiment = self._predict_with_transformers(text)
        else:
            # Use custom model
            overall_sentiment = None
        
        # Get aspect-based classification
        results_df, more_than_one, no_cat = classify(df, features, self.custom_model)
        
        # Format results
        result = {
            "original_text": text,
            "processed_text": processed_text,
            "language": language,
            "model_used": model_type,
            "features": features,
            "classification": results_df.to_dict('records') if not results_df.empty else [],
            "overall_sentiment": overall_sentiment,
            "summary": {
                "total_sentences": len(results_df),
                "positive_count": len(results_df[results_df["sentiment"] == "Positive"]),
                "negative_count": len(results_df[results_df["sentiment"] == "Negative"]),
                "features_found": len(features)
            }
        }
        
        return result
    
    def _predict_with_transformers(self, text: str) -> Dict:
        """
        Predict sentiment using transformers
        
        Args:
            text: Input text
            
        Returns:
            Sentiment prediction dictionary
        """
        if not self.transformers_pipeline:
            return None
        
        try:
            results = self.transformers_pipeline(text[:512])[0]  # Limit to 512 tokens
            
            # Convert to standardized format
            sentiment_map = {
                "POSITIVE": "Positive",
                "NEGATIVE": "Negative",
                "LABEL_1": "Positive",
                "LABEL_0": "Negative"
            }
            
            max_result = max(results, key=lambda x: x['score'])
            
            return {
                "sentiment": sentiment_map.get(max_result['label'], max_result['label']),
                "confidence": max_result['score'],
                "all_scores": results
            }
        except Exception as e:
            print(f"Error in transformers prediction: {e}")
            return None
    
    def analyze_batch(self, df: pd.DataFrame, progress_callback=None) -> Dict:
        """
        Analyze batch of reviews
        
        Args:
            df: DataFrame with 'reviewText' and 'rating' columns
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Analysis results dictionary
        """
        # Preprocess all reviews
        total_reviews = len(df)
        if progress_callback:
            progress_callback(0, total_reviews, "Preprocessing reviews...")
        
        df = preprocess(df, self.nlp)
        
        if progress_callback:
            progress_callback(total_reviews * 0.3, total_reviews, "Constructing linguistic features...")
        
        # Construct Spacy objects
        df = construct_spacy_obj(df, self.nlp)
        
        if progress_callback:
            progress_callback(total_reviews * 0.5, total_reviews, "Extracting features...")
        
        # Extract features
        features = feature_extraction(df, self.ft_model, self.nlp)
        
        if progress_callback:
            progress_callback(total_reviews * 0.8, total_reviews, "Classifying sentiments...")
        
        # Classify
        results_df, more_than_one, no_cat = classify(df, features, self.custom_model)
        
        if progress_callback:
            progress_callback(total_reviews, total_reviews, "Complete!")
        
        # Format results
        from utils import format_results_for_display
        results = format_results_for_display(features, results_df)
        
        return results
    
    def explain_prediction(self, text: str, method: str = "lime") -> Dict:
        """
        Explain model prediction using LIME or SHAP
        
        Args:
            text: Input text
            method: Explanation method ("lime" or "shap")
            
        Returns:
            Explanation dictionary
        """
        if method == "lime" and self.lime_explainer:
            return self._explain_with_lime(text)
        elif method == "shap" and SHAP_AVAILABLE:
            return self._explain_with_shap(text)
        else:
            return {"error": f"Explanation method {method} not available"}
    
    def _explain_with_lime(self, text: str) -> Dict:
        """
        Explain prediction using LIME
        
        Args:
            text: Input text
            
        Returns:
            LIME explanation
        """
        try:
            # Create prediction function
            def predict_proba(texts):
                predictions = []
                for t in texts:
                    try:
                        pred = self.custom_model.predict([t])[0]
                        # Convert to probability-like scores
                        if pred == "Positive":
                            predictions.append([0.2, 0.8])
                        else:
                            predictions.append([0.8, 0.2])
                    except:
                        predictions.append([0.5, 0.5])
                return np.array(predictions)
            
            # Generate explanation
            exp = self.lime_explainer.explain_instance(
                text,
                predict_proba,
                num_features=10
            )
            
            # Extract important words
            explanation = {
                "method": "LIME",
                "important_words": exp.as_list(),
                "prediction": exp.predict_proba.tolist() if hasattr(exp, 'predict_proba') else None
            }
            
            return explanation
            
        except Exception as e:
            return {"error": f"LIME explanation failed: {str(e)}"}
    
    def _explain_with_shap(self, text: str) -> Dict:
        """
        Explain prediction using SHAP
        
        Args:
            text: Input text
            
        Returns:
            SHAP explanation
        """
        # SHAP implementation would go here
        # This is more complex and requires more setup
        return {"error": "SHAP explanation not yet implemented"}
    
    def compare_models(self, text: str) -> Dict:
        """
        Compare predictions from different models
        
        Args:
            text: Input text
            
        Returns:
            Comparison dictionary
        """
        results = {
            "text": text,
            "models": {}
        }
        
        # Custom model prediction
        custom_result = self.analyze_single_review(text, model_type="logistic_regression")
        results["models"]["custom_lr"] = {
            "name": "Custom Logistic Regression",
            "sentiment": custom_result.get("summary", {})
        }
        
        # Transformers prediction
        if TRANSFORMERS_AVAILABLE and self.transformers_pipeline:
            trans_result = self._predict_with_transformers(text)
            results["models"]["transformers"] = {
                "name": "DistilBERT",
                "sentiment": trans_result
            }
        
        return results


# Convenience functions for backward compatibility
_default_analyzer = None

def get_analyzer(model_type: str = "logistic_regression") -> SentimentAnalyzer:
    """Get or create sentiment analyzer instance"""
    global _default_analyzer
    if _default_analyzer is None or _default_analyzer.model_type != model_type:
        _default_analyzer = SentimentAnalyzer(model_type=model_type)
    return _default_analyzer


def analyze_text(text: str, model_type: str = "logistic_regression") -> Dict:
    """
    Analyze single text (convenience function)
    
    Args:
        text: Review text
        model_type: Model type to use
        
    Returns:
        Analysis results
    """
    analyzer = get_analyzer(model_type)
    return analyzer.analyze_single_review(text)


def analyze_csv(filepath: str, model_type: str = "logistic_regression", progress_callback=None) -> Dict:
    """
    Analyze CSV file (convenience function)
    
    Args:
        filepath: Path to CSV file
        model_type: Model type to use
        progress_callback: Optional progress callback
        
    Returns:
        Analysis results
    """
    df = pd.read_csv(filepath, header=None, names=['reviewText', 'rating'])
    analyzer = get_analyzer(model_type)
    return analyzer.analyze_batch(df, progress_callback)
