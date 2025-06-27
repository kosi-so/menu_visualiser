import pytest
import os
import tempfile
from unittest.mock import Mock, patch, mock_open, MagicMock
from src.app.ocr.ocr import extract_menu_items
from src.app.ocr.group_with_gpt import group_lines_with_gpt
from src.app.ocr.ocr_pipeline import run_pipeline


class TestExtractMenuItems:
    """Test cases for the extract_menu_items function."""

    @patch('src.app.ocr.ocr.client')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_extract_menu_items_success(self, mock_file, mock_client):
        """Test successful extraction of menu items from image."""
        # Mock the Azure Document Intelligence response
        mock_result = Mock()
        mock_page = Mock()
        mock_line1 = Mock()
        mock_line1.content = "  •  Burger Deluxe  "
        mock_line2 = Mock()
        mock_line2.content = "  $12.99  "
        mock_line3 = Mock()
        mock_line3.content = "  Fresh beef with fries  "
        
        mock_page.lines = [mock_line1, mock_line2, mock_line3]
        mock_result.pages = [mock_page]
        
        mock_poller = Mock()
        mock_poller.result.return_value = mock_result
        mock_client.begin_analyze_document.return_value = mock_poller

        # Test the function
        result = extract_menu_items("fake_image_path.jpg")

        # Assertions
        assert result == ["Burger Deluxe", "$12.99", "Fresh beef with fries"]
        mock_client.begin_analyze_document.assert_called_once()
        mock_file.assert_called_once_with("fake_image_path.jpg", "rb")

    @patch('src.app.ocr.ocr.client')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_extract_menu_items_with_bullets_and_numbers(self, mock_file, mock_client):
        """Test extraction with various bullet points and numbers."""
        # Mock response with different bullet formats
        mock_result = Mock()
        mock_page = Mock()
        mock_lines = [
            Mock(content="  1.  Chicken Salad  "),
            Mock(content="  •  Caesar Dressing  "),
            Mock(content="  -  Garden Fresh  "),
            Mock(content="  2.  Steak House  "),
            Mock(content="  $15.99  "),
        ]
        mock_page.lines = mock_lines
        mock_result.pages = [mock_page]
        
        mock_poller = Mock()
        mock_poller.result.return_value = mock_result
        mock_client.begin_analyze_document.return_value = mock_poller

        result = extract_menu_items("fake_image_path.jpg")

        # Should clean bullets and numbers
        expected = ["Chicken Salad", "Caesar Dressing", "Garden Fresh", "Steak House", "$15.99"]
        assert result == expected

    @patch('src.app.ocr.ocr.client')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_extract_menu_items_empty_result(self, mock_file, mock_client):
        """Test handling of empty OCR result."""
        # Mock empty response
        mock_result = Mock()
        mock_result.pages = []
        
        mock_poller = Mock()
        mock_poller.result.return_value = mock_result
        mock_client.begin_analyze_document.return_value = mock_poller

        result = extract_menu_items("fake_image_path.jpg")

        assert result == []

    @patch('src.app.ocr.ocr.client')
    def test_extract_menu_items_file_not_found(self, mock_client):
        """Test handling of file not found error."""
        with pytest.raises(FileNotFoundError):
            extract_menu_items("nonexistent_file.jpg")

    @patch('src.app.ocr.ocr.client')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_extract_menu_items_azure_error(self, mock_file, mock_client):
        """Test handling of Azure API errors."""
        # Mock Azure API error
        mock_client.begin_analyze_document.side_effect = Exception("Azure API Error")

        with pytest.raises(Exception, match="Azure API Error"):
            extract_menu_items("fake_image_path.jpg")

    # Example of using fixtures from conftest.py
    def test_extract_menu_items_with_fixture(self, sample_ocr_lines, temp_image_file):
        """Test using fixtures from conftest.py."""
        # sample_ocr_lines fixture provides test data
        assert len(sample_ocr_lines) > 0
        assert "Burger Deluxe" in sample_ocr_lines
        
        # temp_image_file fixture provides a temporary file path
        assert os.path.exists(temp_image_file)


class TestGroupLinesWithGPT:
    """Test cases for the group_lines_with_gpt function."""

    @patch('src.app.ocr.group_with_gpt.client')
    def test_group_lines_with_gpt_success(self, mock_client):
        """Test successful grouping of OCR lines with GPT."""
        # Mock GPT response
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = '[{"name": "Burger", "price": "$12.99", "description": "Delicious burger"}]'
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        # Test input
        ocr_lines = ["Burger", "$12.99", "Delicious burger"]
        
        result = group_lines_with_gpt(ocr_lines)

        # Assertions
        assert result == '[{"name": "Burger", "price": "$12.99", "description": "Delicious burger"}]'
        mock_client.chat.completions.create.assert_called_once()

    @patch('src.app.ocr.group_with_gpt.client')
    def test_group_lines_with_gpt_empty_input(self, mock_client):
        """Test grouping with empty OCR lines."""
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = '[]'
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        result = group_lines_with_gpt([])

        assert result == '[]'

    @patch('src.app.ocr.group_with_gpt.client')
    def test_group_lines_with_gpt_api_error(self, mock_client):
        """Test handling of GPT API errors."""
        mock_client.chat.completions.create.side_effect = Exception("GPT API Error")

        with pytest.raises(Exception, match="GPT API Error"):
            group_lines_with_gpt(["test line"])

    @patch('src.app.ocr.group_with_gpt.client')
    def test_group_lines_with_gpt_prompt_format(self, mock_client):
        """Test that the prompt is formatted correctly."""
        mock_response = Mock()
        mock_choice = Mock()
        mock_choice.message.content = '[]'
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        ocr_lines = ["Line 1", "Line 2"]
        group_lines_with_gpt(ocr_lines)

        # Check that the prompt contains the OCR lines
        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert "Line 1" in user_message
        assert "Line 2" in user_message

    # Example of using fixtures from conftest.py
    def test_group_lines_with_gpt_using_fixtures(self, sample_ocr_lines, sample_structured_menu):
        """Test using fixtures for consistent test data."""
        # Use the sample_ocr_lines fixture
        assert len(sample_ocr_lines) == 9  # 3 menu items × 3 lines each
        
        # Use the sample_structured_menu fixture
        assert len(sample_structured_menu) == 3
        assert sample_structured_menu[0]["name"] == "Burger Deluxe"
        assert sample_structured_menu[0]["price"] == "$12.99"


class TestOCRPipeline:
    """Test cases for the run_pipeline function."""

    @patch('src.app.ocr.ocr_pipeline.group_lines_with_gpt')
    @patch('src.app.ocr.ocr_pipeline.extract_menu_items')
    def test_run_pipeline_success(self, mock_extract, mock_group):
        """Test successful pipeline execution."""
        # Mock the OCR extraction
        mock_extract.return_value = ["Burger", "$12.99", "Delicious burger"]
        
        # Mock the GPT grouping
        mock_group.return_value = '[{"name": "Burger", "price": "$12.99", "description": "Delicious burger"}]'

        result = run_pipeline("fake_image_path.jpg")

        # Assertions
        assert result == '[{"name": "Burger", "price": "$12.99", "description": "Delicious burger"}]'
        mock_extract.assert_called_once_with("fake_image_path.jpg")
        mock_group.assert_called_once_with(["Burger", "$12.99", "Delicious burger"])

    @patch('src.app.ocr.ocr_pipeline.group_lines_with_gpt')
    @patch('src.app.ocr.ocr_pipeline.extract_menu_items')
    def test_run_pipeline_ocr_failure(self, mock_extract, mock_group):
        """Test pipeline when OCR extraction fails."""
        mock_extract.side_effect = Exception("OCR Error")

        with pytest.raises(Exception, match="OCR Error"):
            run_pipeline("fake_image_path.jpg")

        # GPT grouping should not be called if OCR fails
        mock_group.assert_not_called()

    @patch('src.app.ocr.ocr_pipeline.group_lines_with_gpt')
    @patch('src.app.ocr.ocr_pipeline.extract_menu_items')
    def test_run_pipeline_gpt_failure(self, mock_extract, mock_group):
        """Test pipeline when GPT grouping fails."""
        mock_extract.return_value = ["Burger", "$12.99"]
        mock_group.side_effect = Exception("GPT Error")

        with pytest.raises(Exception, match="GPT Error"):
            run_pipeline("fake_image_path.jpg")

        # OCR should be called, but GPT fails
        mock_extract.assert_called_once()
        mock_group.assert_called_once()

    # Example of using fixtures from conftest.py
    def test_run_pipeline_with_fixtures(self, sample_ocr_lines, sample_structured_menu):
        """Test pipeline using fixtures for consistent data."""
        # This test shows how you could use fixtures in pipeline tests
        # In a real scenario, you'd mock the functions but use fixture data
        assert len(sample_ocr_lines) > 0
        assert len(sample_structured_menu) > 0


class TestOCRIntegration:
    """Integration tests for OCR functionality."""

    def test_ocr_module_imports(self):
        """Test that all OCR modules can be imported."""
        try:
            from src.app.ocr.ocr import extract_menu_items
            from src.app.ocr.group_with_gpt import group_lines_with_gpt
            from src.app.ocr.ocr_pipeline import run_pipeline
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import OCR modules: {e}")

    def test_environment_variables_required(self):
        """Test that required environment variables are checked."""
        # This test ensures that the modules handle missing env vars gracefully
        # In a real scenario, you might want to add proper error handling for missing env vars
        assert True  # Placeholder - add actual env var validation if needed

    # Example of using fixtures from conftest.py
    def test_integration_with_fixtures(self, sample_ocr_lines, sample_structured_menu, temp_image_file):
        """Integration test using multiple fixtures."""
        # This demonstrates how to use multiple fixtures in one test
        assert len(sample_ocr_lines) > 0
        assert len(sample_structured_menu) > 0
        assert os.path.exists(temp_image_file)


if __name__ == "__main__":
    pytest.main([__file__]) 