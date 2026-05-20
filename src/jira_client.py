"""Jira client for API interactions."""

import logging
from typing import Dict, List, Any, Optional
from jira import JIRA
from .config import Config

logger = logging.getLogger(__name__)


class JiraClient:
    """Client for interacting with Jira API."""

    def __init__(self, config: Config):
        """Initialize Jira client with configuration.
        
        Args:
            config: Config object with Jira credentials
        """
        self.config = config
        self.config.validate()
        
        auth = (config.jira_username, config.jira_api_token)
        self.client = JIRA(server=config.jira_server, basic_auth=auth)
        logger.info(f"Jira client initialized for {config.jira_project_key}")

    def create_issue(
        self,
        summary: str,
        description: str,
        issue_type: str = "Task",
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new Jira issue.
        
        Args:
            summary: Issue summary/title
            description: Issue description
            issue_type: Type of issue (Task, Bug, Story, etc.)
            **kwargs: Additional fields
            
        Returns:
            Created issue data
        """
        issue_dict = {
            "project": self.config.jira_project_key,
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
        issue_dict.update(kwargs)
        
        issue = self.client.create_issue(fields=issue_dict)
        logger.info(f"Created issue {issue.key}")
        return {"key": issue.key, "url": f"{self.config.jira_server}/browse/{issue.key}"}

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get issue details.
        
        Args:
            issue_key: Issue key (e.g., "PROJ-123")
            
        Returns:
            Issue data
        """
        issue = self.client.issue(issue_key)
        logger.info(f"Retrieved issue {issue_key}")
        return {
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "assignee": issue.fields.assignee.name if issue.fields.assignee else None,
        }

    def update_issue(self, issue_key: str, **kwargs) -> bool:
        """Update an existing issue.
        
        Args:
            issue_key: Issue key
            **kwargs: Fields to update
            
        Returns:
            True if successful
        """
        issue = self.client.issue(issue_key)
        issue.update(fields=kwargs)
        logger.info(f"Updated issue {issue_key}")
        return True

    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search issues using JQL.
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results
            
        Returns:
            List of issue data
        """
        issues = self.client.search_issues(jql, maxResults=max_results)
        logger.info(f"Found {len(issues)} issues")
        return [
            {
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
            }
            for issue in issues
        ]

    def add_comment(self, issue_key: str, comment: str) -> bool:
        """Add a comment to an issue.
        
        Args:
            issue_key: Issue key
            comment: Comment text
            
        Returns:
            True if successful
        """
        issue = self.client.issue(issue_key)
        self.client.add_comment(issue, comment)
        logger.info(f"Added comment to {issue_key}")
        return True

    def transition_issue(self, issue_key: str, transition_name: str) -> bool:
        """Transition issue to new status.
        
        Args:
            issue_key: Issue key
            transition_name: Name of transition (e.g., "Done", "In Progress")
            
        Returns:
            True if successful
        """
        issue = self.client.issue(issue_key)
        transitions = self.client.transitions(issue)
        
        for transition in transitions["transitions"]:
            if transition["name"] == transition_name:
                self.client.transition_issue(issue, transition["id"])
                logger.info(f"Transitioned {issue_key} to {transition_name}")
                return True
        
        logger.warning(f"Transition '{transition_name}' not found for {issue_key}")
        return False
