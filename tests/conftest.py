"""
Test utilities and fixtures
"""

import pytest
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = "Test response"
    response.choices[0].finish_reason = "stop"
    response.model = "gpt-4"
    response.usage = Mock()
    response.usage.prompt_tokens = 10
    response.usage.completion_tokens = 20
    response.usage.total_tokens = 30
    response.id = "test-id"
    response.created = 1234567890
    return response


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response"""
    response = Mock()
    response.content = [Mock()]
    response.content[0].text = "Test response"
    response.content[0].type = "text"
    response.model = "claude-3-sonnet-20240229"
    response.usage = Mock()
    response.usage.input_tokens = 10
    response.usage.output_tokens = 20
    response.stop_reason = "end_turn"
    response.id = "test-id"
    response.type = "message"
    response.role = "assistant"
    return response
