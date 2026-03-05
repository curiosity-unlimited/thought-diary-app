"""
AI Service for sentiment analysis using GitHub Models API.

This module provides functionality to analyze text content for sentiment
using the GitHub Models API with the gpt-4o model. It identifies positive
and negative words/phrases and returns HTML-marked content with sentiment counts.
"""

import os
import re
from typing import Tuple
import requests
from flask import current_app


def analyze_sentiment(content: str) -> Tuple[str, int, int]:
    """
    Analyze text content for sentiment using GitHub Models API.
    
    This function sends text to the GitHub Models API (gpt-4o) to identify
    positive and negative sentiment words/phrases. The API returns HTML with
    <span class="positive"> and <span class="negative"> tags wrapping
    sentiment-bearing words.
    
    Args:
        content (str): The text content to analyze for sentiment.
        
    Returns:
        Tuple[str, int, int]: A tuple containing:
            - analyzed_content (str): HTML with sentiment markers
            - positive_count (int): Number of positive sentiment markers
            - negative_count (int): Number of negative sentiment markers
            
    Raises:
        None: Errors are caught and logged, returning original content on failure.
        
    Example:
        >>> content = "I felt both excitement and anxious today."
        >>> analyzed, pos, neg = analyze_sentiment(content)
        >>> print(analyzed)
        'I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> today.'
        >>> print(pos, neg)
        1 1
    """
    # Get environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    model_name = os.getenv("GITHUB_MODEL_NAME", "gpt-4o")
    
    # Validate token
    if not github_token:
        current_app.logger.error("GITHUB_TOKEN not configured")
        return content, 0, 0
    
    # Prepare the API request
    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}"
    }
    
    # Create the sentiment analysis prompt
    prompt = """Analyze the following text for sentiment and identify words or phrases that convey positive or negative emotions.

Return the text with HTML span tags around sentiment words:
- Use <span class="positive">word</span> for positive sentiment words
- Use <span class="negative">word</span> for negative sentiment words
- Leave neutral words unmarked

Only return the marked-up HTML text, nothing else. Do not add any explanation or additional text.

Text to analyze:
"""
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a sentiment analysis assistant. You identify positive and negative sentiment in text and mark them with HTML span tags."
            },
            {
                "role": "user",
                "content": prompt + content
            }
        ],
        "model": model_name,
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    try:
        # Make the API request with timeout
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        analyzed_content = result.get("choices", [{}])[0].get("message", {}).get("content", content)
        
        # Clean up the response (remove any markdown code blocks if present)
        analyzed_content = analyzed_content.strip()
        if analyzed_content.startswith("```html"):
            analyzed_content = analyzed_content[7:]
        if analyzed_content.startswith("```"):
            analyzed_content = analyzed_content[3:]
        if analyzed_content.endswith("```"):
            analyzed_content = analyzed_content[:-3]
        analyzed_content = analyzed_content.strip()
        
        # Count positive and negative markers
        positive_count = len(re.findall(r'<span class="positive">', analyzed_content))
        negative_count = len(re.findall(r'<span class="negative">', analyzed_content))
        
        current_app.logger.info(
            f"Sentiment analysis completed: {positive_count} positive, {negative_count} negative markers"
        )
        
        return analyzed_content, positive_count, negative_count
        
    except requests.exceptions.Timeout:
        current_app.logger.error("GitHub Models API request timed out")
        return content, 0, 0
        
    except requests.exceptions.ConnectionError as e:
        current_app.logger.error(f"Connection error to GitHub Models API: {str(e)}")
        return content, 0, 0
        
    except requests.exceptions.HTTPError as e:
        current_app.logger.error(f"HTTP error from GitHub Models API: {str(e)}")
        return content, 0, 0
        
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error calling GitHub Models API: {str(e)}")
        return content, 0, 0
        
    except (KeyError, IndexError, ValueError) as e:
        current_app.logger.error(f"Error parsing GitHub Models API response: {str(e)}")
        return content, 0, 0
        
    except Exception as e:
        current_app.logger.error(f"Unexpected error in sentiment analysis: {str(e)}")
        return content, 0, 0


def get_sentiment_summary(positive_count: int, negative_count: int) -> str:
    """
    Get a summary label for overall sentiment based on counts.
    
    Args:
        positive_count (int): Number of positive sentiment markers.
        negative_count (int): Number of negative sentiment markers.
        
    Returns:
        str: Sentiment summary - "positive", "negative", or "neutral".
        
    Example:
        >>> get_sentiment_summary(5, 2)
        'positive'
        >>> get_sentiment_summary(2, 5)
        'negative'
        >>> get_sentiment_summary(3, 3)
        'neutral'
    """
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"
