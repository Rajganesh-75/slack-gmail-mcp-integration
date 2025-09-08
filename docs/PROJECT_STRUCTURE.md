# Project Structure

This document explains the organization of the Slack-Gmail MCP Bridge project.

## 📁 Directory Structure

```
slack-integration/
├── README.md                    # Project overview and quick start
├── SETUP.md                     # Detailed setup instructions
├── COMMANDS.md                  # Available commands reference
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── first_run_setup.py           # 🆕 Complete setup wizard for new users
├── check_requirements.py        # 🆕 Requirements validation and diagnostics
├── src/                         # 📦 Source code directory
│   ├── slack_gmail_mcp_bridge.py   # Main monitoring bridge
│   ├── get_user_conversation.py    # Conversation retrieval tool
│   ├── config_loader.py            # Configuration management
│   ├── setup_config.py             # Interactive configuration
│   └── test_configuration.py       # Configuration testing
├── config/                      # 🔧 Configuration files
│   └── user_config.json            # User-specific settings (created by setup)
├── docs/                        # 📚 Documentation
│   └── PROJECT_STRUCTURE.md        # This file
├── backup/                      # 🗂️ Old files (not needed for operation)
└── credentials.json             # 🔑 Gmail API credentials (user provides)
```

## 🚀 Main Entry Points

### For New Users
- **`first_run_setup.py`** - Complete setup wizard that guides through everything
- **`check_requirements.py`** - Validates setup and diagnoses issues

### For Daily Use
- **`src/get_user_conversation.py`** - Get and email specific Slack conversations
- **`src/slack_gmail_mcp_bridge.py`** - Main monitoring bridge

### For Configuration
- **`src/setup_config.py`** - Interactive configuration setup
- **`src/test_configuration.py`** - Test and validate configuration

## 📋 File Descriptions

### Root Level Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, features, and quick start guide |
| `SETUP.md` | Detailed setup instructions for all skill levels |
| `COMMANDS.md` | Complete reference of available commands |
| `LICENSE` | MIT License for open source distribution |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Protects sensitive files from being committed |

### Setup and Validation

| File | Purpose |
|------|---------|
| `first_run_setup.py` | **NEW**: Complete onboarding experience for new users |
| `check_requirements.py` | **NEW**: Comprehensive validation and troubleshooting |

### Source Code (`src/`)

| File | Purpose |
|------|---------|
| `slack_gmail_mcp_bridge.py` | Main application - monitors Slack and sends emails |
| `get_user_conversation.py` | Tool to retrieve specific conversations |
| `config_loader.py` | Handles loading and managing user configuration |
| `setup_config.py` | Interactive configuration setup |
| `test_configuration.py` | Tests and validates configuration |

### Configuration (`config/`)

| File | Purpose |
|------|---------|
| `user_config.json` | User-specific settings (email, Slack, preferences) |

### Documentation (`docs/`)

| File | Purpose |
|------|---------|
| `PROJECT_STRUCTURE.md` | This file - explains project organization |

## 🔧 Configuration Files

### User Configuration (`config/user_config.json`)
Contains all user-specific settings:
- Email address for notifications
- Slack username and workspace
- Monitoring preferences
- Keywords and filters
- Gmail API credentials path

### Environment Files
- `credentials.json` - Gmail API credentials (user provides)
- No hardcoded personal information anywhere

## 🗂️ Backup Directory

The `backup/` directory contains old files from previous versions:
- Legacy scripts and configurations
- Multiple versions of similar functionality
- Test files from development

These files are not needed for operation and are kept for reference only.

## 🚀 Running the Project

### First Time Setup
```bash
python3 first_run_setup.py      # Complete guided setup
python3 check_requirements.py   # Validate everything is working
```

### Daily Usage
```bash
python3 src/get_user_conversation.py username --send
python3 src/slack_gmail_mcp_bridge.py --test
python3 src/slack_gmail_mcp_bridge.py --live
```

### Configuration Management
```bash
python3 src/setup_config.py         # Interactive configuration
python3 src/test_configuration.py   # Test configuration
```

## 📦 Import Structure

The project uses relative imports from the `src/` directory:
- Main scripts import from `src.config_loader`
- Path handling ensures compatibility
- Backward compatibility with old configurations

## 🔐 Security Considerations

- **No hardcoded personal information** in any files
- **Gmail credentials** stored locally, never committed
- **User configuration** protected by `.gitignore`
- **Secure credential loading** with multiple fallback locations

## 🎯 Open Source Ready

The project structure is designed for open source distribution:
- Clean separation of code and configuration
- No personal information embedded
- Complete setup experience for new users
- Professional documentation and organization

---

This structure provides a clean, professional, and maintainable codebase that's ready for open source distribution while being easy for new users to understand and use.
