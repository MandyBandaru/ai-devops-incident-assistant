from providers.base import AIProvider
from ai_client_simulation import get_ai_response


class MockProvider(AIProvider):

    def analyze_incident(self, incident: str) -> dict:
        mock_response = get_ai_response(incident)

        analysis_sections = [
            mock_response["explanation"],
            "",
            "Possible causes:",
            *[f"- {cause}" for cause in mock_response["possible_causes"]],
            "",
            "Recommended action:",
            mock_response["recommended_action"],
            "",
            "Diagnostic commands:",
            *[
                f"- {command}"
                for command in mock_response["diagnostic_commands"]
            ],
            "",
            "Troubleshooting steps:",
            *[
                f"- {step}"
                for step in mock_response["troubleshooting_steps"]
            ],
        ]

        return {
            "provider": "mock",
            "model": "rule-based mock",
            "incident": incident,
            "analysis": "\n".join(analysis_sections),
            "root_cause_confirmed": mock_response["root_cause_confirmed"],
        }
