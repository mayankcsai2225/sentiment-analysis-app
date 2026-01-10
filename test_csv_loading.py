"""
Test script to check CSV file loading
"""
import pandas as pd
from pathlib import Path
import config
import utils

print("=" * 60)
print("Testing CSV File Loading...")
print("=" * 60)

# Test with actual sample CSV file
sample_file = config.CSV_DIR / "B07S6BW832.csv"
print(f"\nTesting with file: {sample_file}")
print(f"File exists: {sample_file.exists()}")

# Test validation
print("\nValidating CSV file...")
is_valid, message, df = utils.validate_csv_file(sample_file)

print(f"Validation result: {is_valid}")
print(f"Message: {message}")

if is_valid and df is not None:
    print(f"\nValidated DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))
else:
    print("\nValidation failed!")
