#!/usr/bin/env python3
"""
Unit tests for utils.get_json
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that utils.get_json returns expected JSON payload
        and calls requests.get exactly once with test_url.
        """

        # Create a Mock response object with a json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Configure the patched requests.get to return this mock_response
        mock_get.return_value = mock_response

        # Call the actual function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)   # called once with URL
        self.assertEqual(result, test_payload)       # correct returned json


if __name__ == "__main__":
    unittest.main()
