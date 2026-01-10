"""
Unit tests for sentiment analysis components
"""
import pytest
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import utils
import config
from analyzer import SentimentAnalyzer


class TestUtils:
    """Test utility functions"""
    
    def test_validate_single_review_valid(self):
        """Test valid review validation"""
        is_valid, message = utils.validate_single_review("This is a great product!")
        assert is_valid is True
    
    def test_validate_single_review_too_short(self):
        """Test review that's too short"""
        is_valid, message = utils.validate_single_review("Hi")
        assert is_valid is False
    
    def test_validate_single_review_empty(self):
        """Test empty review"""
        is_valid, message = utils.validate_single_review("")
        assert is_valid is False
    
    def test_validate_single_review_too_long(self):
        """Test review that's too long"""
        long_text = "a" * 6000
        is_valid, message = utils.validate_single_review(long_text)
        assert is_valid is False
    
    def test_truncate_text(self):
        """Test text truncation"""
        text = "This is a long text that should be truncated"
        truncated = utils.truncate_text(text, max_length=20)
        assert len(truncated) <= 23  # 20 + "..."
    
    def test_truncate_text_short(self):
        """Test truncation of already short text"""
        text = "Short"
        truncated = utils.truncate_text(text, max_length=20)
        assert truncated == text
    
    def test_format_results_for_display(self):
        """Test results formatting"""
        features = {"battery": ["life"], "camera": []}
        df = pd.DataFrame({
            "category": ["battery", "camera"],
            "sentence": ["Great battery life", "Amazing camera"],
            "sentiment": ["Positive", "Positive"]
        })
        
        results = utils.format_results_for_display(features, df)
        
        assert "features" in results
        assert "classification" in results
        assert "summary" in results
        assert results["summary"]["total_sentences"] == 2
        assert results["summary"]["positive_count"] == 2
        assert results["summary"]["negative_count"] == 0
    
    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        probs = [0.3, 0.7]
        confidence = utils.calculate_confidence_score(probs)
        assert confidence == 0.7
    
    def test_calculate_confidence_score_empty(self):
        """Test confidence with empty list"""
        confidence = utils.calculate_confidence_score([])
        assert confidence == 0.0


class TestAnalyzer:
    """Test sentiment analyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return SentimentAnalyzer(model_type="logistic_regression")
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization"""
        assert analyzer is not None
        assert analyzer.model_type == "logistic_regression"
        assert analyzer.nlp is not None
        assert analyzer.ft_model is not None
        assert analyzer.custom_model is not None
    
    def test_detect_language_english(self, analyzer):
        """Test language detection for English"""
        text = "This is an English review"
        lang = analyzer.detect_language(text)
        assert lang == "en"
    
    def test_analyze_single_review_valid(self, analyzer):
        """Test single review analysis with valid input"""
        text = "This phone has an amazing camera and great battery life!"
        result = analyzer.analyze_single_review(text)
        
        assert "error" not in result
        assert "original_text" in result
        assert "summary" in result
        assert "features" in result
        assert "classification" in result
    
    def test_analyze_single_review_short(self, analyzer):
        """Test single review analysis with short text"""
        text = "OK"
        result = analyzer.analyze_single_review(text)
        
        # Should handle short text gracefully
        assert "error" in result or "summary" in result
    
    def test_analyze_batch_valid(self, analyzer):
        """Test batch analysis with valid data"""
        df = pd.DataFrame({
            'reviewText': [
                "Great phone with excellent camera!",
                "Battery life is terrible.",
                "Good value for money."
            ],
            'rating': [5, 2, 4]
        })
        
        result = analyzer.analyze_batch(df)
        
        assert "features" in result
        assert "classification" in result
        assert "summary" in result
    
    def test_compare_models(self, analyzer):
        """Test model comparison"""
        text = "This is a great product with excellent quality!"
        comparison = analyzer.compare_models(text)
        
        assert "text" in comparison
        assert "models" in comparison
        assert "custom_lr" in comparison["models"]


class TestConfig:
    """Test configuration"""
    
    def test_config_paths_exist(self):
        """Test that config paths are set"""
        assert config.BASE_DIR is not None
        assert config.MODELS_DIR is not None
        assert config.CSV_DIR is not None
    
    def test_config_model_settings(self):
        """Test model configuration"""
        assert config.DEFAULT_MODEL in ["logistic_regression", "transformers"]
        assert config.CONFIDENCE_THRESHOLD >= 0 and config.CONFIDENCE_THRESHOLD <= 1
    
    def test_config_directories_created(self):
        """Test that directories are created"""
        assert config.MODELS_DIR.exists()
        assert config.CSV_DIR.exists()


class TestFeedback:
    """Test feedback functionality"""
    
    def test_create_feedback_table(self):
        """Test feedback table creation"""
        utils.create_feedback_table()
        # If no error, table was created successfully
        assert True
    
    def test_save_and_retrieve_feedback(self):
        """Test saving and retrieving feedback"""
        # Save feedback
        utils.save_feedback(
            "Test review",
            "Positive",
            "Positive",
            5,
            "Test comment"
        )
        
        # Retrieve stats
        stats = utils.get_feedback_stats()
        
        assert stats["total_feedback"] >= 1
        assert "average_rating" in stats
        assert "accuracy" in stats


class TestVisualization:
    """Test visualization functions"""
    
    def test_create_metrics_cards(self):
        """Test metrics extraction"""
        from visualizations import create_metrics_cards
        
        results = {
            "summary": {
                "total_sentences": 10,
                "positive_count": 7,
                "negative_count": 3
            }
        }
        
        total, positive, negative, pos_pct = create_metrics_cards(results)
        
        assert total == 10
        assert positive == 7
        assert negative == 3
        assert pos_pct == 70.0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
