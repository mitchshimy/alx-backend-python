#!/usr/bin/env python3
"""
Test suite for client.GithubOrgClient class covering unit and integration tests.
"""

import unittest
from typing import Any, Dict, List, Optional
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class

import client
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for client.GithubOrgClient.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(
            self,
            org_name: str,
            mock_get_json: Mock
    ) -> None:
        """
        Test that GithubOrgClient.org returns the expected dictionary.
        """
        mock_get_json.return_value = {"org": org_name}
        gh_client = client.GithubOrgClient(org_name)
        result = gh_client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the 'repos_url' from org property.
        """
        gh_client = client.GithubOrgClient("test_org")
        with patch.object(
            client.GithubOrgClient,
            "org",
            new_callable=property
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://fake_url"}
            self.assertEqual(gh_client._public_repos_url, "http://fake_url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test that public_repos returns list of repo names based on mocked payload.
        """
        gh_client = client.GithubOrgClient("test_org")
        expected_repos = ["repo1", "repo2", "repo3"]

        mock_get_json.return_value = [
            {"name": name, "license": None} for name in expected_repos
        ]

        with patch.object(
            client.GithubOrgClient,
            "_public_repos_url",
            new_callable=property
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://fake_repos_url"

            repos = gh_client.public_repos()

            mock_get_json.assert_called_once_with("http://fake_repos_url")
            self.assertEqual(repos, expected_repos)
            mock_repos_url.assert_called_once()

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
        Test has_license returns True if repo has the license_key, else False.
        """
        gh_client = client.GithubOrgClient("org")
        self.assertEqual(gh_client.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            fixtures.org_payload,
            fixtures.repos_payload,
            fixtures.expected_repos,
            fixtures.apache2_repos,
        )
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos using fixtures.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setup class-level patchers and mock responses for requests.get.
        """
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url: str, *args: Any, **kwargs: Any) -> Mock:
            """
            Side effect function to return mocked response based on URL.
            """
            mock_resp = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stop patching requests.get.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test public_repos returns expected list of repo names from fixtures.
        """
        gh_client = client.GithubOrgClient(self.org_payload["login"])
        repos = gh_client.public_repos()

        self.assertEqual(repos, self.expected_repos)
        self.assertIn("apache2", self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
