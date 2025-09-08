#!/usr/bin/env python3
"""
Slack Gmail Bridge - Real Integration with Gmail MCP
This version integrates with the actual gmailcustom extension
"""

import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SlackGmailBridgeReal:
    def __init__(self, config_path="slack_config.json"):
        """Initialize the Slack Gmail bridge with real Gmail integration"""
        self.driver = None
        self.is_logged_in = False
        self.processed_messages = set()
        self.config = self.load_config(config_path)
        self.message_count = 0
        self.current_workspace = None
        
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
                "check_interval": 15,
                "max_messages_per_check": 3,
                "profile_path": "/tmp/slack_chrome_profile",
                "workspaces": [],
                "channels_to_monitor": [],
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
    
    def connect_to_existing_chrome_session(self):
        """Connect to existing Chrome session using remote debugging"""
        logger.info("🔗 Connecting to existing Chrome session via remote debugging...")
        
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
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
            return self.connect_with_new_session()
    
    def connect_with_new_session(self):
        """Create new Chrome session with unique profile"""
        logger.info("🔧 Creating new Chrome session with unique profile...")
        
        chrome_options = Options()
        unique_profile = f"/tmp/slack_integration_profile_{int(time.time())}"
        chrome_options.add_argument(f"--user-data-dir={unique_profile}")
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
            return self.check_slack_web_status()
        except Exception as e:
            logger.error(f"❌ Error navigating to Slack Web: {e}")
            return "error"
    
    def check_slack_web_status(self):
        """Check if Slack Web is logged in"""
        logger.info("🔍 Checking Slack Web status...")
        
        try:
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, "[data-qa='channel_sidebar']") or 
                              driver.find_elements(By.CSS_SELECTOR, "[data-qa='signin_form']") or
                              driver.find_elements(By.CSS_SELECTOR, ".p-workspace_sidebar") or
                              driver.find_elements(By.CSS_SELECTOR, ".signin_form")
            )
            
            if (self.driver.find_elements(By.CSS_SELECTOR, "[data-qa='channel_sidebar']") or
                self.driver.find_elements(By.CSS_SELECTOR, ".p-workspace_sidebar")):
                logger.info("🎉 Slack Web is logged in!")
                self.is_logged_in = True
                self.detect_workspace()
                return "logged_in"
            
            elif (self.driver.find_elements(By.CSS_SELECTOR, "[data-qa='signin_form']") or
                  self.driver.find_elements(By.CSS_SELECTOR, ".signin_form")):
                logger.info("🔐 Sign-in form detected - login required")
                return "signin_required"
            
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
                
                if elapsed % 30 == 0:
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
            
            max_channels = min(len(channels), self.config["slack"]["max_messages_per_check"])
            
            for i, channel in enumerate(channels[:max_channels]):
                try:
                    channel_name = "Unknown Channel"
                    try:
                        channel_name = channel.text.strip() or channel.get_attribute("aria-label") or f"Channel {i+1}"
                        if channel_name.startswith("#"):
                            channel_name = channel_name[1:]
                    except Exception as e:
                        logger.debug(f"Error getting channel name: {e}")
                    
                    if (self.config["slack"]["channels_to_monitor"] and 
                        channel_name not in self.config["slack"]["channels_to_monitor"]):
                        continue
                    
                    self.driver.execute_script("arguments[0].click();", channel)
                    time.sleep(3)
                    
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
                    
                    for msg_element in message_elements[-3:]:
                        try:
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
                    
                    if len(new_messages) >= 2:
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
            if not self.gmail_send_function:
                logger.error("❌ Gmail send function not set!")
                return False
                
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
        logger.info("🔍 Running single message check...")
        
        try:
            new_messages = self.get_new_messages()
            
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
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up...")
        if self.driver:
            self.driver.quit()
        logger.info("✅ Cleanup completed")
    
    def setup_connection(self):
        """Setup Chrome connection and navigate to Slack"""
        logger.info("🚀 Setting up Slack-Gmail Integration")
        
        try:
            if not self.connect_to_existing_chrome_session():
                logger.error("❌ Failed to connect to Chrome")
                return False
            
            status = self.navigate_to_slack_web()
            
            if status == "logged_in":
                logger.info("🎉 Slack Web is ready!")
                return True
            elif status == "signin_required":
                if not self.wait_for_login():
                    logger.error("❌ Login failed or timed out")
                    return False
                return True
            else:
                logger.warning("⚠️ Unexpected Slack Web status, but continuing...")
                self.is_logged_in = True
                return True
            
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return False

# Global instance for use by Goose
slack_bridge = None

def initialize_slack_bridge():
    """Initialize the Slack bridge for use by Goose"""
    global slack_bridge
    if slack_bridge is None:
        slack_bridge = SlackGmailBridgeReal()
    return slack_bridge

def setup_slack_connection():
    """Setup Slack connection"""
    bridge = initialize_slack_bridge()
    return bridge.setup_connection()

def check_slack_messages(gmail_send_function):
    """Check for new Slack messages and forward them"""
    bridge = initialize_slack_bridge()
    bridge.set_gmail_function(gmail_send_function)
    return bridge.run_single_check()

def cleanup_slack_bridge():
    """Cleanup the Slack bridge"""
    global slack_bridge
    if slack_bridge:
        slack_bridge.cleanup()
        slack_bridge = None

if __name__ == "__main__":
    print("💬 Slack-Gmail Bridge Real Integration")
    print("This module is designed to be imported and used by Goose")
    print("Use the functions: initialize_slack_bridge, setup_slack_connection, check_slack_messages")
