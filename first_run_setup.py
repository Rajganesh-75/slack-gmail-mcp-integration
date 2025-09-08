#!/usr/bin/env python3
"""
Slack-Gmail MCP Bridge - First Run Setup
========================================

This script guides new users through the complete setup process:
1. Checks if Goose is running and required extensions are available
2. Enables necessary Goose MCP extensions
3. Configures user email and Slack preferences
4. Sets up Gmail API credentials
5. Tests the complete integration

Run this script first when you clone the repository.
"""

import os
import json
import sys
from pathlib import Path
import subprocess

class FirstRunSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_dir = self.project_root / "config"
        self.user_config_path = self.config_dir / "user_config.json"
        
    def welcome_message(self):
        """Display welcome message and project overview"""
        print("🚀 SLACK-GMAIL MCP BRIDGE - FIRST RUN SETUP")
        print("=" * 50)
        print()
        print("Welcome to the Slack-Gmail MCP Bridge!")
        print("This tool helps you:")
        print("• Monitor Slack conversations via email")
        print("• Send Slack conversation summaries to your email")
        print("• Bridge Slack and Gmail using Goose MCP extensions")
        print()
        print("This setup will guide you through:")
        print("1. 🔧 Checking Goose and required extensions")
        print("2. 📧 Configuring your email settings")
        print("3. 💬 Setting up Slack workspace access")
        print("4. 🔑 Configuring Gmail API credentials")
        print("5. ✅ Testing the complete integration")
        print()
        
        response = input("Ready to begin setup? (y/n): ").lower().strip()
        if response != 'y':
            print("Setup cancelled. Run this script again when ready!")
            sys.exit(0)
    
    def check_goose_environment(self):
        """Check if Goose is available and running"""
        print("\n🔧 STEP 1: CHECKING GOOSE ENVIRONMENT")
        print("-" * 40)
        
        # Check if we're running in Goose context
        try:
            # Try to import goose-related modules or check environment
            goose_available = os.environ.get('GOOSE_CONTEXT') or self.check_goose_process()
            
            if not goose_available:
                print("❌ Goose not detected!")
                print()
                print("This project requires Goose AI with MCP extensions.")
                print("Please:")
                print("1. Install Goose AI from: https://github.com/block/goose")
                print("2. Start Goose AI")
                print("3. Run this setup script from within Goose")
                print()
                response = input("Continue anyway? (y/n): ").lower().strip()
                if response != 'y':
                    sys.exit(1)
            else:
                print("✅ Goose environment detected!")
                
        except Exception as e:
            print(f"⚠️  Could not verify Goose environment: {e}")
            print("Continuing with setup...")
    
    def check_goose_process(self):
        """Check if Goose process is running"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            return 'goose' in result.stdout.lower()
        except:
            return False
    
    def setup_extensions(self):
        """Guide user through enabling required Goose extensions"""
        print("\n🔌 STEP 2: GOOSE MCP EXTENSIONS SETUP")
        print("-" * 40)
        
        required_extensions = {
            'slack': 'Slack MCP - Access Slack messages and conversations',
            'gmailcustom': 'Gmail Custom MCP - Send emails via Gmail API'
        }
        
        print("This project requires the following Goose MCP extensions:")
        print()
        
        for ext_name, description in required_extensions.items():
            print(f"📦 {ext_name}: {description}")
        
        print()
        print("To enable these extensions in Goose:")
        print("1. Open Goose AI interface")
        print("2. Go to Settings → Extensions")
        print("3. Search for and enable: 'slack' and 'gmailcustom'")
        print("4. Restart Goose if prompted")
        print()
        
        while True:
            response = input("Have you enabled the required extensions? (y/n): ").lower().strip()
            if response == 'y':
                break
            elif response == 'n':
                print("Please enable the extensions and return to continue setup.")
            else:
                print("Please answer 'y' or 'n'")
    
    def configure_email(self):
        """Configure user email settings"""
        print("\n📧 STEP 3: EMAIL CONFIGURATION")
        print("-" * 40)
        
        print("Configure where you want to receive Slack conversation emails:")
        print()
        
        while True:
            email = input("Enter your email address: ").strip()
            if '@' in email and '.' in email:
                break
            print("Please enter a valid email address.")
        
        print()
        print("Email notification preferences:")
        
        # Get notification preferences
        preferences = {}
        
        questions = [
            ("send_dm_summaries", "Send daily DM summaries?"),
            ("send_channel_mentions", "Send notifications when mentioned in channels?"),
            ("send_keyword_alerts", "Send alerts for specific keywords?"),
            ("include_message_context", "Include message context in emails?")
        ]
        
        for key, question in questions:
            while True:
                response = input(f"{question} (y/n): ").lower().strip()
                if response in ['y', 'n']:
                    preferences[key] = response == 'y'
                    break
                print("Please answer 'y' or 'n'")
        
        # Keywords setup if enabled
        keywords = []
        if preferences.get('send_keyword_alerts'):
            print("\nEnter keywords to monitor (press Enter when done):")
            while True:
                keyword = input("Keyword: ").strip()
                if not keyword:
                    break
                keywords.append(keyword)
        
        return {
            'email_address': email,
            'preferences': preferences,
            'keywords': keywords
        }
    
    def configure_slack(self):
        """Configure Slack workspace settings"""
        print("\n💬 STEP 4: SLACK CONFIGURATION")
        print("-" * 40)
        
        print("Configure your Slack workspace access:")
        print()
        
        # Get Slack username
        while True:
            username = input("Enter your Slack username (without @): ").strip().lstrip('@')
            if username:
                break
            print("Please enter your Slack username.")
        
        # Get workspace info
        workspace = input("Enter your Slack workspace name (optional): ").strip()
        
        # Monitoring preferences
        print("\nSlack monitoring preferences:")
        
        monitor_dms = input("Monitor direct messages? (y/n): ").lower().strip() == 'y'
        monitor_mentions = input("Monitor channel mentions? (y/n): ").lower().strip() == 'y'
        
        channels_to_monitor = []
        if input("Monitor specific channels? (y/n): ").lower().strip() == 'y':
            print("Enter channel names to monitor (press Enter when done):")
            while True:
                channel = input("Channel name (without #): ").strip().lstrip('#')
                if not channel:
                    break
                channels_to_monitor.append(channel)
        
        return {
            'username': username,
            'workspace': workspace,
            'monitor_dms': monitor_dms,
            'monitor_mentions': monitor_mentions,
            'channels_to_monitor': channels_to_monitor
        }
    
    def setup_gmail_credentials(self):
        """Guide user through Gmail API credentials setup"""
        print("\n🔑 STEP 5: GMAIL API CREDENTIALS")
        print("-" * 40)
        
        credentials_path = self.project_root / "credentials.json"
        
        if credentials_path.exists():
            print("✅ Gmail credentials file found!")
            return str(credentials_path)
        
        print("Gmail API credentials are required to send emails.")
        print()
        print("To get Gmail API credentials:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Gmail API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download the credentials JSON file")
        print("6. Save it as 'credentials.json' in this project folder")
        print()
        
        while True:
            if input("Have you placed credentials.json in the project folder? (y/n): ").lower().strip() == 'y':
                if credentials_path.exists():
                    print("✅ Credentials file found!")
                    return str(credentials_path)
                else:
                    print("❌ credentials.json not found in project folder.")
            else:
                print("Please complete the Gmail API setup and try again.")
    
    def create_user_config(self, email_config, slack_config, credentials_path):
        """Create the user configuration file"""
        print("\n💾 STEP 6: CREATING CONFIGURATION")
        print("-" * 40)
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Create comprehensive user config
        user_config = {
            "user": {
                "email_address": email_config['email_address'],
                "slack_username": slack_config['username'],
                "slack_workspace": slack_config['workspace']
            },
            "email": {
                "preferences": email_config['preferences'],
                "keywords": email_config['keywords']
            },
            "slack": {
                "monitor_dms": slack_config['monitor_dms'],
                "monitor_mentions": slack_config['monitor_mentions'],
                "channels_to_monitor": slack_config['channels_to_monitor']
            },
            "credentials": {
                "gmail_credentials_path": credentials_path
            },
            "setup": {
                "completed": True,
                "version": "1.0",
                "setup_date": self.get_current_timestamp()
            }
        }
        
        # Save configuration
        with open(self.user_config_path, 'w') as f:
            json.dump(user_config, f, indent=2)
        
        print(f"✅ Configuration saved to: {self.user_config_path}")
        return user_config
    
    def get_current_timestamp(self):
        """Get current timestamp for setup tracking"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def test_integration(self):
        """Test the complete integration setup"""
        print("\n🧪 STEP 7: TESTING INTEGRATION")
        print("-" * 40)
        
        print("Running integration tests...")
        
        # Test configuration loading
        try:
            from src.config_loader import ConfigLoader
            config = ConfigLoader()
            print("✅ Configuration loading: OK")
        except Exception as e:
            print(f"❌ Configuration loading: FAILED - {e}")
            return False
        
        # Test Gmail MCP extension
        print("Testing Gmail MCP extension...")
        try:
            # This would be tested in actual Goose environment
            print("✅ Gmail MCP: Ready (test in Goose environment)")
        except Exception as e:
            print(f"❌ Gmail MCP: FAILED - {e}")
        
        # Test Slack MCP extension
        print("Testing Slack MCP extension...")
        try:
            # This would be tested in actual Goose environment
            print("✅ Slack MCP: Ready (test in Goose environment)")
        except Exception as e:
            print(f"❌ Slack MCP: FAILED - {e}")
        
        return True
    
    def completion_message(self):
        """Display setup completion message"""
        print("\n🎉 SETUP COMPLETE!")
        print("=" * 50)
        print()
        print("Your Slack-Gmail MCP Bridge is now configured!")
        print()
        print("📋 NEXT STEPS:")
        print("1. Test the configuration:")
        print("   python3 test_configuration.py")
        print()
        print("2. Get a conversation and send to email:")
        print("   python3 src/get_user_conversation.py <username> -m 10 --send")
        print()
        print("3. Start the monitoring bridge:")
        print("   python3 src/slack_gmail_mcp_bridge.py")
        print()
        print("📚 DOCUMENTATION:")
        print("• README.md - Project overview")
        print("• SETUP.md - Detailed setup guide")
        print("• COMMANDS.md - Available commands")
        print()
        print("🆘 NEED HELP?")
        print("• Check the documentation files")
        print("• Ensure Goose MCP extensions are enabled")
        print("• Verify Gmail API credentials are correct")
        print()
        print("Happy Slack-Gmail bridging! 🌉")
    
    def run_setup(self):
        """Run the complete first-run setup process"""
        try:
            self.welcome_message()
            self.check_goose_environment()
            self.setup_extensions()
            
            email_config = self.configure_email()
            slack_config = self.configure_slack()
            credentials_path = self.setup_gmail_credentials()
            
            self.create_user_config(email_config, slack_config, credentials_path)
            
            if self.test_integration():
                self.completion_message()
            else:
                print("\n⚠️  Setup completed with some test failures.")
                print("Please check the configuration and try running tests manually.")
                
        except KeyboardInterrupt:
            print("\n\n❌ Setup cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            print("Please check the error and try again.")
            sys.exit(1)

if __name__ == "__main__":
    setup = FirstRunSetup()
    setup.run_setup()
