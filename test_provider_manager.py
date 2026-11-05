import unittest
import os
from unittest.mock import patch

from providers.manager import get_provider
from providers.mock_provider import MockProvider


class TestProviderManager(unittest.TestCase):

    # Test 1: Default provider selection
    def test_default_provider(self):

        with patch.dict(os.environ, {}, clear=True):
            provider = get_provider()

        self.assertIsInstance(provider, MockProvider)

    # Test 2: Explicit Mock provider selection
    def test_mock_provider_selection(self):

        with patch.dict(os.environ, {"AI_PROVIDER": "mock"}):
            provider = get_provider()

        self.assertIsInstance(provider, MockProvider)

    # Test 3: Unsupported provider
    def test_unsupported_provider(self):

        with patch.dict(os.environ, {"AI_PROVIDER": "unknown"}):
            with self.assertRaises(ValueError):
                get_provider()


if __name__ == "__main__":
    unittest.main()