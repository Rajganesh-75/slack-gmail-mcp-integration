#!/usr/bin/env python3
"""
Configuration Loader
Loads user-specific configuration for the Slack-Gmail integration.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigLoader:
    """Handles loading and accessing user configuration."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from user_config.json."""
        config_file = self.config_dir / "user_config.json"
        
        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}\n"
                "Please run: python3 setup_config.py"
            )
        
        try:
            with open(config_file) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def get_gmail_address(self) -> str:
        """Get the configured Gmail address."""
        # Try new format first
        email = self.config.get("user", {}).get("email_address")
        if not email:
            # Fallback to old format
            email = self.config.get("gmail_address")
        if not email:
            raise ValueError("Gmail address not configured. Please run setup_config.py")
        return email
    
    def get_slack_user_id(self) -> Optional[str]:
        """Get the configured Slack user ID."""
        # Try new format first
        user_id = self.config.get("user", {}).get("slack_user_id")
        if not user_id:
            # Fallback to old format
            user_id = self.config.get("slack_user_id")
        return user_id
    
    def get_slack_username(self) -> Optional[str]:
        """Get the configured Slack username."""
        return self.config.get("user", {}).get("slack_username")
    
    def get_check_interval(self) -> int:
        """Get the check interval in seconds."""
        return self.config.get("check_interval", 300)
    
    def get_max_messages_per_check(self) -> int:
        """Get the maximum messages per check."""
        return self.config.get("max_messages_per_check", 10)
    
    def should_monitor_dms(self) -> bool:
        """Check if DM monitoring is enabled."""
        # Try new format first
        monitor_dms = self.config.get("slack", {}).get("monitor_dms")
        if monitor_dms is None:
            # Fallback to old format
            monitor_dms = self.config.get("monitor_dms", True)
        return monitor_dms
    
    def should_monitor_mentions(self) -> bool:
        """Check if mention monitoring is enabled."""
        # Try new format first
        monitor_mentions = self.config.get("slack", {}).get("monitor_mentions")
        if monitor_mentions is None:
            # Fallback to old format
            monitor_mentions = self.config.get("monitor_mentions", True)
        return monitor_mentions
    
    def get_mention_keywords(self) -> list:
        """Get additional mention keywords."""
        # Try new format first
        keywords = self.config.get("email", {}).get("keywords")
        if not keywords:
            # Fallback to old format
            keywords = self.config.get("mention_keywords", [])
        return keywords
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get the complete configuration."""
        return self.config.copy()

# Global config instance
_config_instance = None

def get_config() -> ConfigLoader:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance

def reload_config():
    """Reload the configuration from file."""
    global _config_instance
    _config_instance = None
    return get_config()
