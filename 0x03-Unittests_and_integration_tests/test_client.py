#!/usr/bin/env python3
"""Unittests and Integration tests for client.py"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from utils import get_json
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test that org returns the correct value from get_json"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch('client.GithubOrgClient.org',
           new_callable=Mock(return_value={"repos_url": "http://test-url"}))
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns correct URL"""
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "http://test-url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        with patch('client.GithubOrgClient._public_repos_url',
                   return_value="http://test-url"):
            client = GithubOrgClient("test")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://test-url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected result"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class((
    'org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'
), [fixtures.TEST_PAYLOAD])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            Mock(json=Mock(return_value=cls.org_payload)),
            Mock(json=Mock(return_value=cls.repos_payload)),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns repos with apache2 license only"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
