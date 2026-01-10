"""
Test the updated sample data
"""
import pandas as pd
import utils
from analyzer import get_analyzer

print("=" * 60)
print("Testing Updated Sample Data...")
print("=" * 60)

# Load updated sample data
sample_df = utils.load_sample_data()
print(f"\nSample data loaded: {len(sample_df)} reviews")
print(f"Columns: {sample_df.columns.tolist()}")

# Show first few and last few
print("\nFirst 5 reviews:")
for idx, row in sample_df.head(5).iterrows():
    print(f"  {idx+1}. [{row['rating']}★] {row['reviewText'][:60]}...")

print("\nLast 5 reviews:")
for idx, row in sample_df.tail(5).iterrows():
    print(f"  {idx+1}. [{row['rating']}★] {row['reviewText'][:60]}...")

# Test batch analysis
print("\n" + "=" * 60)
print("Testing Batch Analysis with Updated Sample Data...")
print("=" * 60)

analyzer = get_analyzer("logistic_regression")
print("Analyzer loaded!")

print("\nRunning batch analysis...")

def progress_callback(current, total, status):
    print(f"  Progress: {int(current/total*100)}% - {status}")

results = analyzer.analyze_batch(sample_df, progress_callback=progress_callback)

print("\n" + "=" * 60)
print("RESULTS:")
print("=" * 60)

summary = results.get('summary', {})
features = results.get('features', {})
classifications = results.get('classification', [])

print(f"\n📊 Summary:")
print(f"   Total Sentences: {summary.get('total_sentences', 0)}")
print(f"   Positive: {summary.get('positive_count', 0)}")
print(f"   Negative: {summary.get('negative_count', 0)}")
print(f"   Positive %: {summary.get('positive_percentage', 0):.1f}%")

print(f"\n🎯 Features Extracted: {len(features)}")
if features:
    for i, (feature, related) in enumerate(list(features.items())[:10], 1):
        related_str = f" (related: {', '.join(related)})" if related else ""
        print(f"   {i}. {feature}{related_str}")

print(f"\n📝 Classifications: {len(classifications)}")
if classifications:
    print("\n   Sample classifications:")
    for item in classifications[:5]:
        sentiment = item.get('sentiment', 'Unknown')
        emoji = "✅" if sentiment == "Positive" else "❌"
        print(f"   {emoji} [{item.get('category', 'general')}] {sentiment}: {item.get('sentence', '')[:70]}...")

print("\n" + "=" * 60)
if len(features) > 0 and len(classifications) > 0:
    print("✅ SUCCESS! Sample data now works properly with feature extraction!")
else:
    print("⚠️ WARNING: Still not enough data for proper analysis")
print("=" * 60)
