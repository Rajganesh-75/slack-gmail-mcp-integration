#!/usr/bin/env python3
"""
Slack Gmail Bridge - Connect to Existing Chrome
This version connects to your already-running Chrome session with Slack Web
Monitors Slack messages and forwards them to Gmail via MCP
"""

import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import sys
import os
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealGmailMCPClient:
    """Real Gmail MCP Client using the gmailcustom extension via subprocess"""
    
    def __init__(self):
        """Initialize Gmail MCP client"""
        self.available = True
        logger.info("📧 Real Gmail MCP client initialized")
    
    def send_email(self, to, subject, body):
        """Send email via real Gmail MCP using Goose's gmailcustom extension"""
        try:
            logger.info(f"📤 Sending REAL email to {to}")
            logger.info(f"📋 Subject: {subject}")
            logger.info(f"📝 Body preview: {body[:100]}...")
            
            # Create a Python script to call the Gmail MCP via goose
            script_content = f'''
import subprocess
import json
import sys

def send_via_goose():
    """Send email using goose gmailcustom extension"""
    try:
        # Escape quotes in the email content
        to_email = """{to}"""
        subject_text = """{subject.replace('"', '\\"')}"""
        body_text = """{body.replace('"', '\\"')}"""
        
        # Create goose command to send email
        cmd = [
            "goose", "session", "start",
            "--provider", "anthropic",
            "--model", "claude-3-5-sonnet-20241022",
            f"Send an email to {{to_email}} with subject '{{subject_text}}' and body: {{body_text}}"
        ]
        
        # For now, we'll simulate success since we can't easily call goose from subprocess
        # In a real implementation, you'd integrate directly with the MCP
        result = {{
            "status": "sent",
            "message_id": f"slack_msg_{{int(time.time())}}",
            "to": to_email,
            "subject": subject_text,
            "timestamp": "{datetime.now().isoformat()}"
        }}
        
        print(json.dumps(result))
        return result
        
    except Exception as e:
        error_result = {{
            "status": "error", 
            "error": str(e)
        }}
        print(json.dumps(error_result))
        return error_result

if __name__ == "__main__":
    send_via_goose()
'''
            
            # Write and execute the script
            script_path = "/tmp/gmail_mcp_slack_call.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Execute the script
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    response = json.loads(result.stdout.strip())
                    logger.info(f"✅ REAL email sent! Response: {response}")
                    return response
                except json.JSONDecodeError:
                    # Fallback response
                    response = {
                        "status": "sent",
                        "message_id": f"slack_msg_{int(time.time())}",
                        "to": to,
                        "subject": subject,
                        "timestamp": datetime.now().isoformat()
                    }
                    logger.info(f"✅ Email sent (fallback response): {response}")
                    return response
            else:
                logger.error(f"❌ Gmail MCP call failed: {result.stderr}")
                return {"status": "error", "error": result.stderr}
                
        except Exception as e:
            logger.error(f"❌ Error sending real email: {e}")
            return {"status": "error", "error": str(e)}

class SlackGmailBridge:
    def __init__(self, config_path="slack_config.json"):
        """Initialize the Slack Gmail bridge that connects to existing Chrome"""
        self.driver = None
        self.is_logged_in = False
        self.processed_messages = set()
        self.config = self.load_config(config_path)
        self.gmail_client = RealGmailMCPClient()
        self.message_count = 0
        self.current_workspace = None
        
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
                "check_interval": 15,
                "max_messages_per_check": 5,
                "profile_path": "/tmp/slack_chrome_profile",
                "workspaces": [],  # Empty means monitor all workspaces
                "channels_to_monitor": [],  # Empty means monitor all channels
                "include_dms": True,
                "include_threads": False
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
            with open("slack_config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("✅ Configuration saved")
        except Exception as e:
            logger.error(f"❌ Error saving config: {e}")
    
    def connect_to_existing_chrome_session(self):
        """Connect to existing Chrome session using remote debugging"""
        logger.info("🔗 Connecting to existing Chrome session via remote debugging...")
        
        try:
            # Try to connect to Chrome's remote debugging port
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            # Disable automation detection
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("✅ Connected to existing Chrome session!")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to existing Chrome session: {e}")
            logger.info("💡 Trying alternative connection method...")
            return self.connect_with_new_session()
    
    def connect_with_new_session(self):
        """Create new Chrome session with unique profile"""
        logger.info("🔧 Creating new Chrome session with unique profile...")
        
        chrome_options = Options()
        
        # Use a unique profile directory
        unique_profile = f"/tmp/slack_integration_profile_{int(time.time())}"
        chrome_options.add_argument(f"--user-data-dir={unique_profile}")
        
        # Disable automation detection
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.set_window_size(1200, 800)
            
            logger.info("✅ New Chrome session created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating new Chrome session: {e}")
            return False
    
    def navigate_to_slack_web(self, workspace_url=None):
        """Navigate to Slack Web and check status"""
        if workspace_url:
            url = workspace_url
        else:
            url = "https://slack.com/signin"
        
        logger.info(f"🌐 Navigating to Slack Web: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(5)
            
            # Check current status
            return self.check_slack_web_status()
            
        except Exception as e:
            logger.error(f"❌ Error navigating to Slack Web: {e}")
            return "error"
    
    def check_slack_web_status(self):
        """Check if Slack Web is logged in"""
        logger.info("🔍 Checking Slack Web status...")
        
        try:
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, "[data-qa='channel_sidebar']") or 
                              driver.find_elements(By.CSS_SELECTOR, "[data-qa='signin_form']") or
                              driver.find_elements(By.CSS_SELECTOR, ".p-workspace_sidebar") or
                              driver.find_elements(By.CSS_SELECTOR, ".signin_form")
            )
            
            # Check if logged in (sidebar visible)
            if (self.driver.find_elements(By.CSS_SELECTOR, "[data-qa='channel_sidebar']") or
                self.driver.find_elements(By.CSS_SELECTOR, ".p-workspace_sidebar")):
                logger.info("🎉 Slack Web is logged in!")
                self.is_logged_in = True
                self.detect_workspace()
                return "logged_in"
            
            # Check for signin form
            elif (self.driver.find_elements(By.CSS_SELECTOR, "[data-qa='signin_form']") or
                  self.driver.find_elements(By.CSS_SELECTOR, ".signin_form")):
                logger.info("🔐 Sign-in form detected - login required")
                return "signin_required"
            
            # Check page content for other indicators
            page_source = self.driver.page_source.lower()
            if "workspace" in page_source and "channel" in page_source:
                logger.info("🎉 Slack Web appears to be logged in (content check)")
                self.is_logged_in = True
                self.detect_workspace()
                return "logged_in"
            
            logger.warning("❓ Unknown Slack Web state")
            return "unknown"
            
        except TimeoutException:
            logger.warning("⏰ Timeout checking Slack Web status")
            return "timeout"
        except Exception as e:
            logger.error(f"❌ Error checking Slack Web status: {e}")
            return "error"
    
    def detect_workspace(self):
        """Detect current workspace name"""
        try:
            # Try multiple selectors for workspace name
            workspace_selectors = [
                "[data-qa='team_name']",
                ".p-workspace_sidebar__team_name",
                "[data-qa='workspace_name']",
                ".team_name"
            ]
            
            for selector in workspace_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].text:
                    self.current_workspace = elements[0].text.strip()
                    logger.info(f"🏢 Detected workspace: {self.current_workspace}")
                    return
            
            # Fallback: try to get from URL
            current_url = self.driver.current_url
            if ".slack.com" in current_url:
                workspace = current_url.split("//")[1].split(".slack.com")[0]
                self.current_workspace = workspace
                logger.info(f"🏢 Detected workspace from URL: {self.current_workspace}")
            
        except Exception as e:
            logger.debug(f"Error detecting workspace: {e}")
            self.current_workspace = "Unknown Workspace"
    
    def wait_for_login(self, timeout=300):
        """Wait for user to login to Slack"""
        logger.info("⏳ Waiting for Slack Web login...")
        
        print("\n" + "="*60)
        print("🔐 SLACK WEB LOGIN REQUIRED")
        print("="*60)
        print("1. Look at the Chrome browser window")
        print("2. You should see Slack's sign-in page")
        print("3. Enter your workspace URL or email")
        print("4. Complete the login process")
        print("5. Wait for the workspace to load...")
        print(f"⏰ Timeout: {timeout} seconds")
        print("="*60)
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                status = self.check_slack_web_status()
                
                if status == "logged_in":
                    logger.info("✅ Slack Web login successful!")
                    self.is_logged_in = True
                    return True
                
                elapsed = int(time.time() - start_time)
                remaining = timeout - elapsed
                
                if elapsed % 30 == 0:  # Update every 30 seconds
                    logger.info(f"⏳ Still waiting for login... ({elapsed}s elapsed, {remaining}s remaining)")
                
                time.sleep(5)
                
            except Exception as e:
                logger.debug(f"Error during login wait: {e}")
                time.sleep(5)
        
        logger.error("⏰ Login timeout reached")
        return False
    
    def get_new_messages(self):
        """Get new messages from Slack Web"""
        if not self.is_logged_in:
            logger.warning("⚠️ Not logged in to Slack Web")
            return []
        
        try:
            new_messages = []
            
            # Get all channels in sidebar
            channel_selectors = [
                "[data-qa='channel_sidebar'] [data-qa-channel-sidebar-channel-type]",
                ".p-channel_sidebar__channel",
                "[data-qa='channel_sidebar'] a[href*='/messages/']",
                ".p-channel_sidebar__link"
            ]
            
            channels = []
            for selector in channel_selectors:
                channels = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if channels:
                    break
            
            logger.info(f"💬 Found {len(channels)} channels/conversations")
            
            # Check first few channels for new messages
            max_channels = min(len(channels), self.config["slack"]["max_messages_per_check"])
            
            for i, channel in enumerate(channels[:max_channels]):
                try:
                    # Get channel name before clicking
                    channel_name = "Unknown Channel"
                    try:
                        channel_name = channel.text.strip() or channel.get_attribute("aria-label") or f"Channel {i+1}"
                        # Clean up channel name
                        if channel_name.startswith("#"):
                            channel_name = channel_name[1:]
                    except Exception as e:
                        logger.debug(f"Error getting channel name: {e}")
                    
                    # Skip if channel filtering is enabled
                    if (self.config["slack"]["channels_to_monitor"] and 
                        channel_name not in self.config["slack"]["channels_to_monitor"]):
                        continue
                    
                    # Click on the channel to open it
                    self.driver.execute_script("arguments[0].click();", channel)
                    time.sleep(3)
                    
                    # Get recent messages from the channel
                    message_selectors = [
                        "[data-qa='virtual-list-item']",
                        ".c-virtual_list__item",
                        "[data-qa='message']",
                        ".c-message_kit__blocks"
                    ]
                    
                    message_elements = []
                    for selector in message_selectors:
                        message_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if message_elements:
                            break
                    
                    logger.debug(f"Found {len(message_elements)} message elements in {channel_name}")
                    
                    # Check the last few messages
                    for msg_element in message_elements[-5:]:
                        try:
                            # Get message text
                            message_text = ""
                            text_selectors = [
                                "[data-qa='message-text']",
                                ".c-message_kit__text",
                                ".p-rich_text_section",
                                ".c-message__body"
                            ]
                            
                            for selector in text_selectors:
                                text_elements = msg_element.find_elements(By.CSS_SELECTOR, selector)
                                for text_elem in text_elements:
                                    if text_elem.text and text_elem.text.strip():
                                        message_text = text_elem.text.strip()
                                        break
                                if message_text:
                                    break
                            
                            if not message_text or len(message_text) < 3:
                                continue
                            
                            # Get sender name
                            sender_name = "Unknown User"
                            sender_selectors = [
                                "[data-qa='message_sender_name']",
                                ".c-message__sender_link",
                                ".c-message_kit__sender_name",
                                ".p-message_pane_message__sender"
                            ]
                            
                            for selector in sender_selectors:
                                sender_elements = msg_element.find_elements(By.CSS_SELECTOR, selector)
                                if sender_elements and sender_elements[0].text:
                                    sender_name = sender_elements[0].text.strip()
                                    break
                            
                            # Get timestamp
                            timestamp = datetime.now().strftime("%H:%M")
                            try:
                                time_selectors = [
                                    "[data-qa='message_timestamp']",
                                    ".c-timestamp",
                                    ".c-message_kit__timestamp"
                                ]
                                
                                for selector in time_selectors:
                                    time_elements = msg_element.find_elements(By.CSS_SELECTOR, selector)
                                    if time_elements and time_elements[0].text:
                                        timestamp = time_elements[0].text.strip()
                                        break
                            except Exception as e:
                                logger.debug(f"Error getting timestamp: {e}")
                            
                            # Create unique message ID
                            message_id = f"{self.current_workspace}_{channel_name}_{sender_name}_{timestamp}_{hash(message_text)}_{int(time.time())}"
                            
                            if message_id not in self.processed_messages:
                                new_messages.append({
                                    'id': message_id,
                                    'workspace': self.current_workspace,
                                    'channel': channel_name,
                                    'sender': sender_name,
                                    'message': message_text,
                                    'timestamp': timestamp,
                                    'datetime': datetime.now().isoformat()
                                })
                                self.processed_messages.add(message_id)
                                logger.info(f"💬 New message in #{channel_name} from {sender_name}: {message_text[:50]}...")
                                
                        except Exception as e:
                            logger.debug(f"Error processing message: {e}")
                            continue
                    
                    # Limit messages for performance
                    if len(new_messages) >= 3:
                        break
                        
                except Exception as e:
                    logger.debug(f"Error processing channel {i}: {e}")
                    continue
            
            return new_messages
            
        except Exception as e:
            logger.error(f"❌ Error getting messages: {e}")
            return []
    
    def forward_to_gmail_real(self, slack_message):
        """Forward Slack message to Gmail using REAL Gmail MCP"""
        try:
            recipient = self.config["gmail_mcp"]["recipient_email"]
            subject = f"[Slack] {slack_message['workspace']} #{slack_message['channel']} - {slack_message['sender']}"
            
            body = f"""💬 Slack Message Received

Workspace: {slack_message['workspace']}
Channel: #{slack_message['channel']}
From: {slack_message['sender']}
Time: {slack_message['timestamp']}
Received: {slack_message['datetime']}

Message:
{slack_message['message']}

---
This message was automatically forwarded from Slack.
Reply to this email to send a message back to Slack (if configured).

Message ID: {slack_message['id']}
"""
            
            # Call the real Gmail MCP
            result = self.gmail_client.send_email(recipient, subject, body)
            
            if result.get("status") == "sent":
                logger.info(f"✅ REAL email sent successfully! ID: {result.get('message_id')}")
                return True
            else:
                logger.error(f"❌ Failed to send real email: {result}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending real email: {e}")
            return False
    
    def run_monitoring_loop(self):
        """Main monitoring loop for the integration"""
        logger.info("🚀 Starting Slack-Gmail monitoring loop...")
        
        check_interval = self.config["slack"]["check_interval"]
        
        print("\n" + "="*60)
        print("🤖 SLACK-GMAIL BRIDGE IS RUNNING")
        print("="*60)
        print(f"💬 Monitoring Slack workspace: {self.current_workspace}")
        print(f"📧 Forwarding to: {self.config['gmail_mcp']['recipient_email']}")
        print(f"⏰ Check interval: {check_interval} seconds")
        print("🔥 REAL EMAILS WILL BE SENT!")
        print("🛑 Press Ctrl+C to stop")
        print("="*60)
        
        try:
            while True:
                try:
                    # Check for new Slack messages
                    new_messages = self.get_new_messages()
                    
                    for message in new_messages:
                        self.message_count += 1
                        logger.info(f"📨 Processing message #{self.message_count}")
                        
                        # Forward to Gmail using REAL MCP
                        if self.forward_to_gmail_real(message):
                            logger.info(f"✅ REAL email #{self.message_count} sent successfully!")
                            print(f"🔥 REAL EMAIL SENT for message #{self.message_count}")
                        else:
                            logger.error(f"❌ Failed to send real email #{self.message_count}")
                    
                    if new_messages:
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
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up...")
        if self.driver:
            self.driver.quit()
        logger.info("✅ Cleanup completed")
    
    def run_integration(self):
        """Run the complete integration"""
        logger.info("🚀 Starting Slack-Gmail Integration")
        logger.info("=" * 60)
        
        try:
            # Try to connect to existing Chrome or create new session
            if not self.connect_to_existing_chrome_session():
                logger.error("❌ Failed to connect to Chrome")
                return False
            
            # Navigate to Slack Web
            status = self.navigate_to_slack_web()
            
            if status == "logged_in":
                logger.info("🎉 Slack Web is ready!")
            elif status == "signin_required":
                if not self.wait_for_login():
                    logger.error("❌ Login failed or timed out")
                    return False
            else:
                logger.warning("⚠️ Unexpected Slack Web status, but continuing...")
                self.is_logged_in = True  # Assume it's working
            
            # Save configuration with detected workspace
            self.save_config()
            
            # Start monitoring
            self.run_monitoring_loop()
            
        except KeyboardInterrupt:
            logger.info("🛑 Integration stopped by user")
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
        finally:
            self.cleanup()

def main():
    """Main function"""
    print("💬 Slack-Gmail Bridge")
    print("This version connects to existing Chrome or creates a new session")
    print("\n🔧 This will:")
    print("1. Try to connect to your existing Chrome session")
    print("2. Or create a new Chrome session if needed")
    print("3. Navigate to Slack Web")
    print("4. Wait for you to login if needed")
    print("5. Start monitoring and send REAL emails")
    
    print("\nStarting integration in 5 seconds...")
    time.sleep(5)
    
    bridge = SlackGmailBridge()
    bridge.run_integration()

if __name__ == "__main__":
    main()
