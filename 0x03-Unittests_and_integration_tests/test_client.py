#!/usr/bin/env python3
"""
Test suite for the client.GithubOrgClient class methods,
including org retrieval, property mocking, repo listing,
and license verification.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict, Any


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient contains unit tests for GithubOrgClient methods
    such as org(), _public_repos_url, public_repos(), and has_license().
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', autospec=True)
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct payload and
        that get_json is called once with the proper URL.
        """
        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url property returns the 'repos_url'
        from the mocked org payload.
        """
        mocked_org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = mocked_org_payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, mocked_org_payload["repos_url"])

    @patch('client.get_json', autospec=True)
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test public_repos returns the list of repo names from the mocked
        repos JSON payload, and mocks _public_repos_url property.
        """
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = repos_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=property) as mock_public_url:
            mock_public_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once()
            mock_public_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str, expected: bool) -> None:
        """
        Test has_license method to confirm it returns True or False
        depending on whether the repo license key matches the license_key argument.
        """
        client = GithubOrgClient("any_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
