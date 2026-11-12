import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

from app import main


class TestApp(unittest.TestCase):

    def test_main_with_default_mock_provider(self):
        output = io.StringIO()

        with (
            patch.dict(os.environ, {}, clear=True),
            patch("builtins.input", return_value="mvn: command not found"),
            redirect_stdout(output),
        ):
            main()

        report = output.getvalue()

        self.assertIn("AI DEVOPS INCIDENT REPORT", report)
        self.assertIn("Provider              : mock", report)
        self.assertIn("Model                 : rule-based mock", report)
        self.assertIn("Incident              : mvn: command not found", report)
        self.assertIn("Root cause confirmed  : False", report)
        self.assertIn("Possible causes:", report)
        self.assertIn("Recommended action:", report)
        self.assertIn("Diagnostic commands:", report)
        self.assertIn("Troubleshooting steps:", report)
        self.assertNotIn("Unexpected application error:", report)

    @patch("providers.groq_provider.Groq")
    def test_main_with_groq_provider(self, mock_groq):
        mock_client = Mock()
        mock_groq.return_value = mock_client

        mock_response = Mock()
        mock_response.choices = [
            Mock(
                message=Mock(
                    content="Check whether Maven is installed and on PATH."
                ),
                finish_reason="stop",
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        output = io.StringIO()

        with (
            patch.dict(
                os.environ,
                {
                    "AI_PROVIDER": "groq",
                    "GROQ_API_KEY": "test-key",
                },
                clear=True,
            ),
            patch("builtins.input", return_value="mvn: command not found"),
            redirect_stdout(output),
        ):
            main()

        report = output.getvalue()

        self.assertIn("AI DEVOPS INCIDENT REPORT", report)
        self.assertIn("Provider              : groq", report)
        self.assertIn("Model                 : openai/gpt-oss-20b", report)
        self.assertIn("Incident              : mvn: command not found", report)
        self.assertIn("Root cause confirmed  : False", report)
        self.assertIn(
            "Check whether Maven is installed and on PATH.",
            report,
        )
        self.assertNotIn("Unexpected application error:", report)
        mock_client.chat.completions.create.assert_called_once()


if __name__ == "__main__":
    unittest.main()
