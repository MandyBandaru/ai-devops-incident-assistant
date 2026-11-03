import unittest

from ai_client_simulation import get_ai_response
from prompt_builder import build_troubleshooting_prompt


class TestAIClientSimulation(unittest.TestCase):

    def test_maven_error(self):
        result = get_ai_response("mvn: command not found")

        self.assertIn("Maven", result["explanation"])
        self.assertFalse(result["root_cause_confirmed"])

    def test_docker_error(self):
        result = get_ai_response("Docker daemon connection refused")

        self.assertIn("Docker", result["explanation"])
        self.assertFalse(result["root_cause_confirmed"])

    def test_unknown_error(self):
        result = get_ai_response("Unknown application failure")

        self.assertIn("not recognized", result["explanation"])

    def test_prompt_contains_error(self):
        error = "mvn: command not found"

        prompt = build_troubleshooting_prompt(error)

        self.assertIn(error, prompt)
        self.assertIn("senior DevOps engineer", prompt)

    def test_prompt_is_not_empty(self):
        prompt = build_troubleshooting_prompt("Docker error")

        self.assertTrue(prompt.strip())


if __name__ == "__main__":
    unittest.main()