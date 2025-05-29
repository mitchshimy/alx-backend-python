#!/usr/bin/env python3
"""
Module that contains unit tests for utils functions:
- access_nested_map
- get_json
- memoize decorator
"""

import unittest
from typing import Any, Dict, Tuple
from unittest.mock import patch, Mock
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for utils.access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: Dict,
                               path: Tuple[str, ...],
                               expected: Any) -> None:
        """
        Test access_nested_map returns expected result for given nested_map and path.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Dict,
                                         path: Tuple[str, ...]) -> None:
        """
        Test access_nested_map raises KeyError with expected message for invalid keys.
        """
        with self.assertRaises(KeyError) as context:
            utils.access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """
    Test class for utils.get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self,
                      mock_get: Mock,
                      test_url: str,
                      test_payload: Dict[str, Any]) -> None:
        """
        Test get_json returns expected payload and calls requests.get once with correct URL.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = utils.get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test class for utils.memoize decorator.
    """

    def test_memoize(self) -> None:
        """
        Test that memoize caches the result and calls the decorated method only once.
        """

        class TestClass:
            def a_method(self) -> int:
                """Method to be mocked."""
                return 42

            @utils.memoize
            def a_property(self) -> int:
                """Memoized property that calls a_method."""
                return self.a_method()

        test_instance = TestClass()

        with patch.object(test_instance, 'a_method', return_value=42) as mock_method:
            # Call twice, second call should use cache
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
