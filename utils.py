"""
Utility functions for sentiment analysis application
"""
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
import streamlit as st

import config


def validate_csv_file(file) -> Tuple[bool, str, Optional[pd.DataFrame]]:
    """
    Validate uploaded CSV file
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple of (is_valid, message, dataframe)
    """
    try:
        df = pd.read_csv(file, header=None, names=['reviewText', 'rating'])
        
        if df.empty:
            return False, "CSV file is empty", None
            
        if 'reviewText' not in df.columns:
            return False, "CSV must have 'reviewText' column", None
            
        # Check for minimum data
        if len(df) < 1:
            return False, "CSV must have at least 1 review", None
            
        return True, f"Valid CSV with {len(df)} reviews", df
        
    except Exception as e:
        return False, f"Error reading CSV: {str(e)}", None


def validate_single_review(text: str) -> Tuple[bool, str]:
    """
    Validate single review text
    
    Args:
        text: Review text
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not text or len(text.strip()) < 3:
        return False, "Review text must be at least 3 characters"
    
    if len(text) > 5000:
        return False, "Review text is too long (max 5000 characters)"
        
    return True, "Valid review text"


def format_results_for_display(features: Dict, results_df: pd.DataFrame) -> Dict:
    """
    Format analysis results for display
    
    Args:
        features: Feature dictionary
        results_df: Classification results dataframe
        
    Returns:
        Formatted results dictionary
    """
    formatted = {
        "features": {},
        "classification": [],
        "summary": {
            "total_sentences": len(results_df),
            "positive_count": 0,
            "negative_count": 0,
            "features_found": len(features)
        }
    }
    
    # Format features
    for feature, related in features.items():
        try:
            pos = len(results_df[(results_df["category"] == feature) & (results_df["sentiment"] == "Positive")])
            neg = len(results_df[(results_df["category"] == feature) & (results_df["sentiment"] == "Negative")])
            
            formatted["features"][feature] = {
                "related": related,
                "positives": pos,
                "negatives": neg,
                "total": pos + neg
            }
        except:
            formatted["features"][feature] = {
                "related": related,
                "positives": 0,
                "negatives": 0,
                "total": 0
            }
    
    # Format classifications
    for _, row in results_df.iterrows():
        formatted["classification"].append({
            "category": row["category"],
            "sentence": row["sentence"],
            "sentiment": row["sentiment"]
        })
        
        if row["sentiment"] == "Positive":
            formatted["summary"]["positive_count"] += 1
        else:
            formatted["summary"]["negative_count"] += 1
    
    return formatted


def export_to_csv(results: Dict, filename: str = "results.csv") -> str:
    """
    Export results to CSV
    
    Args:
        results: Results dictionary
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    # Create dataframe from classifications
    df = pd.DataFrame(results["classification"])
    
    # Add summary row
    summary_data = {
        "category": "SUMMARY",
        "sentence": f"Total: {results['summary']['total_sentences']} sentences",
        "sentiment": f"Positive: {results['summary']['positive_count']}, Negative: {results['summary']['negative_count']}"
    }
    df = pd.concat([df, pd.DataFrame([summary_data])], ignore_index=True)
    
    filepath = Path(filename)
    df.to_csv(filepath, index=False)
    return str(filepath)


def export_to_json(results: Dict, filename: str = "results.json") -> str:
    """
    Export results to JSON
    
    Args:
        results: Results dictionary
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    filepath = Path(filename)
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return str(filepath)


def create_feedback_table():
    """Create SQLite table for user feedback"""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            review_text TEXT,
            predicted_sentiment TEXT,
            actual_sentiment TEXT,
            rating INTEGER,
            comments TEXT
        )
    ''')
    
    conn.commit()
    conn.close()


def save_feedback(review_text: str, predicted: str, actual: str, rating: int, comments: str = ""):
    """
    Save user feedback to database
    
    Args:
        review_text: The review text
        predicted: Predicted sentiment
        actual: Actual sentiment (user-provided)
        rating: User rating of accuracy (1-5)
        comments: Optional user comments
    """
    create_feedback_table()
    
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedback (review_text, predicted_sentiment, actual_sentiment, rating, comments)
        VALUES (?, ?, ?, ?, ?)
    ''', (review_text, predicted, actual, rating, comments))
    
    conn.commit()
    conn.close()


def get_feedback_stats() -> Dict:
    """
    Get feedback statistics
    
    Returns:
        Dictionary with feedback stats
    """
    create_feedback_table()
    
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM feedback')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(rating) FROM feedback')
    avg_rating = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        SELECT COUNT(*) FROM feedback 
        WHERE predicted_sentiment = actual_sentiment
    ''')
    correct = cursor.fetchone()[0]
    
    conn.close()
    
    accuracy = (correct / total * 100) if total > 0 else 0
    
    return {
        "total_feedback": total,
        "average_rating": round(avg_rating, 2),
        "accuracy": round(accuracy, 2),
        "correct_predictions": correct
    }


@st.cache_data(ttl=config.CACHE_TTL)
def load_sample_data() -> pd.DataFrame:
    """Load sample data for testing"""
    sample_reviews = [
        # Positive reviews with various features
        ("Great phone with amazing camera quality! Battery life is excellent.", 5),
        ("Best phone I ever bought. Fast charging is incredible!", 5),
        ("Superb display quality and the screen is crystal clear. Love it!", 5),
        ("Outstanding camera performance in low light. Photos look professional.", 5),
        ("Battery backup is awesome. Lasts all day with heavy use.", 5),
        ("Very good build quality. Feels premium in hand.", 5),
        ("Excellent performance for gaming. No lag at all.", 5),
        ("The processor is super fast. Apps open instantly.", 4),
        ("Good value for money. Camera and battery both are great.", 4),
        ("Nice phone with good features. Display could be better though.", 4),
        ("Decent phone for the price. Performance is satisfactory.", 4),
        ("Camera is good but battery drains a bit fast.", 4),
        
        # Negative reviews with various issues
        ("Disappointed with the performance. Phone keeps lagging.", 2),
        ("Terrible product. Stopped working after 2 weeks.", 1),
        ("Battery life is very poor. Have to charge twice a day.", 1),
        ("Camera quality is not good. Pictures are blurry.", 1),
        ("Phone heats up too much during charging. Not safe.", 1),
        ("Display has dead pixels. Very disappointed with quality.", 2),
        ("Processor is too slow. Takes forever to open apps.", 2),
        ("Build quality is cheap. Back panel feels like plastic.", 2),
        ("Worst phone ever. Everything is substandard.", 1),
        
        # Mixed reviews
        ("Camera is excellent but battery backup is average.", 3),
        ("Good display and performance but price is too high.", 3),
        ("Battery is great but camera needs improvement.", 3),
        ("Nice design but performance could be better for this price.", 3)
    ]
    
    return pd.DataFrame(sample_reviews, columns=['reviewText', 'rating'])


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def calculate_confidence_score(probabilities: List[float]) -> float:
    """
    Calculate confidence score from probability distribution
    
    Args:
        probabilities: List of probabilities
        
    Returns:
        Confidence score (0-1)
    """
    if not probabilities:
        return 0.0
    return max(probabilities)
