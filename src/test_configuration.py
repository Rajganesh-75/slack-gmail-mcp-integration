#!/usr/bin/env python3
"""
Test Configuration Script
Validates that all required credentials and settings are properly configured.
"""

import json
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def check_config():
    """Check user configuration."""
    config_file = Path("config/user_config.json")
    if not config_file.exists():
        print("❌ User configuration not found. Run: python3 setup_config.py")
        return False
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        
        print("✅ User configuration loaded")
        print(f"   📧 Gmail: {config.get('gmail_address', 'Not set')}")
        print(f"   👤 Slack ID: {config.get('slack_user_id', 'Not set')}")
        print(f"   🔄 Check interval: {config.get('check_interval', 300)}s")
        return True
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def main():
    print("🧪 Configuration Test")
    print("=" * 30)
    
    all_good = True
    
    # Check user configuration
    print("\n📋 User Configuration:")
    if not check_config():
        all_good = False
    
    # Check credential files
    print("\n🔐 Credential Files:")
    cred_files = [
        ("credentials.json", "Gmail credentials"),
        ("token.json", "Gmail token (auto-generated)"),
        ("config/slack_token.env", "Slack token")
    ]
    
    for filepath, description in cred_files:
        if not check_file_exists(filepath, description):
            if filepath != "token.json":  # token.json is auto-generated
                all_good = False
    
    # Check Python dependencies
    print("\n📦 Python Dependencies:")
    try:
        import slack_sdk
        print("✅ slack-sdk: Available")
    except ImportError:
        print("❌ slack-sdk: Missing (run: pip install slack-sdk)")
        all_good = False
    
    # Check for MCP extensions (if using Goose)
    print("\n🤖 MCP Extensions (for Goose users):")
    print("   ℹ️  Slack MCP: Check in Goose settings")
    print("   ℹ️  Gmail Custom MCP: Check in Goose settings")
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Configuration looks good! Ready to run the integration.")
        print("\n🚀 Next steps:")
        print("   • Test with: python3 test_real_slack_mcp.py")
        print("   • Run integration: python3 slack_gmail_mcp_bridge.py")
    else:
        print("⚠️  Some issues found. Please check the items marked with ❌")
        print("\n📖 See SETUP.md for detailed instructions")

if __name__ == "__main__":
    main()
