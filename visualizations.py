"""
Visualization functions for sentiment analysis dashboard
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import io
import base64

import config


def create_sentiment_pie_chart(results: Dict) -> go.Figure:
    """
    Create pie chart for sentiment distribution
    
    Args:
        results: Results dictionary with summary
        
    Returns:
        Plotly figure
    """
    summary = results["summary"]
    
    labels = ["Positive", "Negative"]
    values = [summary["positive_count"], summary["negative_count"]]
    colors = ["#00D26A", "#FF4B4B"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Overall Sentiment Distribution",
        title_font_size=20,
        showlegend=True,
        height=400
    )
    
    return fig


def create_feature_bar_chart(results: Dict, top_n: int = 10) -> go.Figure:
    """
    Create bar chart for top features
    
    Args:
        results: Results dictionary
        top_n: Number of top features to show
        
    Returns:
        Plotly figure
    """
    features_data = []
    
    for feature, data in results["features"].items():
        features_data.append({
            "feature": feature,
            "positive": data["positives"],
            "negative": data["negatives"],
            "total": data["total"]
        })
    
    df = pd.DataFrame(features_data)
    df = df.sort_values("total", ascending=False).head(top_n)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Positive',
        x=df['feature'],
        y=df['positive'],
        marker_color='#00D26A',
        hovertemplate='<b>%{x}</b><br>Positive: %{y}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Negative',
        x=df['feature'],
        y=df['negative'],
        marker_color='#FF4B4B',
        hovertemplate='<b>%{x}</b><br>Negative: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Top {top_n} Features by Mention Count",
        xaxis_title="Feature",
        yaxis_title="Count",
        barmode='stack',
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig


def create_feature_sentiment_heatmap(results: Dict) -> go.Figure:
    """
    Create heatmap showing sentiment for each feature
    
    Args:
        results: Results dictionary
        
    Returns:
        Plotly figure
    """
    features_list = []
    sentiment_scores = []
    
    for feature, data in results["features"].items():
        total = data["total"]
        if total > 0:
            features_list.append(feature)
            # Calculate sentiment score: positive % - negative %
            pos_pct = (data["positives"] / total) * 100
            neg_pct = (data["negatives"] / total) * 100
            sentiment_scores.append(pos_pct - neg_pct)
    
    # Sort by sentiment score
    sorted_data = sorted(zip(features_list, sentiment_scores), key=lambda x: x[1], reverse=True)
    features_list, sentiment_scores = zip(*sorted_data) if sorted_data else ([], [])
    
    # Create color scale
    colors = []
    for score in sentiment_scores:
        if score > 50:
            colors.append('#00D26A')  # Strong positive
        elif score > 0:
            colors.append('#90EE90')  # Mild positive
        elif score > -50:
            colors.append('#FFB6B6')  # Mild negative
        else:
            colors.append('#FF4B4B')  # Strong negative
    
    fig = go.Figure(data=[go.Bar(
        y=features_list,
        x=sentiment_scores,
        orientation='h',
        marker=dict(
            color=sentiment_scores,
            colorscale=[[0, '#FF4B4B'], [0.5, '#FFFFFF'], [1, '#00D26A']],
            showscale=True,
            colorbar=dict(title="Sentiment<br>Score")
        ),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Feature Sentiment Scores",
        xaxis_title="Sentiment Score (Positive % - Negative %)",
        yaxis_title="Feature",
        height=max(400, len(features_list) * 30),
        showlegend=False
    )
    
    return fig


def create_wordcloud(text_list: List[str], sentiment: str = "all") -> plt.Figure:
    """
    Create word cloud from text
    
    Args:
        text_list: List of text strings
        sentiment: Filter by sentiment ("positive", "negative", or "all")
        
    Returns:
        Matplotlib figure
    """
    if not text_list:
        # Create empty figure
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'No data available', 
                ha='center', va='center', fontsize=20)
        ax.axis('off')
        return fig
    
    combined_text = " ".join(text_list)
    
    # Color scheme based on sentiment
    if sentiment.lower() == "positive":
        colormap = "Greens"
    elif sentiment.lower() == "negative":
        colormap = "Reds"
    else:
        colormap = "viridis"
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap=colormap,
        max_words=100,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(combined_text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f'{sentiment.title()} Reviews Word Cloud', fontsize=16, pad=20)
    
    return fig


def create_sentence_length_distribution(results: Dict) -> go.Figure:
    """
    Create histogram of sentence lengths
    
    Args:
        results: Results dictionary
        
    Returns:
        Plotly figure
    """
    sentence_lengths = []
    sentiments = []
    
    for item in results["classification"]:
        sentence_lengths.append(len(item["sentence"].split()))
        sentiments.append(item["sentiment"])
    
    df = pd.DataFrame({
        "length": sentence_lengths,
        "sentiment": sentiments
    })
    
    fig = px.histogram(
        df,
        x="length",
        color="sentiment",
        color_discrete_map={"Positive": "#00D26A", "Negative": "#FF4B4B"},
        nbins=30,
        title="Distribution of Sentence Lengths",
        labels={"length": "Number of Words", "sentiment": "Sentiment"}
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        barmode='overlay'
    )
    
    fig.update_traces(opacity=0.7)
    
    return fig


def create_comparison_chart(results_list: List[Tuple[str, Dict]]) -> go.Figure:
    """
    Create comparison chart for multiple products/datasets
    
    Args:
        results_list: List of tuples (name, results_dict)
        
    Returns:
        Plotly figure
    """
    data = []
    
    for name, results in results_list:
        summary = results["summary"]
        total = summary["total_sentences"]
        if total > 0:
            data.append({
                "Product": name,
                "Positive %": (summary["positive_count"] / total) * 100,
                "Negative %": (summary["negative_count"] / total) * 100,
                "Total Reviews": total
            })
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Positive %',
        x=df['Product'],
        y=df['Positive %'],
        marker_color='#00D26A',
        text=df['Positive %'].round(1),
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Positive: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Negative %',
        x=df['Product'],
        y=df['Negative %'],
        marker_color='#FF4B4B',
        text=df['Negative %'].round(1),
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Negative: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Product Sentiment Comparison",
        xaxis_title="Product",
        yaxis_title="Percentage",
        barmode='stack',
        height=500,
        showlegend=True
    )
    
    return fig


def create_metrics_cards(results: Dict) -> Tuple[int, int, int, float]:
    """
    Extract key metrics for display
    
    Args:
        results: Results dictionary
        
    Returns:
        Tuple of (total_reviews, positive, negative, positive_percentage)
    """
    summary = results["summary"]
    total = summary["total_sentences"]
    positive = summary["positive_count"]
    negative = summary["negative_count"]
    
    positive_pct = (positive / total * 100) if total > 0 else 0
    
    return total, positive, negative, positive_pct


def fig_to_base64(fig) -> str:
    """
    Convert matplotlib figure to base64 string
    
    Args:
        fig: Matplotlib figure
        
    Returns:
        Base64 encoded string
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    buf.close()
    return img_str
