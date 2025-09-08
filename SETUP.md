# Slack-Gmail MCP Bridge - Setup Guide

This guide will walk you through setting up the Slack-Gmail MCP Bridge from scratch.

## 🚀 Quick Start (Recommended)

**New users should start here:**

```bash
# Clone the repository
git clone <repository-url>
cd slack-integration

# Install dependencies
pip install -r requirements.txt

# Run the complete setup wizard
python3 first_run_setup.py
```

The setup wizard will guide you through everything automatically. Skip to [Step 7](#step-7-start-using) if you use this method.

## 📋 Prerequisites

Before starting, ensure you have:

1. **Goose AI** installed and running
2. **Python 3.7+** installed
3. **Access to a Slack workspace**
4. **Gmail account** for receiving notifications

## Step 1: Install Goose MCP Extensions

The project requires two specific MCP extensions:

### Enable Required Extensions

1. Open Goose AI
2. Go to **Settings** → **Extensions**
3. Search for and enable:
   - `slack` - Slack MCP extension for message access
   - `gmailcustom` - Gmail Custom MCP for email sending

4. Restart Goose if prompted

### Verify Extensions

Run this in Goose to verify extensions are available:
```
List available MCP extensions
```

You should see both `slack` and `gmailcustom` in the list.

## Step 2: Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd slack-integration

# Install Python dependencies
pip install -r requirements.txt
```

## Step 3: Gmail API Setup

### Get Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Gmail API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

4. Create credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Desktop application"
   - Download the JSON file

5. **Important**: Rename the downloaded file to `credentials.json` and place it in the project root directory

### Test Gmail API Access

The first time you run the application, you'll be prompted to authorize Gmail access through your browser.

## Step 4: Configure the Application

### Option A: Interactive Setup (Recommended)

```bash
python3 setup_config.py
```

### Option B: Manual Configuration

Create `config/user_config.json` with your settings:

```json
{
  "user": {
    "email_address": "your.email@example.com",
    "slack_username": "your_username",
    "slack_workspace": "your-workspace"
  },
  "email": {
    "preferences": {
      "send_dm_summaries": true,
      "send_channel_mentions": true,
      "send_keyword_alerts": true
    },
    "keywords": ["urgent", "meeting", "deadline"]
  },
  "slack": {
    "monitor_dms": true,
    "monitor_mentions": true,
    "channels_to_monitor": ["general", "team-updates"]
  },
  "credentials": {
    "gmail_credentials_path": "./credentials.json"
  }
}
```

## Step 5: Validate Setup

### Check Requirements

```bash
# Comprehensive requirements check
python3 check_requirements.py
```

This validates:
- File structure
- Configuration files
- Gmail credentials
- Python dependencies
- Goose environment
- MCP extensions

### Test Configuration

```bash
python3 test_configuration.py
```

## Step 6: Test the Integration

### Test Slack-Gmail Bridge

```bash
# Run in test mode (no emails sent)
python3 slack_gmail_mcp_bridge.py --test
```

This will:
- Test Slack MCP connection
- Test Gmail MCP connection
- Process sample messages
- Show what emails would be sent

### Test Conversation Retrieval

```bash
# Preview a conversation (replace 'username' with actual Slack username)
python3 get_user_conversation.py username -m 10

# Send a test conversation to email
python3 get_user_conversation.py username -m 10 --send
```

## Step 7: Start Using

Once everything is tested and working:

### Start Live Monitoring

```bash
# Start live monitoring (sends real emails)
python3 slack_gmail_mcp_bridge.py --live
```

### Get Conversations

```bash
# Get and email a specific conversation
python3 get_user_conversation.py username -m 15 --send
```

## 🔧 Troubleshooting

### First-Time Setup Issues

If you encounter any issues, run the diagnostic tool:

```bash
python3 check_requirements.py
```

This will identify and help fix common problems.

### Common Issues

1. **"Setup Required" Error**
   - Run `python3 first_run_setup.py`
   - This creates all necessary configuration files

2. **"MCP extension not found"**
   - Ensure Goose is running
   - Verify extensions are enabled in Goose settings
   - Restart Goose after enabling extensions

3. **Gmail API authentication fails**
   - Check `credentials.json` is in the project root
   - Ensure Gmail API is enabled in Google Cloud Console
   - Try deleting any existing token files and re-authenticating

4. **Configuration file not found**
   - Run `python3 first_run_setup.py` or `python3 setup_config.py`
   - Check that `config/user_config.json` exists

5. **Slack connection issues**
   - Verify you have access to the Slack workspace
   - Check that the Slack MCP extension is properly enabled
   - Ensure your Slack username is correct in the configuration

### Getting Help

If you encounter issues:

1. **Run diagnostics**: `python3 check_requirements.py`
2. **Check the logs**: Look at console output for specific error messages
3. **Verify prerequisites**: Ensure all requirements are met
4. **Re-run setup**: Use `python3 first_run_setup.py` to start over

## 📁 Configuration Details

### User Configuration File

The `config/user_config.json` file contains all your personal settings:

```json
{
  "user": {
    "email_address": "your.email@example.com",
    "slack_username": "your_username",
    "slack_workspace": "your-workspace"
  },
  "email": {
    "preferences": {
      "send_dm_summaries": true,
      "send_channel_mentions": true,
      "send_keyword_alerts": true,
      "include_message_context": true
    },
    "keywords": ["urgent", "meeting", "deadline", "help"]
  },
  "slack": {
    "monitor_dms": true,
    "monitor_mentions": true,
    "channels_to_monitor": ["general", "team-updates", "announcements"]
  },
  "credentials": {
    "gmail_credentials_path": "./credentials.json"
  },
  "setup": {
    "completed": true,
    "version": "1.0",
    "setup_date": "2024-01-01T00:00:00"
  }
}
```

### Customizing Monitoring

You can customize what gets monitored by editing the configuration:

- **DM Monitoring**: Set `monitor_dms` to `true/false`
- **Mention Monitoring**: Set `monitor_mentions` to `true/false`
- **Specific Channels**: Add channel names to `channels_to_monitor`
- **Keywords**: Add words to the `keywords` array
- **Email Preferences**: Toggle different types of notifications

## 🔐 Security Notes

- **Never commit `credentials.json`** to version control
- **Keep your configuration file private** (it's already in `.gitignore`)
- **Gmail credentials are stored locally** and not transmitted anywhere except to Google's APIs
- **Slack access is handled through Goose MCP** extensions
- **No personal information is hardcoded** in the project files

## 🚀 Advanced Configuration

### Custom Filtering

You can create more sophisticated filtering by modifying the configuration:

```json
{
  "email": {
    "keywords": ["urgent", "ASAP", "deadline", "meeting"],
    "preferences": {
      "send_dm_summaries": true,
      "send_channel_mentions": true,
      "send_keyword_alerts": true
    }
  }
}
```

### Channel-Specific Settings

Monitor specific channels with different settings:

```json
{
  "slack": {
    "channels_to_monitor": ["general", "team-updates", "alerts"],
    "monitor_dms": true,
    "monitor_mentions": true
  }
}
```

## 📋 Available Commands Reference

| Command | Purpose |
|---------|---------|
| `python3 first_run_setup.py` | Complete setup for new users |
| `python3 check_requirements.py` | Validate all requirements |
| `python3 setup_config.py` | Interactive configuration |
| `python3 test_configuration.py` | Test configuration |
| `python3 slack_gmail_mcp_bridge.py --test` | Test monitoring |
| `python3 slack_gmail_mcp_bridge.py --live` | Live monitoring |
| `python3 get_user_conversation.py <user> --send` | Get conversation |

## 🎉 Next Steps

Once setup is complete:

1. **Start with test mode** to ensure everything works
2. **Monitor the logs** when running in live mode
3. **Adjust configuration** based on your needs
4. **Set up monitoring** for important channels and keywords

---

**🚀 Setup Complete!** You should now have a fully functional Slack-Gmail MCP Bridge. 

**For new users**: Always start with `python3 first_run_setup.py` for the best experience!
