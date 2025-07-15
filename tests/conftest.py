"""
Pytest configuration and shared fixtures for menu_visualiser tests.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock


@pytest.fixture
def sample_ocr_lines():
    """Sample OCR lines for testing."""
    return [
        "Burger Deluxe",
        "$12.99",
        "Fresh beef with fries",
        "Chicken Salad",
        "$10.99",
        "Mixed greens with vinaigrette",
        "Steak House",
        "$18.99",
        "Premium cut with mashed potatoes",
    ]


@pytest.fixture
def sample_structured_menu():
    """Sample structured menu data for testing."""
    return [
        {
            "name": "Burger Deluxe",
            "price": "$12.99",
            "description": "Fresh beef with fries",
        },
        {
            "name": "Chicken Salad",
            "price": "$10.99",
            "description": "Mixed greens with vinaigrette",
        },
        {
            "name": "Steak House",
            "price": "$18.99",
            "description": "Premium cut with mashed potatoes",
        },
    ]


@pytest.fixture
def mock_azure_response():
    """Mock Azure Document Intelligence response."""
    mock_result = Mock()
    mock_page = Mock()
    mock_lines = [
        Mock(content="Burger Deluxe"),
        Mock(content="$12.99"),
        Mock(content="Fresh beef with fries"),
        Mock(content="Chicken Salad"),
        Mock(content="$10.99"),
        Mock(content="Mixed greens with vinaigrette"),
    ]
    mock_page.lines = mock_lines
    mock_result.pages = [mock_page]
    return mock_result


@pytest.fixture
def mock_gpt_response():
    """Mock GPT API response."""
    mock_response = Mock()
    mock_choice = Mock()
    mock_choice.message.content = """[
        {"name": "Burger Deluxe", "price": "$12.99", "description": "Fresh beef with fries"},
        {"name": "Chicken Salad", "price": "$10.99", "description": "Mixed greens with vinaigrette"}
    ]"""
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.fixture
def temp_image_file():
    """Create a temporary image file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        # Write some fake image data
        f.write(b"fake_image_data")
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv(
        "AZURE_ENDPOINT", "https://fake-endpoint.cognitiveservices.azure.com/"
    )
    monkeypatch.setenv("AZURE_KEY", "fake-key")
    monkeypatch.setenv("AZURE_OPENAI_KEY", "fake-openai-key")
    monkeypatch.setenv(
        "AZURE_OPENAI_ENDPOINT", "https://fake-openai-endpoint.openai.azure.com/"
    )
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT_NAME", "fake-deployment")
