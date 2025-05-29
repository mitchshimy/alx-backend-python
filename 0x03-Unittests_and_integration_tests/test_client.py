#!/usr/bin/env python3
"""
This module contains unit and integration tests for the GithubOrgClient class.
It thoroughly covers parameterized tests for organization retrieval, testing of
private and public methods, and robust integration tests using fixture data.
Patching is utilized to mock external API calls, ensuring consistent and
isolated testing outcomes.
"""

import unittest
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Any, Dict
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class


def mocked_response(payload: Any) -> Any:
    """
    Creates a mock response object for simulating `requests.get().json()` calls.

    This helper function is designed to return an object that mimics the behavior
    of a `requests` library response, specifically providing a `json()` method
    that returns a predefined payload. This is invaluable for testing API
    interactions without making actual network requests.

    Args:
        payload (Any): The data payload that the mock `json()` method will return.

    Returns:
        MockResponse: An instance of `MockResponse` which has a `json()` method
                      that returns the provided `payload`.
    """

    class MockResponse:
        """
        A simple mock class to simulate a requests.Response object.

        This class provides a `json` method that returns a pre-configured payload,
        useful for mocking API responses in unit tests.
        """
        def json(self_inner) -> Any:
            """
            Returns the preset JSON payload associated with this mock response.

            This method mimics the `.json()` method of a `requests.Response` object,
            allowing tests to access the mocked API data.
            """
            return payload

    return MockResponse()


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Conducts integration tests for the `public_repos` method of `GithubOrgClient`.

    These tests leverage predefined fixture data and mock `requests.get` calls
    to accurately simulate GitHub API responses. The primary objective is to
    verify the correct functionality of public repository retrieval, including
    scenarios with and without specific license filtering.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the class-level fixtures by patching `requests.get`.

        This method initializes a patcher for `requests.get` to intercept
        HTTP requests made by `GithubOrgClient`. It defines a `side_effect`
        function that returns mocked fixture data (`org_payload`, `repos_payload`)
        based on the URL accessed, ensuring tests run consistently without
        external network dependencies.
        """
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> Any:
            """
            Provides a mocked response based on the API endpoint being called.

            This inner function acts as the `side_effect` for the patched
            `requests.get`, returning specific mock data depending on whether
            the request is for the organization's main payload or its repositories.

            Args:
                url (str): The URL that `requests.get` is attempting to access.

            Returns:
                Any: A `MockResponse` object containing the relevant `org_payload`,
                     `repos_payload`, or `None` if the URL does not match.
            """
            if url.endswith("/orgs/google"):
                return mocked_response(cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return mocked_response(cls.repos_payload)
            return mocked_response(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Cleans up class-level fixtures by stopping the `requests.get` patch.

        This method ensures that the mocking of `requests.get` is reverted
        after all integration tests within this class have completed,
        preventing interference with other tests or normal program execution.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Verifies that `public_repos` correctly returns the expected list of
        repository names.

        This test asserts that the `public_repos` method accurately parses
        and extracts repository names from the mocked `repos_payload` fixture
        provided by the `setUpClass` method, confirming the method's core
        functionality.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Tests that `public_repos` effectively filters and returns only
        repositories with the specified license.

        This test focuses on the license filtering capability, ensuring that
        when an 'apache-2.0' license is requested, only repositories matching
        this criterion are returned, based on the fixture data.
        """
        client = GithubOrgClient("google")
        filtered_repos = client.public_repos(license="apache-2.0")
        self.assertEqual(filtered_repos, self.apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """
    Contains comprehensive unit tests for the `GithubOrgClient` class.

    These tests cover the fundamental methods and properties of the client,
    including the accurate retrieval of organization data, the correct
    formation of repository URLs, the listing of public repositories, and
    the static method for checking repository licenses.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Any) -> None:
        """
        Asserts that the `org` property returns the expected JSON payload for
        a given organization name.

        This test verifies that `GithubOrgClient`'s `org` property correctly
        calls the `get_json` utility with the appropriate GitHub API URL
        for the organization and returns the mocked response.

        Args:
            org_name (str): The name of the organization to be retrieved.
            mock_get_json (Any): The mocked object for the `get_json` function,
                                 used to control its return value and verify calls.
        """
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: Any) -> None:
        """
        Confirms that the `_public_repos_url` property correctly extracts
        and returns the public repositories URL from the organization payload.

        This test mocks the `org` property to simulate a GitHub organization
        response and then verifies that `_public_repos_url` returns the
        expected URL for listing repositories.

        Args:
            mock_org (Any): A mocked `PropertyMock` instance for the `org`
                            property, configured to return a dictionary
                            containing a `repos_url`.
        """
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        client = GithubOrgClient("google")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/google/repos"
        )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Any) -> None:
        """
        Verifies that the `public_repos` method returns a list of correct
        repository names.

        This test employs mocks for both `get_json` (to simulate the list of
        repositories) and `_public_repos_url` (to control the URL used for
        fetching repositories), ensuring that the method processes the data
        and extracts repository names as expected.

        Args:
            mock_get_json (Any): The mocked object for the `get_json` function,
                                 set to return a list of repository dictionaries.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict[str, Any],
        license_key: str,
        expected: bool
    ) -> None:
        """
        Tests the `has_license` static method to confirm its accuracy in
        identifying if a repository has a specific license key.

        This test uses parameterized inputs to check various scenarios,
        including cases where the license matches or does not match the
        provided `license_key`.

        Args:
            repo (Dict[str, Any]): A dictionary representing repository metadata,
                                   potentially including a 'license' key.
            license_key (str): The specific license key string to check for
                               within the repository's license information.
            expected (bool): The boolean value expected as the result of the
                             `has_license` call.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
