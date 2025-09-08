#!/usr/bin/env python3
"""
Interactive Setup Configuration for Slack-Gmail Bridge
Creates user-specific configuration for the integration.
"""

import json
import os
import sys
from pathlib import Path

def get_user_input(prompt, default=None, required=True):
    """Get user input with optional default value."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        value = input(full_prompt).strip()
        if value:
            return value
        elif default:
            return default
        elif not required:
            return None
        else:
            print("This field is required. Please enter a value.")

def validate_email(email):
    """Basic email validation."""
    return "@" in email and "." in email.split("@")[1]

def main():
    print("🚀 Slack-Gmail Bridge Setup")
    print("=" * 40)
    print("This will create your personal configuration for the Slack-Gmail integration.")
    print()
    
    # Get user configuration
    config = {}
    
    print("📧 Gmail Configuration:")
    while True:
        gmail_address = get_user_input("Your Gmail address (where messages will be sent)")
        if validate_email(gmail_address):
            config["gmail_address"] = gmail_address
            break
        else:
            print("Please enter a valid email address.")
    
    print("\n👤 Slack Configuration:")
    print("You can find your Slack user ID by:")
    print("1. Going to your Slack profile")
    print("2. Clicking 'More' → 'Copy member ID'")
    print("Or leave blank to configure later.")
    
    slack_user_id = get_user_input("Your Slack User ID (e.g., U1234567890)", required=False)
    if slack_user_id:
        config["slack_user_id"] = slack_user_id
    
    print("\n🎯 Integration Settings:")
    config["monitor_dms"] = get_user_input("Monitor direct messages? (y/n)", "y").lower().startswith('y')
    config["monitor_mentions"] = get_user_input("Monitor mentions? (y/n)", "y").lower().startswith('y')
    
    if config["monitor_mentions"]:
        config["mention_keywords"] = get_user_input("Additional keywords to monitor (comma-separated)", required=False)
        if config["mention_keywords"]:
            config["mention_keywords"] = [kw.strip() for kw in config["mention_keywords"].split(",")]
    
    print("\n⚙️ Advanced Settings:")
    config["check_interval"] = int(get_user_input("Check interval in seconds", "300"))
    config["max_messages_per_check"] = int(get_user_input("Max messages per check", "10"))
    
    # Create config directory if it doesn't exist
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Save configuration
    config_file = config_dir / "user_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, indent=2, fp=f)
    
    print(f"\n✅ Configuration saved to {config_file}")
    print("\n📋 Next Steps:")
    print("1. Set up your Gmail credentials (see SETUP.md)")
    print("2. Configure Slack access (see SETUP.md)")
    print("3. Run: python3 test_configuration.py")
    print("\n🔧 To reconfigure later, just run this script again.")

if __name__ == "__main__":
    main()
