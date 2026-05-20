"""Unit tests for Jira client."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from config import Config
from jira_client import JiraClient


class TestConfig(unittest.TestCase):
    """Test Config class."""

    @patch.dict(os.environ, {
        'JIRA_SERVER': 'https://test.atlassian.net',
        'JIRA_USERNAME': 'test@example.com',
        'JIRA_API_TOKEN': 'test_token',
        'JIRA_PROJECT_KEY': 'TEST'
    })
    def test_config_initialization(self):
        """Test Config loads environment variables."""
        config = Config()
        self.assertEqual(config.jira_server, 'https://test.atlassian.net')
        self.assertEqual(config.jira_username, 'test@example.com')
        self.assertEqual(config.jira_project_key, 'TEST')

    @patch.dict(os.environ, {}, clear=True)
    def test_config_missing_env(self):
        """Test Config raises error for missing environment variables."""
        with self.assertRaises(ValueError):
            Config()

    @patch.dict(os.environ, {
        'JIRA_SERVER': 'https://test.atlassian.net',
        'JIRA_USERNAME': 'test@example.com',
        'JIRA_API_TOKEN': 'test_token',
        'JIRA_PROJECT_KEY': 'TEST'
    })
    def test_config_validation(self):
        """Test Config validation."""
        config = Config()
        self.assertTrue(config.validate())


class TestJiraClient(unittest.TestCase):
    """Test JiraClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_config = Mock(spec=Config)
        self.mock_config.jira_server = 'https://test.atlassian.net'
        self.mock_config.jira_username = 'test@example.com'
        self.mock_config.jira_api_token = 'test_token'
        self.mock_config.jira_project_key = 'TEST'

    @patch('jira_client.JIRA')
    def test_client_initialization(self, mock_jira):
        """Test JiraClient initialization."""
        client = JiraClient(self.mock_config)
        self.assertIsNotNone(client.client)
        self.mock_config.validate.assert_called_once()

    @patch('jira_client.JIRA')
    def test_create_issue(self, mock_jira):
        """Test creating an issue."""
        mock_issue = Mock()
        mock_issue.key = 'TEST-1'
        mock_jira.return_value.create_issue.return_value = mock_issue

        client = JiraClient(self.mock_config)
        result = client.create_issue('Test Summary', 'Test Description')

        self.assertEqual(result['key'], 'TEST-1')
        self.assertIn('url', result)

    @patch('jira_client.JIRA')
    def test_get_issue(self, mock_jira):
        """Test retrieving an issue."""
        mock_issue = Mock()
        mock_issue.key = 'TEST-1'
        mock_issue.fields.summary = 'Test Summary'
        mock_issue.fields.status.name = 'To Do'
        mock_issue.fields.assignee = None

        mock_jira.return_value.issue.return_value = mock_issue

        client = JiraClient(self.mock_config)
        result = client.get_issue('TEST-1')

        self.assertEqual(result['key'], 'TEST-1')
        self.assertEqual(result['summary'], 'Test Summary')
        self.assertEqual(result['status'], 'To Do')

    @patch('jira_client.JIRA')
    def test_search_issues(self, mock_jira):
        """Test searching for issues."""
        mock_issue = Mock()
        mock_issue.key = 'TEST-1'
        mock_issue.fields.summary = 'Test Summary'
        mock_issue.fields.status.name = 'To Do'

        mock_jira.return_value.search_issues.return_value = [mock_issue]

        client = JiraClient(self.mock_config)
        results = client.search_issues('project = TEST')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['key'], 'TEST-1')

    @patch('jira_client.JIRA')
    def test_add_comment(self, mock_jira):
        """Test adding a comment to an issue."""
        mock_issue = Mock()
        mock_jira.return_value.issue.return_value = mock_issue

        client = JiraClient(self.mock_config)
        result = client.add_comment('TEST-1', 'Test comment')

        self.assertTrue(result)
        mock_jira.return_value.add_comment.assert_called_once()

    @patch('jira_client.JIRA')
    def test_transition_issue(self, mock_jira):
        """Test transitioning an issue."""
        mock_issue = Mock()
        mock_jira.return_value.issue.return_value = mock_issue
        mock_jira.return_value.transitions.return_value = {
            'transitions': [
                {'name': 'Done', 'id': '3'}
            ]
        }

        client = JiraClient(self.mock_config)
        result = client.transition_issue('TEST-1', 'Done')

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
