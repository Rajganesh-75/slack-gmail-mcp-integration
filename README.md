# Slack-Gmail Integration

Bridge between Slack and Gmail using MCP (Model Context Protocol).

## 📁 Project Structure

```
slack-integration/
├── 🐍 slack_gmail_bridge.py           # Main bridge application
├── 🐍 slack_desktop_gmail_bridge.py   # Desktop version with GUI integration
├── 🐍 slack_gmail_integration_real.py # Production-ready version
├── ⚙️ slack_config.json               # Slack API configuration
├── ⚙️ slack_desktop_config.json       # Desktop app specific configuration
├── 📦 slack_requirements.txt          # Python dependencies
├── 📂 tests/                          # Test files
├── 📂 config/                         # Configuration and setup
├── 📂 utilities/                      # Shared utilities
└── 📄 README.md                       # This file
```

## 🔧 Core Files

- **`slack_gmail_bridge.py`** - Main bridge application
- **`slack_desktop_gmail_bridge.py`** - Desktop version with GUI integration
- **`slack_gmail_integration_real.py`** - Production-ready version
- `slack_config.json` - Slack API configuration
- `slack_desktop_config.json` - Desktop app specific configuration
- `slack_requirements.txt` - Python dependencies

## 🚀 Quick Start

1. **Configure Slack API** credentials in `slack_config.json`
2. **Install dependencies**: `pip install -r slack_requirements.txt`
3. **Run main bridge**: `python slack_gmail_bridge.py`

## ✨ Features

- 💬 **Slack DM to Gmail forwarding** - Forward Slack direct messages to Gmail
- 📧 **Gmail to Slack reply capability** - Reply to Slack messages from Gmail
- ⚡ **Real-time message monitoring** - Live monitoring of Slack conversations
- 🖥️ **Desktop app integration** - Works with Slack desktop application
- 🔄 **Bidirectional messaging** - Two-way communication between platforms
- 🎯 **Production-ready implementation** - Robust error handling and logging

## 🧪 Testing

Test files are located in the `tests/` directory:
- `test_slack_dm_integration.py` - Basic Slack DM testing
- `test_slack_dm_real.py` - Real-world Slack testing
- `run_slack_dm_test.py` - Test runner

```bash
# Run tests
cd tests/
python test_slack_dm_integration.py
```

## ⚙️ Configuration

### Slack API Setup
Update `slack_config.json` with your Slack workspace details:
```json
{
  "slack_token": "xoxb-your-slack-bot-token",
  "channel_id": "your-channel-id",
  "app_token": "xapp-your-app-token"
}
```

### Desktop Integration
For desktop app integration, configure `slack_desktop_config.json`:
```json
{
  "desktop_integration": true,
  "notification_settings": {
    "enabled": true,
    "sound": false
  }
}
```

## 📦 Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r slack_requirements.txt
   ```
3. **Configure Slack API** credentials (see Configuration section)
4. **Set up Gmail MCP** integration (see config/ folder)

## 🔗 Dependencies

This integration relies on:
- **Slack API** (via slack-sdk)
- **Gmail MCP integration** (shared utility in config/)
- **Real-time message monitoring**
- **WebSocket connections** for live updates

## 🛠️ Development

### Project Structure
- `config/` - Shared configuration files and setup scripts
- `tests/` - Test files for Slack integration
- `utilities/` - Shared utility functions

### Adding Features
1. Modify the appropriate bridge file (`slack_gmail_bridge.py` for main features)
2. Add tests in the `tests/` directory
3. Update configuration files as needed
4. Update this README

## 🔧 Utilities

Located in `utilities/`:
- `check_permissions.py` - Permission checker for Slack API

## 📋 Configuration Files

Located in `config/`:
- `config.json` - Main configuration file
- `token.json` - Authentication tokens
- `requirements.txt` - Python dependencies
- `setup_integration.py` - Setup script

## 🚨 Important Notes

- **API Limits**: Respect Slack API rate limits and terms of service
- **MCP Dependency**: Requires Gmail MCP server to be running
- **Security**: Keep configuration files secure and private
- **Permissions**: Ensure proper Slack app permissions are configured

## 📞 Support

For issues:
1. Check logs in the bridge applications
2. Verify Slack API credentials and permissions
3. Test Slack API connection separately
4. Check Gmail MCP server status
5. Review configuration files for errors

## 🔐 Security

- Store API tokens securely
- Use environment variables for sensitive data
- Regularly rotate API tokens
- Monitor API usage and logs

---

**Note**: This integration uses official Slack APIs. Ensure compliance with Slack's terms of service and your organization's policies.
