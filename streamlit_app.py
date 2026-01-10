"""
Sentiment Analysis Streamlit Application
Advanced sentiment analysis dashboard with multiple ML models and rich visualizations
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import time
import json

# Import our modules
import config
import utils
import visualizations as viz
from analyzer import SentimentAnalyzer, get_analyzer

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
    }
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []


def initialize_analyzer(model_type):
    """Initialize analyzer with loading indicator"""
    if st.session_state.analyzer is None or st.session_state.get('current_model') != model_type:
        with st.spinner(f"🚀 Loading {model_type} model... This may take a moment."):
            st.session_state.analyzer = get_analyzer(model_type)
            st.session_state.current_model = model_type
        st.success("✅ Model loaded successfully!")
    return st.session_state.analyzer


def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Product Review Sentiment Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced ML-powered sentiment analysis with multi-model support</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/sentiment-analysis.png", width=80)
        st.title("⚙️ Settings")
        
        # Model selection
        st.subheader("🤖 Model Selection")
        model_type = st.radio(
            "Choose analysis model:",
            ["logistic_regression", "transformers"],
            format_func=lambda x: "Custom Logistic Regression" if x == "logistic_regression" else "DistilBERT (Hugging Face)",
            help="Compare different models for sentiment analysis"
        )
        
        # Analysis mode
        st.subheader("📊 Analysis Mode")
        analysis_mode = st.radio(
            "Select mode:",
            ["Single Review", "Batch CSV Upload", "Model Comparison"],
            help="Choose how you want to analyze reviews"
        )
        
        # Advanced options
        with st.expander("🔬 Advanced Options"):
            show_explainability = st.checkbox("Show Model Explanations (LIME)", value=False)
            enable_multilingual = st.checkbox("Enable Multilingual Detection", value=True)
            show_wordcloud = st.checkbox("Generate Word Clouds", value=True)
        
        st.divider()
        
        # Feedback stats
        st.subheader("📈 System Stats")
        feedback_stats = utils.get_feedback_stats()
        st.metric("Total Analyses", feedback_stats.get("total_feedback", 0))
        st.metric("Accuracy", f"{feedback_stats.get('accuracy', 0):.1f}%")
        st.metric("Avg Rating", f"{feedback_stats.get('average_rating', 0):.1f}⭐")
    
    # Main content
    if analysis_mode == "Single Review":
        render_single_review_analysis(model_type, show_explainability, enable_multilingual, show_wordcloud)
    
    elif analysis_mode == "Batch CSV Upload":
        render_batch_analysis(model_type, show_wordcloud)
    
    elif analysis_mode == "Model Comparison":
        render_model_comparison()
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**💡 Tip:** Upload CSV files or paste review text for instant analysis")
    with col2:
        st.markdown("**🚀 Powered by:** Spacy, Scikit-learn, Hugging Face Transformers")
    with col3:
        if st.button("📥 Download Sample CSV"):
            sample_df = utils.load_sample_data()
            csv = sample_df.to_csv(index=False, header=False)
            st.download_button(
                "Download",
                csv,
                "sample_reviews.csv",
                "text/csv",
                key='download-csv'
            )


def render_single_review_analysis(model_type, show_explainability, enable_multilingual, show_wordcloud):
    """Render single review analysis interface"""
    st.header("📝 Single Review Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        review_text = st.text_area(
            "Enter your review:",
            height=150,
            placeholder="Type or paste a product review here...\n\nExample: This phone has an amazing camera and battery life! The display is crystal clear and performance is smooth.",
            help="Enter any product review to analyze its sentiment"
        )
    
    with col2:
        st.info("**How it works:**\n\n1. Enter a product review\n2. Click 'Analyze'\n3. View sentiment and features\n4. See detailed breakdowns")
        
        if st.button("🔍 Analyze Review", type="primary"):
            if review_text and len(review_text.strip()) > 3:
                analyze_single_review(review_text, model_type, show_explainability, enable_multilingual, show_wordcloud)
            else:
                st.error("⚠️ Please enter a valid review (at least 3 characters)")


def analyze_single_review(text, model_type, show_explainability, enable_multilingual, show_wordcloud):
    """Analyze a single review"""
    # Initialize analyzer
    analyzer = initialize_analyzer(model_type)
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Analysis steps
        status_text.text("🔄 Preprocessing text...")
        progress_bar.progress(25)
        time.sleep(0.3)
        
        status_text.text("🔍 Extracting features...")
        progress_bar.progress(50)
        
        # Analyze
        results = analyzer.analyze_single_review(text, model_type)
        
        status_text.text("🎯 Classifying sentiment...")
        progress_bar.progress(75)
        time.sleep(0.3)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
        
        # Check for errors
        if "error" in results:
            st.error(f"❌ {results['error']}")
            return
        
        # Display results
        display_single_review_results(results, analyzer, show_explainability, enable_multilingual, show_wordcloud)
        
        # Save to history
        st.session_state.analysis_history.append({
            "text": text[:100] + "..." if len(text) > 100 else text,
            "timestamp": pd.Timestamp.now(),
            "results": results
        })
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        progress_bar.empty()
        status_text.empty()


def display_single_review_results(results, analyzer, show_explainability, enable_multilingual, show_wordcloud):
    """Display results for single review analysis"""
    
    # Overall sentiment header
    st.success("✅ Analysis Complete!")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    summary = results.get("summary", {})
    
    with col1:
        st.metric(
            "📊 Total Sentences",
            summary.get("total_sentences", 0)
        )
    
    with col2:
        st.metric(
            "✅ Positive",
            summary.get("positive_count", 0),
            delta=None
        )
    
    with col3:
        st.metric(
            "❌ Negative",
            summary.get("negative_count", 0),
            delta=None
        )
    
    with col4:
        total = summary.get("total_sentences", 1)
        positive_pct = (summary.get("positive_count", 0) / total * 100) if total > 0 else 0
        st.metric(
            "📈 Positive %",
            f"{positive_pct:.1f}%"
        )
    
    st.divider()
    
    # Language detection
    if enable_multilingual:
        st.info(f"🌐 Detected Language: **{results.get('language', 'en').upper()}**")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Feature Analysis", "📝 Detailed Breakdown", "🔬 Explainability"])
    
    with tab1:
        # Convert to format expected by visualization functions
        viz_results = utils.format_results_for_display(
            results.get("features", {}),
            pd.DataFrame(results.get("classification", []))
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if viz_results["summary"]["total_sentences"] > 0:
                fig = viz.create_sentiment_pie_chart(viz_results)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if viz_results["features"]:
                fig = viz.create_feature_bar_chart(viz_results, top_n=8)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🎯 Features Detected")
        features = results.get("features", {})
        
        if features:
            for feature, related in features.items():
                with st.expander(f"**{feature.title()}**", expanded=True):
                    if related:
                        st.write(f"Related terms: {', '.join(related)}")
                    else:
                        st.write("Primary feature")
        else:
            st.info("No specific features detected")
    
    with tab3:
        st.subheader("📝 Sentence-by-Sentence Analysis")
        classifications = results.get("classification", [])
        
        if classifications:
            for i, item in enumerate(classifications, 1):
                sentiment = item.get("sentiment", "Unknown")
                color = "green" if sentiment == "Positive" else "red"
                
                st.markdown(f"""
                **{i}. [{item.get('category', 'general').title()}]** - :{color}[{sentiment}]
                > {item.get('sentence', '')}
                """)
        else:
            st.info("No classifications available")
    
    with tab4:
        if show_explainability:
            st.subheader("🔬 Model Explanation (LIME)")
            
            with st.spinner("Generating explanation..."):
                explanation = analyzer.explain_prediction(results.get("original_text", ""), method="lime")
                
                if "error" in explanation:
                    st.warning(f"⚠️ {explanation['error']}")
                else:
                    st.write("**Most Important Words:**")
                    
                    important_words = explanation.get("important_words", [])
                    
                    if important_words:
                        # Create a nice table
                        df_explain = pd.DataFrame(important_words, columns=["Word", "Impact"])
                        df_explain["Impact"] = df_explain["Impact"].round(3)
                        df_explain["Direction"] = df_explain["Impact"].apply(
                            lambda x: "🟢 Positive" if x > 0 else "🔴 Negative"
                        )
                        st.dataframe(df_explain, use_container_width=True)
                    else:
                        st.info("No explanation data available")
        else:
            st.info("💡 Enable 'Show Model Explanations' in the sidebar to see why the model made its predictions")
    
    # Export options
    st.divider()
    st.subheader("📥 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as JSON"):
            json_str = json.dumps(results, indent=2, default=str)
            st.download_button(
                "Download JSON",
                json_str,
                "analysis_results.json",
                "application/json"
            )
    
    with col2:
        if st.button("Export as CSV"):
            if results.get("classification"):
                df = pd.DataFrame(results["classification"])
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "analysis_results.csv",
                    "text/csv"
                )
    
    # Feedback section
    st.divider()
    with st.expander("💬 Provide Feedback"):
        st.write("Help us improve! Was this analysis accurate?")
        
        col1, col2 = st.columns(2)
        with col1:
            actual_sentiment = st.selectbox(
                "What's the actual sentiment?",
                ["Positive", "Negative", "Mixed"]
            )
        with col2:
            rating = st.slider("Rate accuracy (1-5)", 1, 5, 3)
        
        comments = st.text_area("Additional comments (optional)")
        
        if st.button("Submit Feedback"):
            predicted = "Positive" if summary.get("positive_count", 0) > summary.get("negative_count", 0) else "Negative"
            utils.save_feedback(results.get("original_text", ""), predicted, actual_sentiment, rating, comments)
            st.success("Thank you for your feedback! 🙏")


def render_batch_analysis(model_type, show_wordcloud):
    """Render batch CSV analysis interface"""
    st.header("📊 Batch CSV Analysis")
    
    # Initialize session state for loaded sample
    if 'loaded_sample_df' not in st.session_state:
        st.session_state.loaded_sample_df = None
    if 'sample_file_name' not in st.session_state:
        st.session_state.sample_file_name = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload CSV file with reviews",
            type=['csv'],
            help="CSV should have 'reviewText' and 'rating' columns"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # If user uploaded a file, clear any loaded sample and previous results
        if uploaded_file is not None:
            st.session_state.loaded_sample_df = None
            st.session_state.sample_file_name = None
            st.session_state.batch_analysis_results = None
    
    with col2:
        st.info("**CSV Format:**\n\nColumn 1: Review text\nColumn 2: Rating (1-5)\n\nNo headers needed!")
        
        # Sample files
        st.write("**Try a sample:**")
        csv_files = list(config.CSV_DIR.glob("*.csv"))
        if csv_files:
            sample_file = st.selectbox(
                "Select sample file:",
                [""] + [f.name for f in csv_files[:5]]
            )
            
            if sample_file and st.button("Load Sample"):
                # Load and validate the sample file
                sample_path = config.CSV_DIR / sample_file
                is_valid, message, df = utils.validate_csv_file(sample_path)
                
                if is_valid:
                    # Store in session state and clear previous results
                    st.session_state.loaded_sample_df = df
                    st.session_state.sample_file_name = sample_file
                    st.session_state.batch_analysis_results = None
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
                    return
    
    # Determine which file to use: uploaded or loaded sample
    df_to_analyze = None
    file_source = None
    
    if uploaded_file is not None:
        # User uploaded a file - use that
        is_valid, message, df_to_analyze = utils.validate_csv_file(uploaded_file)
        file_source = "uploaded"
    elif st.session_state.loaded_sample_df is not None:
        # User loaded a sample - use that
        df_to_analyze = st.session_state.loaded_sample_df
        is_valid = True
        message = f"Loaded sample: {st.session_state.sample_file_name} with {len(df_to_analyze)} reviews"
        file_source = "sample"
    else:
        # No file
        is_valid = False
    
    if is_valid and df_to_analyze is not None:
        st.success(f"✅ {message}")
        
        # Show clear button for loaded samples
        if file_source == "sample":
            if st.button("🗑️ Clear Sample"):
                st.session_state.loaded_sample_df = None
                st.session_state.sample_file_name = None
                st.session_state.batch_analysis_results = None
                st.rerun()
        
        # Preview
        with st.expander("👀 Preview Data"):
            # Only show reviewText and rating columns to avoid spacyObj serialization errors
            display_cols = ['reviewText', 'rating']
            preview_df = df_to_analyze[display_cols].head(10)
            st.dataframe(preview_df, use_container_width=True)
        
        # Analyze button
        if st.button("🚀 Analyze All Reviews", type="primary"):
            # Pass a copy to prevent modifying the session state DataFrame
            analyze_batch_reviews(df_to_analyze.copy(), model_type, show_wordcloud)
        
        # Display results if they exist in session state (persists across reruns)
        elif 'batch_analysis_results' in st.session_state and st.session_state.batch_analysis_results is not None:
            st.divider()
            display_batch_results(st.session_state.batch_analysis_results, show_wordcloud)
    elif uploaded_file is not None and not is_valid:
        st.error(f"❌ {message}")


def analyze_batch_reviews(df, model_type, show_wordcloud):
    """Analyze batch of reviews"""
    # Initialize analyzer
    analyzer = initialize_analyzer(model_type)
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def progress_callback(current, total, status):
        progress = int((current / total) * 100)
        progress_bar.progress(progress)
        status_text.text(f"{status} ({current}/{total})")
    
    try:
        # Analyze
        results = analyzer.analyze_batch(df, progress_callback=progress_callback)
        
        progress_bar.empty()
        status_text.empty()
        
        # Store results in session state so they persist across reruns
        st.session_state.batch_analysis_results = results
        
        # Display results
        display_batch_results(results, show_wordcloud)
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        progress_bar.empty()
        status_text.empty()


def display_batch_results(results, show_wordcloud):
    """Display batch analysis results"""
    st.success("✅ Batch Analysis Complete!")
    
    # Key metrics
    total, positive, negative, pos_pct = viz.create_metrics_cards(results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total Sentences", total)
    with col2:
        st.metric("✅ Positive", positive)
    with col3:
        st.metric("❌ Negative", negative)
    with col4:
        st.metric("📊 Positive %", f"{pos_pct:.1f}%")
    
    st.divider()
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Features", "📝 Details", "☁️ Word Clouds"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = viz.create_sentiment_pie_chart(results)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = viz.create_feature_bar_chart(results)
            st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap
        fig = viz.create_feature_sentiment_heatmap(results)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🎯 Feature Breakdown")
        
        features_df = []
        for feature, data in results["features"].items():
            features_df.append({
                "Feature": feature.title(),
                "Positive": data["positives"],
                "Negative": data["negatives"],
                "Total": data["total"],
                "Sentiment %": f"{(data['positives'] / data['total'] * 100) if data['total'] > 0 else 0:.1f}%"
            })
        
        df_features = pd.DataFrame(features_df)
        df_features = df_features.sort_values("Total", ascending=False)
        
        st.dataframe(df_features, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("📝 All Classifications")
        
        classifications_df = pd.DataFrame(results["classification"])
        
        # Add filtering
        filter_sentiment = st.selectbox("Filter by sentiment:", ["All", "Positive", "Negative"])
        filter_category = st.selectbox("Filter by category:", ["All"] + list(results["features"].keys()))
        
        filtered_df = classifications_df.copy()
        
        if filter_sentiment != "All":
            filtered_df = filtered_df[filtered_df["sentiment"] == filter_sentiment]
        
        if filter_category != "All":
            filtered_df = filtered_df[filtered_df["category"] == filter_category]
        
        st.dataframe(filtered_df, use_container_width=True, height=400)
    
    with tab4:
        if show_wordcloud:
            st.subheader("☁️ Word Clouds")
            
            # Get sentences
            positive_sentences = [item["sentence"] for item in results["classification"] if item["sentiment"] == "Positive"]
            negative_sentences = [item["sentence"] for item in results["classification"] if item["sentiment"] == "Negative"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Positive Reviews**")
                if positive_sentences:
                    fig = viz.create_wordcloud(positive_sentences, "positive")
                    st.pyplot(fig)
                else:
                    st.info("No positive sentences")
            
            with col2:
                st.write("**Negative Reviews**")
                if negative_sentences:
                    fig = viz.create_wordcloud(negative_sentences, "negative")
                    st.pyplot(fig)
                else:
                    st.info("No negative sentences")
        else:
            st.info("💡 Enable 'Generate Word Clouds' in the sidebar to see word clouds")
    
    # Export
    st.divider()
    st.subheader("📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        json_str = json.dumps(results, indent=2, default=str)
        st.download_button(
            "📄 Download as JSON",
            json_str,
            "batch_results.json",
            "application/json",
            use_container_width=True
        )
    
    with col2:
        df_export = pd.DataFrame(results["classification"])
        csv = df_export.to_csv(index=False)
        st.download_button(
            "📊 Download as CSV",
            csv,
            "batch_results.csv",
            "text/csv",
            use_container_width=True
        )


def render_model_comparison():
    """Render model comparison interface"""
    st.header("🤖 Model Comparison")
    
    st.info("Compare predictions from different sentiment analysis models on the same review")
    
    review_text = st.text_area(
        "Enter review for comparison:",
        height=150,
        placeholder="Enter a review to compare how different models analyze it..."
    )
    
    if st.button("🔍 Compare Models", type="primary"):
        if review_text and len(review_text.strip()) > 3:
            compare_models(review_text)
        else:
            st.error("⚠️ Please enter a valid review")


def compare_models(text):
    """Compare different models"""
    st.subheader("📊 Model Comparison Results")
    
    # Custom LR Model
    with st.spinner("Analyzing with Custom Logistic Regression..."):
        analyzer_lr = get_analyzer("logistic_regression")
        results_lr = analyzer_lr.analyze_single_review(text, "logistic_regression")
    
    # Transformers Model
    with st.spinner("Analyzing with DistilBERT (Transformers)..."):
        try:
            analyzer_trans = get_analyzer("transformers")
            results_trans = analyzer_trans.analyze_single_review(text, "transformers")
        except Exception as e:
            results_trans = {"error": str(e)}
    
    # Display comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔹 Custom LR Model")
        if "error" not in results_lr:
            summary_lr = results_lr.get("summary", {})
            st.metric("Positive Sentences", summary_lr.get("positive_count", 0))
            st.metric("Negative Sentences", summary_lr.get("negative_count", 0))
            st.metric("Features Found", summary_lr.get("features_found", 0))
        else:
            st.error(results_lr.get("error"))
    
    with col2:
        st.subheader("🔸 DistilBERT Model")
        if "error" not in results_trans:
            overall = results_trans.get("overall_sentiment", {})
            if overall:
                st.metric("Overall Sentiment", overall.get("sentiment", "N/A"))
                st.metric("Confidence", f"{overall.get('confidence', 0):.2%}")
            
            summary_trans = results_trans.get("summary", {})
            st.metric("Positive Sentences", summary_trans.get("positive_count", 0))
            st.metric("Negative Sentences", summary_trans.get("negative_count", 0))
        else:
            st.warning(f"Transformers model unavailable: {results_trans.get('error')}")
    
    # Detailed comparison
    with st.expander("📊 Detailed Comparison"):
        st.json({
            "custom_lr": results_lr,
            "transformers": results_trans
        })


if __name__ == "__main__":
    main()
