"""
Test script to check batch analysis
"""
import pandas as pd
from pathlib import Path
import config
import utils
from analyzer import get_analyzer

print("=" * 60)
print("Testing Batch Analysis...")
print("=" * 60)

# Load a small sample CSV
sample_file = config.CSV_DIR / "B07S6BW832.csv"
print(f"\nLoading file: {sample_file}")

is_valid, message, df = utils.validate_csv_file(sample_file)

if is_valid and df is not None:
    print(f"Loaded {len(df)} reviews")
    
    # Take only first 5 reviews for quick testing
    df_small = df.head(5)
    print(f"\nTesting with {len(df_small)} reviews for speed")
    
    print("\nInitializing analyzer...")
    try:
        analyzer = get_analyzer("logistic_regression")
        print("Analyzer initialized successfully!")
        
        print("\nStarting batch analysis...")
        
        def progress_callback(current, total, status):
            print(f"Progress: {current}/{total} - {status}")
        
        results = analyzer.analyze_batch(df_small, progress_callback=progress_callback)
        
        print("\n" + "=" * 60)
        print("Analysis Results:")
        print("=" * 60)
        print(f"Summary: {results.get('summary', {})}")
        print(f"Features found: {len(results.get('features', {}))}")
        print(f"Classifications: {len(results.get('classification', []))}")
        
        if results.get('classification'):
            print("\nFirst 3 classifications:")
            for item in results['classification'][:3]:
                print(f"  - Category: {item.get('category')}, Sentiment: {item.get('sentiment')}")
                print(f"    Sentence: {item.get('sentence')[:80]}...")
        
        print("\n✅ Batch analysis completed successfully!")
        
    except Exception as e:
        print(f"\n❌ ERROR during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print(f"Failed to load CSV: {message}")
