"""
Test with different sample sizes to find the minimum working size
"""
import pandas as pd
from pathlib import Path
import config
import utils
from analyzer import get_analyzer

print("=" * 60)
print("Testing Different Sample Sizes...")
print("=" * 60)

# Load CSV
sample_file = config.CSV_DIR / "B07S6BW832.csv"
is_valid, message, df = utils.validate_csv_file(sample_file)

if is_valid and df is not None:
    print(f"Total reviews available: {len(df)}")
    
    # Initialize analyzer once
    analyzer = get_analyzer("logistic_regression")
    
    # Test different sizes
    for size in [5, 10, 20, 50, 100]:
        if size > len(df):
            break
            
        print(f"\n{'=' * 60}")
        print(f"Testing with {size} reviews...")
        print(f"{'=' * 60}")
        
        df_sample = df.head(size)
        
        try:
            results = analyzer.analyze_batch(df_sample)
            
            features_count = len(results.get('features', {}))
            classifications_count = len(results.get('classification', []))
            summary = results.get('summary', {})
            
            print(f"✅ Success!")
            print(f"   Features found: {features_count}")
            print(f"   Classifications: {classifications_count}")
            print(f"   Positive: {summary.get('positive_count', 0)}")
            print(f"   Negative: {summary.get('negative_count', 0)}")
            
            if features_count > 0:
                print(f"   Top features: {list(results['features'].keys())[:5]}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 60}")
    print("Recommendation:")
    print("=" * 60)
    print("Based on the results, the minimum recommended sample size is:")
    print("to get meaningful feature extraction and classification results.")
    
else:
    print(f"Failed to load CSV: {message}")
