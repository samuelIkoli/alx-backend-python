#!/usr/bin/env python3
"""
This module contains unit tests for functions defined in the utils module.
The tests validate the behavior of nested map access, JSON retrieval from URLs,
and memoization logic to ensure correct functionality and robustness.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    This class contains unit tests for the access_nested_map
    function.The tests
    verify that values can be retrieved correctly
    using a sequence of keys and
    confirm that appropriate exceptions are
    raised for invalid paths.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map raises a KeyError when attempting to access
        a value using an invalid or incomplete key path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    This class contains unit tests for the get_json function.
    The tests ensure that HTTP GET requests are properly
    delegated to the requests library and
    that JSON payloads are returned correctly without
    making real network calls.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        # Patch requests.get
        with patch('utils.requests.get') as mock_get:
            # Create a mock response object with a .json() method
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function under test
            result = get_json(test_url)

            # Assert requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)

            # Assert function returned expected JSON payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass,
                          "a_method", return_value=42) as mock_method:
            # Call twice
            first = obj.a_property
            second = obj.a_property

            # Both results should be 42
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)

            # But a_method should be called ONLY ONCE
            mock_method.assert_called_once()
