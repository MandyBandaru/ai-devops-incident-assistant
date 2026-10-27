
import unittest
from incident_analyzer_v2 import classify_error


class TestIncidentAnalyzer(unittest.TestCase):

    def test_maven_error(self):
        result = classify_error("mvn: command not found")
        self.assertEqual(
            result,
            "Possible Maven installation or PATH issue"
        )

    def test_permission_error(self):
        result = classify_error("Permission denied")
        self.assertEqual(result, "Possible permissions issue")

    def test_timeout_error(self):
        result = classify_error("Connection timed out")
        self.assertEqual(
            result,
            "Possible network connectivity issue"
        )

    def test_unknown_error(self):
        result = classify_error("Unexpected application failure")
        self.assertEqual(
            result,
            "Unknown error - investigate further"
        )


if __name__ == "__main__":
    unittest.main()
