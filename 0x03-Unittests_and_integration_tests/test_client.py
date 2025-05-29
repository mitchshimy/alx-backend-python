#!/usr/bin/env python3
"""
This module contains unit and integration tests for the GithubOrgClient class.
It covers parameterized tests for organization retrieval, testing of private
and public methods, and integration tests using fixture data with patching
to mock external API calls for consistent testing outcomes.
"""

import unittest
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from typing import Any, Dict
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class


def mocked_response(payload: Any) -> Any:
    """
    Helper function to create a mock response object for requests.get().json().

    Args:
        payload (Any): The data payload returned by the mock json().

    Returns:
        MockResponse: A mock response object with a json() method.
    """

    class MockResponse:
        def json(self_inner) -> Any:
            """Return the preset payload."""
            return payload

    return MockResponse()


@parameterized_class([{
    'org_payload': TEST_PAYLOAD[0][0],
    'repos_payload': TEST_PAYLOAD[0][1],
    'expected_repos': TEST_PAYLOAD[0][2],
    'apache2_repos': TEST_PAYLOAD[0][3]
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the public_repos method of GithubOrgClient.

    These tests use fixture data and mock requests.get calls to simulate
    GitHub API responses, verifying correct behavior of public repository
    retrieval, with and without license filtering.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Class-level setup method to patch requests.get and set side effects
        to return mocked fixture data based on URL called.
        """
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> Any:
            """Return mocked response depending on API endpoint called."""
            if url.endswith("/orgs/google"):
                return mocked_response(cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return mocked_response(cls.repos_payload)
            return mocked_response(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test that public_repos returns the expected list of repository names.

        This verifies that the method correctly parses repository names from
        the mocked repos_payload fixture.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test public_repos returns only repositories with the specified license.

        This tests filtering by license 'apache-2.0' using fixture data.
        """
        client = GithubOrgClient("google")
        filtered_repos = client.public_repos(license="apache-2.0")
        self.assertEqual(filtered_repos, self.apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class covering core methods and
    properties, including org retrieval, repos URL, public repos, and license
    checking.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Any) -> None:
        """
        Test that the org property returns expected JSON payload for given org.

        Args:
            org_name (str): The organization name to retrieve.
            mock_get_json (Any): Mock object for get_json function.
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
        Test that _public_repos_url property returns the correct repos URL.

        Args:
            mock_org (Any): Mocked org property returning a repos_url dict.
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
        Test that public_repos returns a list of repository names.

        Args:
            mock_get_json (Any): Mocked get_json returning list of repo dicts.
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
    ({"license": None}, "my_license", False),
    ({}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict[str, Any],
        license_key: str,
        expected: bool
    ) -> None:
        """
        Test has_license static method to confirm license key matching.

        Args:
            repo (Dict[str, Any]): Repository metadata dictionary.
            license_key (str): License key string to check.
            expected (bool): Expected boolean result.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
