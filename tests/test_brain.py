"""
Tests for Brain module
"""

import pytest
from unittest.mock import Mock, patch
from config.settings import Settings
from core.brain import Brain


@pytest.fixture
def settings():
    """Create test settings"""
    return Settings()


@pytest.fixture
def brain(settings):
    """Create brain instance"""
    return Brain(settings)


def test_brain_initialization(brain):
    """Test brain initialization"""
    assert brain is not None
    assert brain.provider in ["openai", "anthropic"]
    assert brain.model is not None


def test_brain_repr(brain):
    """Test brain string representation"""
    repr_str = repr(brain)
    assert "Brain" in repr_str
    assert brain.provider in repr_str


@patch('openai.chat.completions.create')
def test_generate_response_openai(mock_create, brain):
    """Test OpenAI response generation"""
    if brain.provider != "openai":
        pytest.skip("Not using OpenAI provider")
    
    # Mock response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test response"
    mock_create.return_value = mock_response
    
    messages = [{"role": "user", "content": "Hello"}]
    response = brain.generate_response(messages)
    
    assert response == "Test response"
    mock_create.assert_called_once()


def test_summarize_text(brain):
    """Test text summarization"""
    text = "This is a long text that needs to be summarized. " * 10
    summary = brain.summarize_text(text, max_length=50)
    
    assert summary is not None
    assert isinstance(summary, str)


def test_extract_keywords(brain):
    """Test keyword extraction"""
    text = "Python programming language is great for data science and machine learning"
    keywords = brain.extract_keywords(text, count=3)
    
    assert keywords is not None
    assert isinstance(keywords, list)
    assert len(keywords) <= 3


def test_analyze_intent(brain):
    """Test intent analysis"""
    text = "Search for Python tutorials"
    intent = brain.analyze_intent(text)
    
    assert intent is not None
    assert isinstance(intent, dict)
    assert "intent" in intent or "action" in intent
