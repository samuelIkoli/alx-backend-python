import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""

        # Setup mock return value
        mock_get_json.return_value = {"payload": True}

        # Instantiate client
        client = GithubOrgClient(org_name)

        # Call the property
        result = client.org

        # Assert get_json was called once with expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert result is mock return value
        self.assertEqual(result, {"payload": True})

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