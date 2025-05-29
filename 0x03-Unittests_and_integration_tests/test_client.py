#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient.
Tests cover:
- Parameterized org retrieval
- Private and public method behaviors
- Integration tests with fixtures and mock patching
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


def mocked_response(payload):
    """Helper function to mock requests.get().json() response."""
    class MockResponse:
        def json(self_inner):
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
    """Integration tests for the public_repos method of GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get using fixture data."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("/orgs/google"):
                return mocked_response(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return mocked_response(cls.repos_payload)
            return mocked_response(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos returns expected results
        when filtering by license 'apache-2.0'.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns expected JSON payload.

        Args:
            org_name (str): The organization name to test.
            mock_get_json (Mock): Mock for get_json.
        """
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct repos URL
        from the organization payload.

        Args:
            mock_org (Mock): Mocked org property returning a repos_url.
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
    def test_public_repos(self, mock_get_json):
        """
        Test public_repos method returns list of repository names.

        Args:
            mock_get_json (Mock): Mocked response with repo JSON data.
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
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license returns True if repo has the given license key.

        Args:
            repo (dict): The repository metadata.
            license_key (str): The license key to check.
            expected (bool): Expected result.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )
