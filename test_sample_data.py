"""
Test script to check if sample data processing works properly
"""
import pandas as pd
from analyzer import get_analyzer
import utils

# Try loading sample data
print("=" * 60)
print("Testing Sample Data Loading...")
print("=" * 60)

# Load sample data using the utility function
sample_df = utils.load_sample_data()
print(f"\nSample data loaded: {len(sample_df)} reviews")
print("\nSample data head:")
print(sample_df.head())
print(f"\nColumns: {sample_df.columns.tolist()}")

# Test validation
is_valid, message, df = utils.validate_csv_file(sample_df)
print(f"\nValidation result: {is_valid}")
print(f"Message: {message}")

if is_valid and df is not None:
    print(f"\nValidated DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Try to analyze the data
    print("\n" + "=" * 60)
    print("Testing Analyzer...")
    print("=" * 60)
    
    try:
        analyzer = get_analyzer("logistic_regression")
        print("Analyzer loaded successfully!")
        
        # Test batch analysis on first review
        print("\nTesting single review analysis...")
        first_review = df.iloc[0]['reviewText']
        print(f"Review text: {first_review}")
        
        result = analyzer.analyze_single_review(first_review, "logistic_regression")
        
        if "error" in result:
            print(f"\nERROR: {result['error']}")
        else:
            print(f"\nAnalysis successful!")
            print(f"Summary: {result.get('summary', {})}")
            
    except Exception as e:
        print(f"\nERROR during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print(f"\nValidation failed!")
