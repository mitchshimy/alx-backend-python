#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import utils
import requests
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test_org/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://test-url.com"
            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://test-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(
        TEST_PAYLOAD[0]["org_payload"],
        TEST_PAYLOAD[0]["repos_payload"],
        TEST_PAYLOAD[0]["expected_repos"],
        TEST_PAYLOAD[0]["apache2_repos"]
    )]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Define side_effect function to simulate different URLs
        def side_effect(url):
            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            return None

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


class MockResponse:
    """MockResponse for simulating requests.get().json()"""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data
