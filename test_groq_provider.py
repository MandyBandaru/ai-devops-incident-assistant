
import os
import unittest
from unittest.mock import Mock, patch

from providers.groq_provider import GroqProvider


class TestGroqProvider(unittest.TestCase):

    # Test 1: Missing API key
    def test_missing_api_key(self):

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                GroqProvider()

    # Test 2: Successful AI response
    @patch("providers.groq_provider.Groq")
    def test_successful_analysis(self, mock_groq):

        mock_client = Mock()
        mock_groq.return_value = mock_client

        mock_response = Mock()

        mock_response.choices = [
            Mock(
                message=Mock(
                    content=(
                        "Maven command was not found. "
                        "Check installation and PATH."
                    )
                )
            )
        ]

        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            provider = GroqProvider()
            result = provider.analyze_incident(
                "mvn: command not found"
            )

        self.assertEqual(result["provider"], "groq")
        self.assertEqual(result["model"], "openai/gpt-oss-20b")
        self.assertFalse(result["root_cause_confirmed"])
        self.assertIn("Maven", result["analysis"])

    # Test 3: Verify selected model
    @patch("providers.groq_provider.Groq")
    def test_model_selection(self, mock_groq):

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            provider = GroqProvider()

        self.assertEqual(provider.model, "openai/gpt-oss-20b")
    
    # Test 4: Groq returns no response choices
    @patch("providers.groq_provider.Groq")
    def test_empty_choices(self, mock_groq):

        mock_client = Mock()
        mock_groq.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = []

        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            provider = GroqProvider()

            with self.assertRaises(ValueError):
                provider.analyze_incident("mvn: command not found")

    # Test 5: Groq returns empty response content
    @patch("providers.groq_provider.Groq")
    def test_empty_analysis(self, mock_groq):

        mock_client = Mock()
        mock_groq.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content="   "))
        ]

        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            provider = GroqProvider()

            with self.assertRaises(ValueError):
                provider.analyze_incident("mvn: command not found")



if __name__ == "__main__":
    unittest.main()
