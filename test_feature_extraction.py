"""
Test script to debug feature extraction
"""
import pandas as pd
from pathlib import Path
import config
import utils
from analyzer import get_analyzer
import spacy
from preprocess import preprocess, construct_spacy_obj
from feature_extraction import feature_extraction
import fasttext

print("=" * 60)
print("Testing Feature Extraction Step by Step...")
print("=" * 60)

# Load a small sample CSV
sample_file = config.CSV_DIR / "B07S6BW832.csv"
print(f"\nLoading file: {sample_file}")

is_valid, message, df = utils.validate_csv_file(sample_file)

if is_valid and df is not None:
    # Take only first 10 reviews
    df_small = df.head(10)
    print(f"\nProcessing {len(df_small)} reviews")
    
    print("\nOriginal data:")
    print(df_small[['reviewText', 'rating']].head())
    
    # Load spacy and fasttext
    print("\nLoading NLP models...")
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe('sentencizer')
    
    ft_model = fasttext.load_model('models/fasttext_model_cbow.bin')
    print("Models loaded!")
    
    # Step 1: Preprocess
    print("\n" + "=" * 60)
    print("Step 1: Preprocessing...")
    print("=" * 60)
    df_processed = preprocess(df_small.copy(), nlp)
    print(f"After preprocessing: {len(df_processed)} reviews")
    print("\nPreprocessed text samples:")
    for idx, text in df_processed['reviewText'].head(3).items():
        print(f"{idx}: {text[:100]}...")
    
    # Step 2: Construct spacy objects
    print("\n" + "=" * 60)
    print("Step 2: Constructing Spacy Objects...")
    print("=" * 60)
    df_processed = construct_spacy_obj(df_processed, nlp)
    print(f"Spacy objects created for {len(df_processed)} reviews")
    
    # Step 3: Feature extraction
    print("\n" + "=" * 60)
    print("Step 3: Feature Extraction...")
    print("=" * 60)
    features = feature_extraction(df_processed, ft_model, nlp)
    
    print(f"\nFeatures extracted: {len(features)}")
    if features:
        print("\nTop features:")
        for i, (feature, related) in enumerate(list(features.items())[:10]):
            print(f"  {i+1}. {feature}: {related}")
    else:
        print("\n⚠️ NO FEATURES EXTRACTED!")
        print("\nDebugging info:")
        print(f"Number of reviews: {len(df_processed)}")
        print(f"Review text types: {df_processed['reviewText'].dtype}")
        
        # Check for nouns in the reviews
        all_nouns = []
        for review in df_processed['spacyObj'].head(3):
            review_nouns = [token.text for token in review if token.pos_ == "NOUN"]
            print(f"\nNouns in review: {review_nouns}")
            all_nouns.extend(review_nouns)
        
        print(f"\nTotal nouns found in first 3 reviews: {len(all_nouns)}")
        print(f"Unique nouns: {set(all_nouns)}")
        
else:
    print(f"Failed to load CSV: {message}")
