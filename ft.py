"""
FastText Model Module
Handles loading and managing the FastText word embedding model
"""
import os
import fasttext
import fasttext.util

# Configuration
MODEL_PATH = os.path.join('models', 'fasttext_model_cbow.bin')
MODEL_DIM = 100  # Default dimension for FT model

_model = None

def get_model():
    """
    Load and return the FastText model
    
    Returns:
        FastText model instance
    """
    global _model
    
    if _model is not None:
        return _model
    
    # Check if model exists
    if os.path.exists(MODEL_PATH):
        print(f"Loading FastText model from {MODEL_PATH}")
        try:
            _model = fasttext.load_model(MODEL_PATH)
            print(f"FastText model loaded successfully. Dimension: {_model.get_dimension()}")
            return _model
        except Exception as e:
            print(f"Error loading FastText model: {e}")
            print("Falling back to pre-trained model...")
    
    # Fallback: download pre-trained model if local model doesn't exist
    print("Downloading pre-trained FastText model (this may take a while on first run)...")
    try:
        # Download English model
        fasttext.util.download_model('en', if_exists='ignore')
        _model = fasttext.load_model('cc.en.300.bin')
        
        # Optionally reduce dimension to match expected size
        if _model.get_dimension() != MODEL_DIM:
            print(f"Reducing model dimension from {_model.get_dimension()} to {MODEL_DIM}")
            fasttext.util.reduce_model(_model, MODEL_DIM)
        
        # Save for future use
        os.makedirs('models', exist_ok=True)
        _model.save_model(MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")
        
        return _model
    except Exception as e:
        print(f"Error downloading FastText model: {e}")
        raise RuntimeError("Failed to load or download FastText model")

def get_word_vector(word):
    """
    Get word vector for a given word
    
    Args:
        word: Word to get vector for
        
    Returns:
        Word vector as numpy array
    """
    model = get_model()
    return model.get_word_vector(word)

if __name__ == "__main__":
    # Test the module
    model = get_model()
    print(f"Model ready. Dimension: {model.get_dimension()}")
    
    # Test word vector
    test_word = "phone"
    vector = model.get_word_vector(test_word)
    print(f"Vector for '{test_word}': shape = {vector.shape}")
