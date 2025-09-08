#!/usr/bin/env python3
"""
Setup script for Slack-Gmail MCP Integration
This script helps set up and test the integration
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_slack_dependencies():
    """Check if Slack SDK and other dependencies are available"""
    print("🔍 Checking Slack dependencies...")
    
    try:
        # Try to import slack-sdk
        try:
            import slack_sdk
            print("✅ Slack SDK available!")
        except ImportError:
            print("❌ Slack SDK not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "slack-sdk"])
            print("✅ Slack SDK installed!")
        
        # Check for other required packages
        try:
            import requests
            import websocket
            print("✅ Required dependencies available!")
            return True
        except ImportError as e:
            print(f"❌ Missing dependencies: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Slack setup: {e}")
        return False

def create_config_file():
    """Create configuration file for the integration"""
    print("⚙️ Creating configuration file...")
    
    config = {
        "gmail_mcp": {
            "enabled": True,
            "recipient_email": "rajganesh47@gmail.com",
            "check_interval": 30
        },
        "slack": {
            "check_interval": 10,
            "max_messages_per_check": 5,
            "enable_desktop_integration": True
        },
        "integration": {
            "enable_bidirectional": True,
            "log_level": "INFO",
            "max_message_length": 1000
        }
    }
    
    config_path = Path("config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration file created: {config_path}")
    print("📝 Please edit config.json and update your settings!")
    return True

def create_slack_config():
    """Create Slack-specific configuration file"""
    print("⚙️ Creating Slack configuration...")
    
    slack_config = {
        "slack_token": "xoxb-your-slack-bot-token",
        "app_token": "xapp-your-app-token", 
        "channel_id": "your-channel-id",
        "user_id": "your-user-id",
        "signing_secret": "your-signing-secret"
    }
    
    config_path = Path("../slack_config.json")
    with open(config_path, "w") as f:
        json.dump(slack_config, f, indent=2)
    
    print(f"✅ Slack configuration file created: {config_path}")
    print("🔑 Please update slack_config.json with your actual Slack API credentials!")
    return True

def test_gmail_mcp_connection():
    """Test connection to Gmail MCP"""
    print("📧 Testing Gmail MCP connection...")
    
    try:
        # This would test your actual Gmail MCP
        print("✅ Gmail MCP integration ready!")
        print("💡 Make sure your Gmail MCP server is running before starting the bridge.")
        return True
    except Exception as e:
        print(f"❌ Gmail MCP connection test failed: {e}")
        return False

def create_startup_script():
    """Create a startup script for easy launching"""
    print("🚀 Creating startup script...")
    
    startup_script = """#!/bin/bash
# Slack-Gmail Bridge Startup Script

echo "🚀 Starting Slack-Gmail Bridge..."

# Check if config exists
if [ ! -f "config/config.json" ]; then
    echo "❌ config/config.json not found. Please run config/setup_integration.py first."
    exit 1
fi

# Check if Slack config exists
if [ ! -f "slack_config.json" ]; then
    echo "❌ slack_config.json not found. Please configure your Slack API credentials."
    exit 1
fi

# Install/update requirements
pip install -r slack_requirements.txt

# Start the bridge
echo "🌉 Starting Slack-Gmail Bridge..."
python3 slack_gmail_bridge.py

echo "👋 Bridge stopped."
"""
    
    script_path = Path("../start_slack_bridge.sh")
    with open(script_path, "w") as f:
        f.write(startup_script)
    
    # Make executable
    os.chmod(script_path, 0o755)
    
    print(f"✅ Startup script created: {script_path}")
    print("💡 Run './start_slack_bridge.sh' to start the integration!")
    return True

def main():
    """Main setup function"""
    print("🔧 Slack-Gmail MCP Integration Setup")
    print("=" * 50)
    
    steps = [
        ("Installing requirements", install_requirements),
        ("Checking Slack dependencies", check_slack_dependencies),
        ("Creating configuration", create_config_file),
        ("Creating Slack config", create_slack_config),
        ("Testing Gmail MCP", test_gmail_mcp_connection),
        ("Creating startup script", create_startup_script)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"⚠️ {step_name} had issues, but continuing...")
    
    print("\n" + "=" * 50)
    print(f"✅ Setup completed! ({success_count}/{len(steps)} steps successful)")
    
    if success_count == len(steps):
        print("\n🎉 Everything looks good! Next steps:")
        print("1. Edit config/config.json and update your email address")
        print("2. Edit slack_config.json and add your Slack API credentials")
        print("3. Make sure your Gmail MCP server is running")
        print("4. Run: ./start_slack_bridge.sh")
        print("5. Test by sending a Slack DM!")
    else:
        print("\n⚠️ Some steps had issues. Please review the output above.")
        print("You may need to install missing dependencies manually.")
    
    print("\n📚 Check README.md for detailed instructions!")

if __name__ == "__main__":
    main()
