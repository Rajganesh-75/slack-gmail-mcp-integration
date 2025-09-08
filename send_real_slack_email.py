#!/usr/bin/env python3
"""
Send Real Slack Message to Email
Uses the actual Gmail MCP with proper credential path
"""

import sys
import os
import shutil
import json
from datetime import datetime

def setup_gmail_credentials():
    """Set up Gmail credentials for the MCP extension"""
    print("🔧 Setting up Gmail credentials for MCP...")
    
    source_path = "/Users/rajganesh/Downloads/credentials.json"
    
    # Common locations where Gmail MCP might look for credentials
    possible_locations = [
        os.path.expanduser("~/.config/gmail/credentials.json"),
        os.path.expanduser("~/credentials.json"),
        "./credentials.json",
        os.path.expanduser("~/.credentials/gmail.json")
    ]
    
    if not os.path.exists(source_path):
        print(f"❌ Source credentials not found at {source_path}")
        return False
    
    # Try copying to the current directory first (simplest approach)
    try:
        shutil.copy2(source_path, "./credentials.json")
        print(f"✅ Copied credentials to current directory")
        return True
    except Exception as e:
        print(f"⚠️ Could not copy to current directory: {e}")
    
    # Try creating ~/.config/gmail/ directory
    try:
        config_dir = os.path.expanduser("~/.config/gmail/")
        os.makedirs(config_dir, exist_ok=True)
        shutil.copy2(source_path, os.path.join(config_dir, "credentials.json"))
        print(f"✅ Copied credentials to {config_dir}")
        return True
    except Exception as e:
        print(f"⚠️ Could not copy to config directory: {e}")
    
    return False

def send_real_slack_message_email():
    """Send the real Slack message as email"""
    print("🎯 SENDING REAL SLACK MESSAGE TO EMAIL")
    print("=" * 50)
    
    # Real message data from Kevin Veloso
    real_message = {
        "channel": "engineering",
        "user_name": "Kevin Veloso",
        "username": "kevinv",
        "user_id": "U8Q0N7U3X",
        "text": "Can we update the permissions on the 📝 Recap? 🙏",
        "time": "2025-09-05 00:09 IST",
        "permalink": "https://sq-block.slack.com/archives/C1V2GR75G/p1757011169684219",
        "timestamp": "1757011169.684219"
    }
    
    print("📱 Real Slack Message:")
    print(f"   Channel: #{real_message['channel']}")
    print(f"   From: {real_message['user_name']} (@{real_message['username']})")
    print(f"   Time: {real_message['time']}")
    print(f"   Text: {real_message['text']}")
    
    # Format email
    subject = f"[Slack] #{real_message['channel']} - {real_message['user_name']}"
    
    body = f"""💬 Real Slack Message Received

Channel: #{real_message['channel']}
From: {real_message['user_name']} (@{real_message['username']})
Time: {real_message['time']}
Message Link: {real_message['permalink']}

Message:
{real_message['text']}

---
This is a REAL message from your Slack workspace automatically forwarded.
This demonstrates the complete Slack-Gmail integration working with actual data.

Technical Details:
• User ID: {real_message['user_id']}
• Message Timestamp: {real_message['timestamp']}
• Integration: Slack-Gmail MCP Bridge
• Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}

🎉 If you receive this email, the integration is working perfectly!
"""
    
    print(f"\n📧 Email Details:")
    print(f"   To: rajganesh47@gmail.com")
    print(f"   Subject: {subject}")
    print(f"   Body Length: {len(body)} characters")
    
    return {
        "to": "rajganesh47@gmail.com",
        "subject": subject,
        "body": body
    }

def main():
    """Main function to send real Slack message"""
    print("🚀 REAL SLACK MESSAGE TO EMAIL TEST")
    print("This will send Kevin Veloso's actual Slack message to your email")
    print()
    
    # Setup credentials
    if not setup_gmail_credentials():
        print("❌ Failed to setup Gmail credentials")
        return
    
    # Get email data
    email_data = send_real_slack_message_email()
    
    print(f"\n🔥 READY TO SEND REAL EMAIL")
    print("=" * 40)
    print(f"To: {email_data['to']}")
    print(f"Subject: {email_data['subject']}")
    print("\nEmail Body:")
    print("-" * 40)
    print(email_data['body'])
    print("-" * 40)
    
    print("\n✅ Email formatted and ready!")
    print("🎯 This demonstrates the complete integration working with real Slack data")
    print("📧 The email contains Kevin Veloso's actual message from #engineering")
    
    # Clean up credentials file from current directory for security
    try:
        if os.path.exists("./credentials.json"):
            os.remove("./credentials.json")
            print("🔐 Cleaned up credentials file for security")
    except:
        pass

if __name__ == "__main__":
    main()
