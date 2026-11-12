
import os
import unittest
from unittest.mock import Mock, patch

import httpx
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from providers.groq_provider import GroqProvider


def make_status_error(error_class, status_code, message):
    """Build a Groq status error with local HTTPX request/response objects."""
    request = httpx.Request("POST", "https://example.test/chat/completions")
    response = httpx.Response(status_code, request=request)
    return error_class(message, response=response, body=None)


class TestGroqProvider(unittest.TestCase):

    def assert_provider_translates_error(
        self, mock_groq, sdk_error, expected_message
    ):
        """Check that an SDK error becomes the expected user-facing error."""
        mock_client = Mock()
        mock_groq.return_value = mock_client
        mock_client.chat.completions.create.side_effect = sdk_error

        # This dummy value is used only while constructing the mocked provider.
        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}):
            provider = GroqProvider()

            with self.assertRaisesRegex(RuntimeError, expected_message):
                provider.analyze_incident("mvn: command not found")

        mock_client.chat.completions.create.assert_called_once()

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

    # Test 6: Authentication errors are translated to a safe message.
    @patch("providers.groq_provider.Groq")
    def test_authentication_error(self, mock_groq):
        error = make_status_error(
            AuthenticationError, 401, "authentication failed"
        )
        self.assert_provider_translates_error(
            mock_groq, error, "Groq authentication failed"
        )

    # Test 7: Rate-limit errors are translated to a safe message.
    @patch("providers.groq_provider.Groq")
    def test_rate_limit_error(self, mock_groq):
        error = make_status_error(
            RateLimitError, 429, "rate limit exceeded"
        )
        self.assert_provider_translates_error(
            mock_groq, error, "Groq rate limit exceeded"
        )

    # Test 8: Timeouts get their specific error message.
    @patch("providers.groq_provider.Groq")
    def test_api_timeout_error(self, mock_groq):
        request = httpx.Request(
            "POST", "https://example.test/chat/completions"
        )
        error = APITimeoutError(request=request)
        self.assert_provider_translates_error(
            mock_groq, error, "Groq API request timed out"
        )

    # Test 9: Other connection errors get the connection error message.
    @patch("providers.groq_provider.Groq")
    def test_api_connection_error(self, mock_groq):
        request = httpx.Request(
            "POST", "https://example.test/chat/completions"
        )
        error = APIConnectionError(
            message="simulated connection failure",
            request=request,
        )
        self.assert_provider_translates_error(
            mock_groq, error, "Could not connect to Groq"
        )

    # Test 10: General status errors include the HTTP status code.
    @patch("providers.groq_provider.Groq")
    def test_api_status_error(self, mock_groq):
        error = make_status_error(
            APIStatusError, 503, "simulated server failure"
        )
        self.assert_provider_translates_error(
            mock_groq, error, "HTTP status 503"
        )



if __name__ == "__main__":
    unittest.main()
