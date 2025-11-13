#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""

        # Setup mock return value
        expected_value = {"login": org_name}
        mock_get_json.return_value = expected_value

        # Instantiate client
        client = GithubOrgClient(org_name)

        # Call the property
        result = client.org

        self.assertEqual(result, expected_value)

        # Assert get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Test memoization - call again
        result2 = client.org()
        self.assertEqual(result2, expected_value)
        # should still be called once due to memoization
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL."""

        # Mock payload returned by GithubOrgClient.org
        mocked_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        with patch.object(GithubOrgClient, "org", return_value=mocked_payload):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            # Validate output
            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""

        # Fake JSON payload returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        # Mock the repos URL property
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=unittest.mock.PropertyMock,
                          return_value="https://fakeurl.com/repos") as mock_url:

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Expected list of repo names
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Ensure the URL property was accessed once
            mock_url.assert_called_once()

            # Ensure get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with("https://fakeurl.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license static method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""

        def fake_get(url):
            mock = Mock()
            if url == "https://api.github.com/orgs/google":
                mock.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock.json.return_value = cls.repos_payload
            else:
                mock.json.return_value = {}
            return mock

        cls.get_patcher = patch("client.requests.get", side_effect=fake_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)