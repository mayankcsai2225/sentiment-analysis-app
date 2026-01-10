"""
FastAPI REST API for Sentiment Analysis
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import pandas as pd
from pathlib import Path
import io

# Import our modules
import config
from analyzer import get_analyzer
import utils

# Create FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    version=config.API_VERSION,
    description="Advanced sentiment analysis API with multi-model support",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Request/Response models
class SingleReviewRequest(BaseModel):
    text: str = Field(..., description="Review text to analyze", min_length=3)
    model_type: Optional[str] = Field("logistic_regression", description="Model type: logistic_regression or transformers")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "This phone has an amazing camera! Battery life is great too.",
                "model_type": "logistic_regression"
            }
        }

class SingleReviewResponse(BaseModel):
    original_text: str
    processed_text: str
    language: str
    model_used: str
    summary: Dict
    features: Dict
    classification: List[Dict]

class BatchAnalysisResponse(BaseModel):
    summary: Dict
    features: Dict
    classification: List[Dict]

class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: Dict

class FeedbackRequest(BaseModel):
    review_text: str
    predicted_sentiment: str
    actual_sentiment: str
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = ""


# API Endpoints
@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "Sentiment Analysis API",
        "version": config.API_VERSION,
        "documentation": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": config.API_VERSION,
        "models_loaded": {
            "logistic_regression": True,
            "transformers": TRANSFORMERS_AVAILABLE
        }
    }


@app.post("/analyze/single", response_model=SingleReviewResponse, tags=["Analysis"])
async def analyze_single_review(request: SingleReviewRequest):
    """
    Analyze a single review
    
    Args:
        request: Review analysis request
        
    Returns:
        Analysis results
    """
    try:
        # Get analyzer
        analyzer = get_analyzer(request.model_type)
        
        # Analyze
        results = analyzer.analyze_single_review(request.text, request.model_type)
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/batch", response_model=BatchAnalysisResponse, tags=["Analysis"])
async def analyze_batch_reviews(
    file: UploadFile = File(..., description="CSV file with reviews"),
    model_type: str = "logistic_regression"
):
    """
    Analyze batch of reviews from CSV file
    
    Args:
        file: CSV file with reviews (columns: reviewText, rating)
        model_type: Model type to use
        
    Returns:
        Batch analysis results
    """
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), header=None, names=['reviewText', 'rating'])
        
        # Validate
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Get analyzer
        analyzer = get_analyzer(model_type)
        
        # Analyze
        results = analyzer.analyze_batch(df)
        
        return results
    
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/analyze/compare", tags=["Analysis"])
async def compare_models(request: SingleReviewRequest):
    """
    Compare predictions from different models
    
    Args:
        request: Review text
        
    Returns:
        Comparison results
    """
    try:
        analyzer = get_analyzer("logistic_regression")
        comparison = analyzer.compare_models(request.text)
        return comparison
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@app.post("/explain", tags=["Explainability"])
async def explain_prediction(
    request: SingleReviewRequest,
    method: str = "lime"
):
    """
    Explain model prediction
    
    Args:
        request: Review text
        method: Explanation method (lime or shap)
        
    Returns:
        Explanation results
    """
    try:
        analyzer = get_analyzer(request.model_type)
        explanation = analyzer.explain_prediction(request.text, method=method)
        
        if "error" in explanation:
            raise HTTPException(status_code=400, detail=explanation["error"])
        
        return explanation
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")


@app.post("/feedback", tags=["Feedback"])
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit user feedback
    
    Args:
        feedback: Feedback data
        
    Returns:
        Success message
    """
    try:
        utils.save_feedback(
            feedback.review_text,
            feedback.predicted_sentiment,
            feedback.actual_sentiment,
            feedback.rating,
            feedback.comments
        )
        
        return {"message": "Feedback saved successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")


@app.get("/feedback/stats", tags=["Feedback"])
async def get_feedback_statistics():
    """Get feedback statistics"""
    try:
        stats = utils.get_feedback_stats()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve stats: {str(e)}")


# For imports in analyzer
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except:
    TRANSFORMERS_AVAILABLE = False


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
