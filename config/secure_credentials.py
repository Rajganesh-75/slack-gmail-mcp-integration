#!/usr/bin/env python3
"""
Secure Credentials Handler
Safely manages credentials without exposing them in the codebase
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SecureCredentials:
    """Secure credential management"""
    
    def __init__(self):
        """Initialize secure credentials handler"""
        self.credentials_path = None
        self.credentials = None
        
    def load_credentials(self, custom_path=None):
        """Load credentials from secure location"""
        
        # Priority order for credential locations
        credential_paths = [
            custom_path,  # User-specified path
            os.environ.get('GMAIL_CREDENTIALS_PATH'),  # Environment variable
            '/Users/rajganesh/Downloads/credentials.json',  # Your specified path
            os.path.expanduser('~/.config/gmail/credentials.json'),  # Standard location
            './config/secure/credentials.json',  # Local secure folder (not in git)
        ]
        
        for path in credential_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        self.credentials = json.load(f)
                    self.credentials_path = path
                    logger.info(f"✅ Credentials loaded from: {path}")
                    return True
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load credentials from {path}: {e}")
                    continue
        
        logger.error("❌ No valid credentials found in any location")
        return False
    
    def get_credentials(self):
        """Get loaded credentials"""
        return self.credentials
    
    def get_credentials_path(self):
        """Get path to credentials file"""
        return self.credentials_path
    
    def is_loaded(self):
        """Check if credentials are loaded"""
        return self.credentials is not None
    
    def setup_environment_variable(self):
        """Show how to set up environment variable"""
        print("🔐 To set up environment variable:")
        print(f"export GMAIL_CREDENTIALS_PATH='/Users/rajganesh/Downloads/credentials.json'")
        print("Add this to your ~/.bashrc or ~/.zshrc for permanent setup")

# Global instance
secure_creds = SecureCredentials()

def get_gmail_credentials():
    """Get Gmail credentials securely"""
    if not secure_creds.is_loaded():
        if not secure_creds.load_credentials():
            raise Exception("Gmail credentials not found or invalid")
    return secure_creds.get_credentials()

def test_credentials():
    """Test credential loading"""
    print("🧪 Testing secure credential loading...")
    
    if secure_creds.load_credentials():
        print(f"✅ Credentials loaded successfully")
        print(f"📁 Path: {secure_creds.get_credentials_path()}")
        
        creds = secure_creds.get_credentials()
        if 'type' in creds:
            print(f"🔑 Credential type: {creds['type']}")
        if 'client_id' in creds:
            client_id_preview = creds['client_id'][:20] + "..." if len(creds['client_id']) > 20 else creds['client_id']
            print(f"🆔 Client ID preview: {client_id_preview}")
        
        return True
    else:
        print("❌ Failed to load credentials")
        secure_creds.setup_environment_variable()
        return False

if __name__ == "__main__":
    test_credentials()
