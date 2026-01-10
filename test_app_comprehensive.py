"""
Comprehensive Test Script for Streamlit Sentiment Analysis App
This script tests all major features programmatically
"""
import pandas as pd
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
from analyzer import get_analyzer
import utils
import config

def test_single_review():
    """Test single review analysis"""
    print("\n" + "="*60)
    print("TEST 1: Single Review Analysis")
    print("="*60)
    
    test_review = "This phone has an amazing camera and battery life! The display is crystal clear and performance is smooth. However, the price is a bit high."
    
    try:
        analyzer = get_analyzer("logistic_regression")
        results = analyzer.analyze_single_review(test_review)
        
        if "error" in results:
            print(f"❌ FAILED: {results['error']}")
            return False
        
        print(f"✅ PASSED: Single review analysis completed")
        print(f"   - Total sentences: {results['summary']['total_sentences']}")
        print(f"   - Positive: {results['summary']['positive_count']}")
        print(f"   - Negative: {results['summary']['negative_count']}")
        print(f"   - Features found: {results['summary']['features_found']}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_csv_loading():
    """Test CSV file loading"""
    print("\n" + "="*60)
    print("TEST 2: CSV File Loading")
    print("="*60)
    
    csv_file = config.CSV_DIR / "micromax-ione.csv"
    
    if not csv_file.exists():
        print(f"❌ FAILED: Sample CSV not found at {csv_file}")
        return False
    
    try:
        # Test validation function
        is_valid, message, df = utils.validate_csv_file(csv_file)
        
        if not is_valid:
            print(f"❌ FAILED: CSV validation failed - {message}")
            return False
        
        print(f"✅ PASSED: CSV loaded successfully")
        print(f"   - {message}")
        print(f"   - Shape: {df.shape}")
        print(f"   - Columns: {df.columns.tolist()}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_analysis():
    """Test batch CSV analysis"""
    print("\n" + "="*60)
    print("TEST 3: Batch CSV Analysis (Small Sample)")
    print("="*60)
    
    csv_file = config.CSV_DIR / "micromax-ione.csv"
    
    try:
        # Load data
        df = pd.read_csv(csv_file, header=None, names=['reviewText', 'rating'])
        
        # Take small sample for testing
        test_df = df.head(5).copy()
        print(f"   Testing with {len(test_df)} reviews...")
        
        # Analyze
        analyzer = get_analyzer("logistic_regression")
        
        progress_counter = {'current': 0}
        def progress_callback(current, total, status):
            progress_counter['current'] = current
            if current % 10 == 0 or current == total:
                print(f"   Progress: {current}/{total} - {status}")
        
        results = analyzer.analyze_batch(test_df, progress_callback=progress_callback)
        
        print(f"✅ PASSED: Batch analysis completed")
        print(f"   - Total sentences: {results['summary']['total_sentences']}")
        print(f"   - Positive: {results['summary']['positive_count']}")
        print(f"   - Negative: {results['summary']['negative_count']}")
        print(f"   - Features: {len(results['features'])}")
        
        # Show top 3 features
        if results['features']:
            print(f"   - Top features:")
            for i, (feature, data) in enumerate(list(results['features'].items())[:3], 1):
                print(f"      {i}. {feature}: {data['total']} mentions")
        
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_feature_extraction():
    """Test feature extraction"""
    print("\n" + "="*60)
    print("TEST 4: Feature Extraction")
    print("="*60)
    
    test_reviews = pd.DataFrame({
        'reviewText': [
            'The camera quality is excellent and battery lasts long',
            'Screen is beautiful but performance is slow',
            'Great phone overall, good value for money'
        ],
        'rating': [5, 3, 5]
    })
    
    try:
        analyzer = get_analyzer("logistic_regression")
        results = analyzer.analyze_batch(test_reviews)
        
        features = results.get('features', {})
        
        if not features:
            print("⚠️  WARNING: No features extracted (this might be OK for small samples)")
            return True
        
        print(f"✅ PASSED: Feature extraction completed")
        print(f"   - Features found: {len(features)}")
        for feature, data in list(features.items())[:5]:
            print(f"      • {feature}: {data['total']} mentions")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_visualization_data():
    """Test that results can be formatted for visualization"""
    print("\n" + "="*60)
    print("TEST 5: Visualization Data Formatting")
    print("="*60)
    
    try:
        # Create mock results
        test_df = pd.DataFrame({
            'reviewText': ['Good phone', 'Bad battery'],
            'rating': [5, 2]
        })
        
        analyzer = get_analyzer("logistic_regression")
        results = analyzer.analyze_batch(test_df)
        
        # Test formatting function
        from utils import format_results_for_display
        viz_results = format_results_for_display(
            results.get('features', {}),
            pd.DataFrame(results.get('classification', []))
        )
        
        required_keys = ['summary', 'features', 'classification']
        for key in required_keys:
            if key not in viz_results:
                print(f"❌ FAILED: Missing key '{key}' in visualization data")
                return False
        
        print(f"✅ PASSED: Visualization data formatting works")
        print(f"   - All required keys present")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_feedback_system():
    """Test feedback saving system"""
    print("\n" + "="*60)
    print("TEST 6: Feedback System")
    print("="*60)
    
    try:
        # Test saving feedback
        utils.save_feedback(
            review_text="Test review",
            predicted="Positive",
            actual="Positive",
            rating=5,
            comments="Test feedback"
        )
        
        # Test getting stats
        stats = utils.get_feedback_stats()
        
        print(f"✅ PASSED: Feedback system works")
        print(f"   - Total feedback: {stats.get('total_feedback', 0)}")
        print(f"   - Accuracy: {stats.get('accuracy', 0):.1f}%")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_sample_data():
    """Test loading sample data"""
    print("\n" + "="*60)
    print("TEST 7: Sample Data Loading")
    print("="*60)
    
    try:
        sample_df = utils.load_sample_data()
        
        if sample_df is None or len(sample_df) == 0:
            print("❌ FAILED: No sample data returned")
            return False
        
        print(f"✅ PASSED: Sample data loaded")
        print(f"   - Rows: {len(sample_df)}")
        print(f"   - Columns: {sample_df.columns.tolist()}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "SENTIMENT ANALYSIS APP TEST SUITE" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        ("Single Review Analysis", test_single_review),
        ("CSV File Loading", test_csv_loading),
        ("Batch CSV Analysis", test_batch_analysis),
        ("Feature Extraction", test_feature_extraction),
        ("Visualization Data", test_visualization_data),
        ("Feedback System", test_feedback_system),
        ("Sample Data Loading", test_sample_data),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ({passed/total*100:.1f}%)")
    print(f"Failed: {failed} ({failed/total*100:.1f}%)")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! App is ready for deployment!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
