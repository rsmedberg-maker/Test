"""Configuration management for Jira integration."""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Config:
    """Load and manage configuration from environment variables."""

    def __init__(self):
        """Initialize configuration from environment."""
        self.jira_server: str = self._get_env("JIRA_SERVER")
        self.jira_username: str = self._get_env("JIRA_USERNAME")
        self.jira_api_token: str = self._get_env("JIRA_API_TOKEN")
        self.jira_project_key: str = self._get_env("JIRA_PROJECT_KEY")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    @staticmethod
    def _get_env(key: str) -> str:
        """Get environment variable and raise error if not found.
        
        Args:
            key: Environment variable name
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If environment variable is not set
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    def validate(self) -> bool:
        """Validate that all required configuration is set.
        
        Returns:
            True if valid, raises exception otherwise
        """
        required_fields = [
            self.jira_server,
            self.jira_username,
            self.jira_api_token,
            self.jira_project_key,
        ]
        if not all(required_fields):
            raise ValueError("Missing required configuration")
        return True

    def __repr__(self) -> str:
        """String representation of config (masks sensitive data)."""
        return (
            f"Config(server={self.jira_server}, "
            f"username={self.jira_username}, "
            f"project={self.jira_project_key})"
        )
