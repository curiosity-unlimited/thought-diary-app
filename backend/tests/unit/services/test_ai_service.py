"""Unit tests for AI sentiment analysis service.

This module tests:
- Successful sentiment analysis with GitHub Models API
- Positive and negative sentiment counting
- API error handling (connection, timeout, HTTP errors)
- Graceful fallback to original content on failure
"""

from unittest.mock import patch, MagicMock
import requests
from app.services.ai_service import analyze_sentiment, get_sentiment_summary


class TestAnalyzeSentiment:
    """Test cases for analyze_sentiment function."""
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_success(self, mock_post, app):
        """Test successful sentiment analysis."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'I felt <span class="positive">happy</span> and <span class="positive">excited</span> but also <span class="negative">nervous</span>.'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment('I felt happy and excited but also nervous.')
        
        assert analyzed_content == 'I felt <span class="positive">happy</span> and <span class="positive">excited</span> but also <span class="negative">nervous</span>.'
        assert positive_count == 2
        assert negative_count == 1
        
        # Verify API was called
        mock_post.assert_called_once()
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_only_positive(self, mock_post, app):
        """Test sentiment analysis with only positive words."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'I had a <span class="positive">wonderful</span>, <span class="positive">amazing</span>, <span class="positive">fantastic</span> day!'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment('I had a wonderful, amazing, fantastic day!')
        
        assert positive_count == 3
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_only_negative(self, mock_post, app):
        """Test sentiment analysis with only negative words."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'I felt <span class="negative">terrible</span>, <span class="negative">awful</span>, and <span class="negative">miserable</span>.'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment('I felt terrible, awful, and miserable.')
        
        assert positive_count == 0
        assert negative_count == 3
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_no_markers(self, mock_post, app):
        """Test sentiment analysis with no sentiment markers (neutral)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'I went to the store today.'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment('I went to the store today.')
        
        assert analyzed_content == 'I went to the store today.'
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_connection_error(self, mock_post, app):
        """Test graceful handling of connection errors."""
        # Mock connection error
        mock_post.side_effect = requests.exceptions.ConnectionError('Connection failed')
        
        original_content = 'Test content here.'
        analyzed_content, positive_count, negative_count = analyze_sentiment(original_content)
        
        # Should return original content on error
        assert analyzed_content == original_content
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_timeout_error(self, mock_post, app):
        """Test graceful handling of timeout errors."""
        # Mock timeout error
        mock_post.side_effect = requests.exceptions.Timeout('Request timed out')
        
        original_content = 'Test content here.'
        analyzed_content, positive_count, negative_count = analyze_sentiment(original_content)
        
        # Should return original content on timeout
        assert analyzed_content == original_content
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_http_error(self, mock_post, app):
        """Test graceful handling of HTTP errors."""
        # Mock HTTP error (e.g., 500 Internal Server Error)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('500 Server Error')
        mock_post.return_value = mock_response
        
        original_content = 'Test content here.'
        analyzed_content, positive_count, negative_count = analyze_sentiment(original_content)
        
        # Should return original content on HTTP error
        assert analyzed_content == original_content
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_invalid_json_response(self, mock_post, app):
        """Test handling of invalid JSON response from API."""
        # Mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError('Invalid JSON')
        mock_post.return_value = mock_response
        
        original_content = 'Test content here.'
        analyzed_content, positive_count, negative_count = analyze_sentiment(original_content)
        
        # Should return original content when JSON parsing fails
        assert analyzed_content == original_content
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_missing_choices(self, mock_post, app):
        """Test handling of API response missing expected fields."""
        # Mock response without choices field
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        original_content = 'Test content here.'
        analyzed_content, positive_count, negative_count = analyze_sentiment(original_content)
        
        # Should return original content when response structure is unexpected
        assert analyzed_content == original_content
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_empty_content(self, mock_post, app):
        """Test analyzing empty content."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': ''
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment('')
        
        assert analyzed_content == ''
        assert positive_count == 0
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_long_content(self, mock_post, app):
        """Test analyzing long content."""
        long_content = 'This is a very long diary entry. ' * 100
        analyzed = long_content + ' <span class="positive">happy</span>'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': analyzed
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment(long_content)
        
        assert positive_count == 1
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_special_characters(self, mock_post, app):
        """Test analyzing content with special characters."""
        content = 'I felt "happy" & excited! 😊'
        analyzed = 'I felt "<span class="positive">happy</span>" & <span class="positive">excited</span>! 😊'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': analyzed
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment(content)
        
        assert positive_count == 2
        assert negative_count == 0
    
    @patch('app.services.ai_service.requests.post')
    def test_analyze_sentiment_nested_spans(self, mock_post, app):
        """Test counting with nested or malformed span tags."""
        # Some malformed HTML with nested spans
        analyzed = '<span class="positive">I felt <span class="positive">happy</span></span>'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': analyzed
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyzed_content, positive_count, negative_count = analyze_sentiment('I felt happy')
        
        # Should count all positive span tags
        assert positive_count == 2
        assert negative_count == 0
    
    @patch('app.services.ai_service.os.getenv')
    def test_analyze_sentiment_missing_github_token(self, mock_getenv, app):
        """Test behavior when GITHUB_TOKEN is not configured."""
        # Mock missing GITHUB_TOKEN
        mock_getenv.return_value = None
        
        original_content = 'Test content here.'
        analyzed_content, positive_count, negative_count = analyze_sentiment(original_content)
        
        # Should return original content when token is missing
        assert analyzed_content == original_content
        assert positive_count == 0
        assert negative_count == 0


class TestGetSentimentSummary:
    """Test cases for get_sentiment_summary helper function."""
    
    def test_sentiment_summary_positive(self, app):
        """Test sentiment summary classification for positive entries."""
        assert get_sentiment_summary(5, 2) == 'positive'
        assert get_sentiment_summary(10, 0) == 'positive'
        assert get_sentiment_summary(3, 1) == 'positive'
    
    def test_sentiment_summary_negative(self, app):
        """Test sentiment summary classification for negative entries."""
        assert get_sentiment_summary(2, 5) == 'negative'
        assert get_sentiment_summary(0, 10) == 'negative'
        assert get_sentiment_summary(1, 3) == 'negative'
    
    def test_sentiment_summary_neutral(self, app):
        """Test sentiment summary classification for neutral entries."""
        assert get_sentiment_summary(0, 0) == 'neutral'
        assert get_sentiment_summary(3, 3) == 'neutral'
        assert get_sentiment_summary(10, 10) == 'neutral'
    
    def test_sentiment_summary_edge_cases(self, app):
        """Test sentiment summary with edge case values."""
        assert get_sentiment_summary(1, 0) == 'positive'
        assert get_sentiment_summary(0, 1) == 'negative'
        assert get_sentiment_summary(100, 99) == 'positive'
        assert get_sentiment_summary(99, 100) == 'negative'


class TestAPIIntegration:
    """Test cases for API request configuration."""
    
    @patch('app.services.ai_service.requests.post')
    def test_api_request_headers(self, mock_post, app):
        """Test that API requests include correct headers."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test content'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyze_sentiment('Test content')
        
        # Verify headers were included
        call_kwargs = mock_post.call_args[1]
        assert 'headers' in call_kwargs
        assert 'Authorization' in call_kwargs['headers']
        assert 'Content-Type' in call_kwargs['headers']
        assert call_kwargs['headers']['Content-Type'] == 'application/json'
    
    @patch('app.services.ai_service.requests.post')
    def test_api_request_timeout(self, mock_post, app):
        """Test that API requests include timeout parameter."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test content'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        analyze_sentiment('Test content')
        
        # Verify timeout was set (should be 30 seconds)
        call_kwargs = mock_post.call_args[1]
        assert 'timeout' in call_kwargs
        assert call_kwargs['timeout'] == 30
    
    @patch('app.services.ai_service.requests.post')
    def test_api_request_payload(self, mock_post, app):
        """Test that API requests include correct payload structure."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test content'
                }
            }]
        }
        mock_post.return_value = mock_response
        
        test_content = 'I felt happy today.'
        analyze_sentiment(test_content)
        
        # Verify payload structure
        call_kwargs = mock_post.call_args[1]
        assert 'json' in call_kwargs
        payload = call_kwargs['json']
        assert 'messages' in payload
        assert 'model' in payload
        assert len(payload['messages']) > 0
        # Verify test content is included in messages
        message_contents = [msg.get('content', '') for msg in payload['messages']]
        assert any(test_content in content for content in message_contents)
