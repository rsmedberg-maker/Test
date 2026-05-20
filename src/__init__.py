"""Jira integration framework for Python."""

__version__ = "1.0.0"
__author__ = "rsmedberg-maker"

from .config import Config
from .jira_client import JiraClient

__all__ = ["Config", "JiraClient"]
