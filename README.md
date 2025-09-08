# Slack-Gmail MCP Bridge

A powerful integration tool that bridges Slack conversations to Gmail using Goose MCP (Model Context Protocol) extensions. Monitor your Slack workspace and receive important conversations directly in your email inbox.

## 🚀 Features

- **Real-time Slack Monitoring**: Monitor DMs, channel mentions, and specific channels
- **Email Notifications**: Receive formatted Slack conversations via Gmail
- **MCP Integration**: Uses Goose MCP extensions for seamless Slack and Gmail integration
- **Configurable Filtering**: Set up custom keywords, channels, and notification preferences
- **Conversation Retrieval**: Get specific conversations and send them to email on demand
- **Secure Credentials**: Safe handling of Gmail API credentials and Slack tokens
- **Open Source Ready**: No hardcoded personal information, fully configurable

## 🛠️ Requirements

- **Goose AI** with MCP extensions enabled
- **Python 3.7+**
- **Gmail API credentials**
- **Slack workspace access**

### Required Goose MCP Extensions
- `slack` - For Slack integration
- `gmailcustom` - For Gmail integration

## 🚀 Quick Start

### 1. First Time Setup

```bash
# Clone the repository
git clone <repository-url>
cd slack-integration

# Install dependencies
pip install -r requirements.txt

# Run the interactive setup (guides you through everything)
python3 first_run_setup.py
```

The setup script will guide you through:
- ✅ Checking Goose environment and extensions
- ✅ Configuring your email settings
- ✅ Setting up Slack workspace access
- ✅ Gmail API credentials setup
- ✅ Testing the complete integration

### 2. Verify Setup

```bash
# Check if everything is configured correctly
python3 check_requirements.py
```

### 3. Start Using

```bash
# Get a conversation and send to email
python3 get_user_conversation.py username -m 15 --send

# Start monitoring (test mode first)
python3 slack_gmail_mcp_bridge.py --test
```

## 📦 Manual Installation (Alternative)

If you prefer manual setup:

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure manually**:
   ```bash
   python3 setup_config.py
   ```

3. **Set up Gmail API**:
   - Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
   - Save as `credentials.json` in project root

## ⚙️ Configuration

The project uses `config/user_config.json` for all user settings:

```json
{
  "user": {
    "email_address": "your.email@example.com",
    "slack_username": "your_slack_username",
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
  }
}
```

## 🚀 Usage

### Start Monitoring
```bash
# Test mode (safe, no emails sent)
python3 slack_gmail_mcp_bridge.py --test

# Live mode (sends real emails)
python3 slack_gmail_mcp_bridge.py --live
```

### Get Specific Conversations
```bash
# Preview conversation
python3 get_user_conversation.py username -m 15

# Send conversation to email
python3 get_user_conversation.py username -m 15 --send
```

### Validate Setup
```bash
# Check requirements and configuration
python3 check_requirements.py

# Test specific configuration
python3 test_configuration.py
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `python3 first_run_setup.py` | **NEW**: Complete setup for new users |
| `python3 check_requirements.py` | **NEW**: Validate all requirements |
| `python3 slack_gmail_mcp_bridge.py --test` | Run monitoring in test mode |
| `python3 slack_gmail_mcp_bridge.py --live` | Run monitoring with real emails |
| `python3 get_user_conversation.py <user> --send` | Get and email a conversation |
| `python3 setup_config.py` | Interactive configuration setup |
| `python3 test_configuration.py` | Validate configuration |

## 🔧 Troubleshooting

### First-Time Users

If you're new to the project, always start with:
```bash
python3 first_run_setup.py
```

### Common Issues

1. **"Setup Required" Error**
   - Run `python3 first_run_setup.py`
   - This creates the necessary configuration files

2. **MCP Extensions Not Found**
   - Ensure Goose is running with `slack` and `gmailcustom` extensions enabled
   - Check Goose settings → Extensions

3. **Gmail API Errors**
   - Verify `credentials.json` is valid and in the project root
   - Check Gmail API is enabled in Google Cloud Console

4. **Configuration Issues**
   - Run `python3 check_requirements.py` for comprehensive diagnosis
   - Re-run setup if needed

### Getting Help

- Run `python3 check_requirements.py` for detailed diagnostics
- Check the `SETUP.md` file for detailed setup instructions
- Review `COMMANDS.md` for all available commands

## 📁 Project Structure

```
slack-integration/
├── first_run_setup.py           # 🆕 Complete setup for new users
├── check_requirements.py        # 🆕 Requirements validator
├── slack_gmail_mcp_bridge.py    # Main monitoring script
├── get_user_conversation.py     # Conversation retrieval tool
├── setup_config.py              # Interactive setup
├── test_configuration.py        # Configuration validator
├── config_loader.py             # Configuration management
├── config/
│   ├── user_config.json         # User-specific settings
│   └── config.json              # General configuration
├── credentials.json             # Gmail API credentials (not in repo)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── SETUP.md                     # Detailed setup guide
├── COMMANDS.md                  # Command reference
└── LICENSE                      # MIT License
```

## 🔐 Security & Privacy

- **No hardcoded personal information** - Everything is configurable
- **Gmail API credentials** stored locally, never committed to repository
- **User configuration** is gitignored to protect personal settings
- **Secure credential loading** with multiple fallback locations
- **Open source ready** - Safe to share and contribute to

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes (ensure no personal info is hardcoded)
4. Test with `python3 check_requirements.py`
5. Submit a pull request

## 🆕 What's New in Open Source Version

- ✅ **Complete first-run setup experience**
- ✅ **No hardcoded personal information**
- ✅ **Interactive configuration wizard**
- ✅ **Requirements validation system**
- ✅ **Better error messages and guidance**
- ✅ **Comprehensive documentation**
- ✅ **MIT License for open source use**

## 📞 Support

For issues and questions:
1. Run `python3 check_requirements.py` for diagnostics
2. Check the documentation files
3. Ensure proper Goose MCP setup
4. Review troubleshooting section

---

**🚀 Ready to get started?** Run `python3 first_run_setup.py` and follow the interactive guide!
