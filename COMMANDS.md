# 🚀 Slack-Gmail Integration - Useful Commands

This document lists all the useful commands available in your Slack-Gmail integration project.

## 📧 **Email Integration Commands**

### **Get User Conversations**
```bash
# Get conversation with any user and send to email
python3 get_user_conversation.py <username> --send

# Examples:
python3 get_user_conversation.py alice --send          # Conversation with alice
python3 get_user_conversation.py bob --send       # Conversation with bob
python3 get_user_conversation.py alice --send           # Conversation with alice

# Get more messages:
python3 get_user_conversation.py alice -m 20 --send    # Get 20 messages
python3 get_user_conversation.py john -m 15 --send      # Get 15 messages

# Preview before sending:
python3 get_user_conversation.py alice                 # Just preview
python3 get_user_conversation.py john -m 10             # Preview 10 messages
```

### **Live Monitoring**
```bash
# Safe test mode (no real emails sent)
python3 secure_slack_gmail_bridge.py --test

# Live mode (sends real emails)
python3 secure_slack_gmail_bridge.py --live

# Alternative bridges:
python3 slack_gmail_bridge.py --test                    # Web automation version
python3 slack_desktop_gmail_bridge.py                   # Desktop app version
```

---

## 🧪 **Testing Commands**

### **Component Testing**
```bash
# Test secure Gmail integration
python3 test_secure_gmail.py

# Test real Slack message forwarding
python3 test_real_message.py

# Test Slack web access
python3 test_slack_access.py

# Complete integration test guide
python3 test_live_integration.py

# Test real Slack MCP integration
python3 test_real_slack_mcp.py
```

### **Send Specific Messages**
```bash
# Send real Slack message to email
python3 send_real_slack_email.py

# Send conversation to email
python3 send_conversation_email.py
```

---

## 🔧 **Setup and Configuration**

### **Initial Setup**
```bash
# Run setup script
python3 config/setup_integration.py

# Test secure credentials
python3 config/secure_credentials.py

# Install dependencies
pip install -r slack_requirements.txt
pip install -r config/requirements.txt
```

### **Configuration Files**
```bash
# Edit main Slack config
nano slack_config.json

# Edit desktop config
nano slack_desktop_config.json

# Edit general config
nano config/config.json
```

---

## 📱 **Slack MCP Commands (via Goose)**

### **User Information**
```bash
# Get user info
slack__get_user_info --inputs '[{"username": "alice"}]'

# Get your own info
slack__get_user_info --inputs '[{"username": "me"}]'
```

### **Channel Operations**
```bash
# List channels
slack__list_channels --channel_types "public_channel,private_channel,im" --limit 10

# Get channel messages
slack__get_channel_messages --channels '[{"channel_name": "engineering"}]' --messages_to_retrieve 5

# Get DM messages
slack__get_channel_messages --channels '[{"dm_username": "alice"}]' --messages_to_retrieve 10
```

### **Search Messages**
```bash
# Search messages
slack__search_messages --query_terms "jenkins" --count 10

# Search messages from specific user
slack__search_messages --filter '{"from_user_id_or_usernames": [{"username": "alice"}]}' --count 5
```

---

## 📧 **Gmail MCP Commands (via Goose)**

### **Email Operations**
```bash
# Send email
gmailcustom__send_email --to "your-email@example.com" --subject "Test" --body "Test message"

# List recent emails
gmailcustom__list_emails --count 10

# Read specific email
gmailcustom__read_email --message_id "your-message-id"

# Search emails
gmailcustom__search_emails --query "from:slack" --count 5
```

---

## 🔍 **Utility Commands**

### **File Operations**
```bash
# View project structure
ls -la
tree -I 'archive|__pycache__'

# Check Git status
git status

# View logs
tail -f *.log
```

### **Process Management**
```bash
# Run in background
nohup python3 secure_slack_gmail_bridge.py --live > integration.log 2>&1 &

# Check running processes
ps aux | grep python

# Kill process
pkill -f "slack_gmail_bridge"
```

---

## 🛠️ **Development Commands**

### **Code Quality**
```bash
# Check Python syntax
python3 -m py_compile *.py

# Format code
black *.py

# Check imports
python3 -c "import sys; print(sys.path)"
```

### **Debugging**
```bash
# Run with debug output
python3 -u secure_slack_gmail_bridge.py --test

# Check credentials
python3 -c "from config.secure_credentials import test_credentials; test_credentials()"

# Test MCP connections
python3 -c "import slack; import gmailcustom; print('MCP extensions loaded')"
```

---

## 📊 **Monitoring Commands**

### **Log Analysis**
```bash
# View recent logs
tail -n 50 integration.log

# Search logs for errors
grep -i "error" *.log

# Count processed messages
grep -c "Email sent" integration.log
```

### **System Status**
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check network connectivity
ping slack.com
ping gmail.com
```

---

## 🔐 **Security Commands**

### **Credential Management**
```bash
# Check credential location
ls -la ./credentials.json

# Verify .gitignore
cat .gitignore

# Check for exposed credentials
grep -r "credentials" --exclude-dir=.git .
```

### **Cleanup**
```bash
# Remove temporary files
rm -f credentials.json
rm -rf __pycache__

# Clean up logs
rm -f *.log

# Reset permissions
chmod 600 config/*.json
```

---

## 🚀 **Quick Start Commands**

### **Most Common Usage**
```bash
# 1. Get conversation with a user
python3 get_user_conversation.py <username> --send

# 2. Start live monitoring
python3 secure_slack_gmail_bridge.py --live

# 3. Test integration
python3 secure_slack_gmail_bridge.py --test

# 4. Send specific message
python3 send_real_slack_email.py
```

### **Emergency Commands**
```bash
# Stop all integration processes
pkill -f "slack_gmail"

# Check what's running
ps aux | grep python | grep slack

# Restart integration
python3 secure_slack_gmail_bridge.py --live &
```

---

## 📝 **Documentation Commands**

### **View Help**
```bash
# Get help for any script
python3 get_user_conversation.py --help
python3 secure_slack_gmail_bridge.py --help

# View this command list
cat COMMANDS.md

# View README
cat README.md
```

---

## 🎯 **Most Useful Commands Summary**

### **Daily Use:**
1. `python3 get_user_conversation.py <username> --send` - Get any user conversation
2. `python3 secure_slack_gmail_bridge.py --live` - Start live monitoring
3. `python3 secure_slack_gmail_bridge.py --test` - Safe testing

### **Setup:**
1. `python3 config/setup_integration.py` - Initial setup
2. `pip install -r slack_requirements.txt` - Install dependencies

### **Troubleshooting:**
1. `python3 test_secure_gmail.py` - Test Gmail connection
2. `python3 test_real_slack_mcp.py` - Test Slack connection
3. `tail -f integration.log` - Monitor logs

---

**💡 Pro Tip:** Bookmark this file for quick reference to all available commands!
