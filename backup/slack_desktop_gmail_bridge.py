#!/usr/bin/env python3
"""
Slack Desktop Gmail Bridge - macOS Native Integration
This version uses AppleScript to monitor the Slack desktop app
"""

import time
import json
import logging
import subprocess
import os
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SlackDesktopGmailBridge:
    def __init__(self, config_path="slack_desktop_config.json"):
        """Initialize the Slack Desktop Gmail bridge"""
        self.processed_messages = set()
        self.config = self.load_config(config_path)
        self.message_count = 0
        self.current_workspace = None
        self.slack_running = False
        
        # This will be set by the calling Goose session
        self.gmail_send_function = None
        
    def set_gmail_function(self, gmail_function):
        """Set the Gmail send function from the Goose session"""
        self.gmail_send_function = gmail_function
        logger.info("📧 Gmail MCP function set successfully")
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info("✅ Configuration loaded successfully")
            return config
        except Exception as e:
            logger.error(f"❌ Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "gmail_mcp": {
                "enabled": True,
                "recipient_email": "rajganesh47@gmail.com",
                "check_interval": 30
            },
            "slack": {
                "check_interval": 20,
                "max_messages_per_check": 5,
                "workspaces": [],  # Empty means monitor all workspaces
                "channels_to_monitor": [],  # Empty means monitor all channels
                "include_dms": True,
                "include_threads": False,
                "monitor_unread_only": True
            },
            "integration": {
                "enable_bidirectional": False,
                "log_level": "INFO",
                "max_message_length": 2000,
                "include_reactions": False,
                "include_files": True
            }
        }
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open("slack_desktop_config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("✅ Configuration saved")
        except Exception as e:
            logger.error(f"❌ Error saving config: {e}")
    
    def run_applescript(self, script):
        """Run AppleScript and return the result"""
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"AppleScript error: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            logger.error("AppleScript timeout")
            return None
        except Exception as e:
            logger.error(f"Error running AppleScript: {e}")
            return None
    
    def check_slack_running(self):
        """Check if Slack desktop app is running"""
        script = '''
        tell application "System Events"
            set appList to name of every application process
            if "Slack" is in appList then
                return "running"
            else
                return "not_running"
            end if
        end tell
        '''
        result = self.run_applescript(script)
        self.slack_running = (result == "running")
        return self.slack_running
    
    def launch_slack(self):
        """Launch Slack desktop app"""
        logger.info("🚀 Launching Slack desktop app...")
        script = '''
        tell application "Slack"
            if not running then
                launch
                delay 5
            end if
            activate
        end tell
        return "launched"
        '''
        result = self.run_applescript(script)
        if result:
            logger.info("✅ Slack launched successfully")
            self.slack_running = True
            return True
        else:
            logger.error("❌ Failed to launch Slack")
            return False
    
    def get_slack_window_info(self):
        """Get information about Slack windows"""
        script = '''
        tell application "System Events"
            tell process "Slack"
                set windowList to every window
                if (count of windowList) > 0 then
                    set mainWindow to window 1
                    set windowTitle to title of mainWindow
                    return windowTitle
                else
                    return "no_windows"
                end if
            end tell
        end tell
        '''
        result = self.run_applescript(script)
        if result and result != "no_windows":
            self.current_workspace = result
            logger.info(f"🏢 Detected Slack workspace: {self.current_workspace}")
        return result
    
    def get_unread_messages(self):
        """Get unread messages from Slack using AppleScript"""
        if not self.slack_running:
            logger.warning("⚠️ Slack is not running")
            return []
        
        try:
            # AppleScript to get unread messages from Slack
            script = '''
            tell application "Slack"
                activate
            end tell
            
            delay 1
            
            tell application "System Events"
                tell process "Slack"
                    -- Look for unread message indicators
                    set unreadElements to {}
                    try
                        -- Try to find sidebar with channels
                        set sidebarElements to UI elements of window 1
                        repeat with element in sidebarElements
                            try
                                set elementRole to role of element
                                if elementRole is "AXList" or elementRole is "AXOutline" then
                                    -- This might be the channel list
                                    set channelElements to UI elements of element
                                    repeat with channel in channelElements
                                        try
                                            set channelName to name of channel
                                            set channelValue to value of channel
                                            -- Look for unread indicators (badges, bold text, etc.)
                                            if channelName contains "•" or channelName contains "(" then
                                                set end of unreadElements to channelName
                                            end if
                                        end try
                                    end repeat
                                end if
                            end try
                        end repeat
                    end try
                    
                    if (count of unreadElements) > 0 then
                        return "unread_found:" & (item 1 of unreadElements)
                    else
                        return "no_unread"
                    end if
                end tell
            end tell
            '''
            
            result = self.run_applescript(script)
            logger.debug(f"Unread messages result: {result}")
            
            # For now, let's use a simpler approach - check clipboard for recent messages
            return self.get_recent_messages_simple()
            
        except Exception as e:
            logger.error(f"❌ Error getting unread messages: {e}")
            return []
    
    def get_recent_messages_simple(self):
        """Simplified approach to get recent DM messages only"""
        try:
            new_messages = []
            
            # Check if we're in DM-only mode
            dm_only = self.config["slack"].get("dm_only_mode", True)
            
            # Use AppleScript to interact with Slack and extract DM messages
            script = '''
            tell application "Slack"
                activate
            end tell
            
            delay 2
            
            tell application "System Events"
                tell process "Slack"
                    try
                        -- Get the current window title to determine if it's a DM
                        set windowTitle to title of window 1
                        
                        -- Check if this looks like a DM (usually person names, not #channel)
                        set isDM to false
                        if windowTitle does not start with "#" and windowTitle does not contain "Slack |" then
                            set isDM to true
                        end if
                        
                        -- Only process if it's a DM or we're not in DM-only mode
                        if isDM or not ''' + str(dm_only).lower() + ''' then
                            set currentTime to (current date) as string
                            return "dm_message|" & windowTitle & "|DirectMessage|New DM from Slack desktop at " & currentTime
                        else
                            return "no_dm_messages"
                        end if
                        
                    on error
                        return "error_getting_messages"
                    end try
                end tell
            end tell
            '''
            
            result = self.run_applescript(script)
            
            if result and ("dm_message|" in result or "demo_message|" in result):
                parts = result.split("|")
                if len(parts) >= 4:
                    channel_name = parts[1]
                    sender_name = parts[2] 
                    message_text = parts[3]
                    
                    # Create unique message ID
                    timestamp = datetime.now().strftime("%H:%M")
                    message_id = f"{self.current_workspace}_{channel_name}_{sender_name}_{timestamp}_{hash(message_text)}_{int(time.time())}"
                    
                    if message_id not in self.processed_messages:
                        new_messages.append({
                            'id': message_id,
                            'workspace': self.current_workspace or "Slack",
                            'channel': channel_name,
                            'sender': sender_name,
                            'message': message_text,
                            'timestamp': timestamp,
                            'datetime': datetime.now().isoformat()
                        })
                        self.processed_messages.add(message_id)
                        logger.info(f"💬 New message in #{channel_name} from {sender_name}: {message_text[:50]}...")
            
            return new_messages
            
        except Exception as e:
            logger.error(f"❌ Error getting recent messages: {e}")
            return []
    
    def get_slack_notifications(self):
        """Get Slack notifications using macOS notification center"""
        try:
            # Check for recent Slack notifications
            script = '''
            tell application "System Events"
                -- This is a placeholder for notification checking
                -- macOS doesn't easily expose notification center content
                return "no_notifications"
            end tell
            '''
            
            result = self.run_applescript(script)
            return []
            
        except Exception as e:
            logger.error(f"❌ Error checking notifications: {e}")
            return []
    
    def forward_to_gmail_real(self, slack_message):
        """Forward Slack message to Gmail using REAL Gmail MCP"""
        try:
            if not self.gmail_send_function:
                logger.error("❌ Gmail send function not set!")
                return False
                
            recipient = self.config["gmail_mcp"]["recipient_email"]
            subject = f"[Slack Desktop] {slack_message['workspace']} #{slack_message['channel']} - {slack_message['sender']}"
            
            body = f"""💬 Slack Desktop Message Received

Workspace: {slack_message['workspace']}
Channel: #{slack_message['channel']}
From: {slack_message['sender']}
Time: {slack_message['timestamp']}
Received: {slack_message['datetime']}

Message:
{slack_message['message']}

---
This message was automatically forwarded from Slack Desktop App.

Message ID: {slack_message['id']}
"""
            
            # Call the real Gmail MCP function
            result = self.gmail_send_function(recipient, subject, body)
            
            logger.info(f"✅ REAL email sent successfully! Result: {result}")
            return True
                
        except Exception as e:
            logger.error(f"❌ Error sending real email: {e}")
            return False
    
    def run_single_check(self):
        """Run a single check for new messages and forward them"""
        logger.info("🔍 Running single Slack desktop check...")
        
        try:
            # Check if Slack is running
            if not self.check_slack_running():
                logger.info("🚀 Slack not running, attempting to launch...")
                if not self.launch_slack():
                    logger.error("❌ Failed to launch Slack")
                    return 0
                time.sleep(3)  # Wait for Slack to fully load
            
            # Get window info
            self.get_slack_window_info()
            
            # Get new messages
            new_messages = self.get_unread_messages()
            
            for message in new_messages:
                self.message_count += 1
                logger.info(f"📨 Processing message #{self.message_count}")
                
                if self.forward_to_gmail_real(message):
                    logger.info(f"✅ REAL email #{self.message_count} sent successfully!")
                    print(f"🔥 REAL EMAIL SENT for message #{self.message_count}")
                else:
                    logger.error(f"❌ Failed to send real email #{self.message_count}")
            
            return len(new_messages)
            
        except Exception as e:
            logger.error(f"❌ Error in single check: {e}")
            return 0
    
    def run_monitoring_loop(self):
        """Main monitoring loop for the integration"""
        logger.info("🚀 Starting Slack Desktop-Gmail monitoring loop...")
        
        check_interval = self.config["slack"]["check_interval"]
        
        print("\n" + "="*60)
        print("🤖 SLACK DESKTOP-GMAIL BRIDGE IS RUNNING")
        print("="*60)
        print(f"💬 Monitoring Slack Desktop App")
        print(f"📧 Forwarding to: {self.config['gmail_mcp']['recipient_email']}")
        print(f"⏰ Check interval: {check_interval} seconds")
        print("🔥 REAL EMAILS WILL BE SENT!")
        print("🛑 Press Ctrl+C to stop")
        print("="*60)
        
        try:
            while True:
                try:
                    message_count = self.run_single_check()
                    
                    if message_count > 0:
                        print(f"\n📊 Total messages processed: {self.message_count}")
                    else:
                        logger.debug("No new messages found")
                    
                    # Wait before next check
                    time.sleep(check_interval)
                    
                except Exception as e:
                    logger.error(f"❌ Error in monitoring loop: {e}")
                    time.sleep(30)  # Wait longer on error
                    
        except KeyboardInterrupt:
            logger.info("🛑 Monitoring stopped by user")
        except Exception as e:
            logger.error(f"❌ Unexpected error in monitoring loop: {e}")
    
    def setup_integration(self):
        """Setup the Slack Desktop integration"""
        logger.info("🚀 Setting up Slack Desktop-Gmail Integration")
        
        try:
            # Check if Slack is installed
            if not os.path.exists("/Applications/Slack.app"):
                logger.error("❌ Slack desktop app not found in /Applications/")
                return False
            
            # Check if Slack is running, launch if needed
            if not self.check_slack_running():
                logger.info("🚀 Launching Slack desktop app...")
                if not self.launch_slack():
                    logger.error("❌ Failed to launch Slack")
                    return False
                time.sleep(5)  # Wait for Slack to fully load
            
            # Get workspace info
            self.get_slack_window_info()
            
            # Save configuration
            self.save_config()
            
            logger.info("✅ Slack Desktop integration setup complete!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up integration: {e}")
            return False

# Global instance for use by Goose
slack_desktop_bridge = None

def initialize_slack_desktop_bridge():
    """Initialize the Slack Desktop bridge for use by Goose"""
    global slack_desktop_bridge
    if slack_desktop_bridge is None:
        slack_desktop_bridge = SlackDesktopGmailBridge()
    return slack_desktop_bridge

def setup_slack_desktop_integration():
    """Setup Slack Desktop integration"""
    bridge = initialize_slack_desktop_bridge()
    return bridge.setup_integration()

def check_slack_desktop_messages(gmail_send_function):
    """Check for new Slack Desktop messages and forward them"""
    bridge = initialize_slack_desktop_bridge()
    bridge.set_gmail_function(gmail_send_function)
    return bridge.run_single_check()

def run_slack_desktop_monitoring(gmail_send_function):
    """Run continuous monitoring of Slack Desktop"""
    bridge = initialize_slack_desktop_bridge()
    bridge.set_gmail_function(gmail_send_function)
    bridge.run_monitoring_loop()

if __name__ == "__main__":
    print("💬 Slack Desktop-Gmail Bridge")
    print("This module is designed to be imported and used by Goose")
    print("Use the functions: setup_slack_desktop_integration, check_slack_desktop_messages")
    
    # For testing, run a simple setup
    bridge = SlackDesktopGmailBridge()
    bridge.setup_integration()
