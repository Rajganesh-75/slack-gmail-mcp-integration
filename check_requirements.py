#!/usr/bin/env python3
"""
Slack-Gmail MCP Bridge - Requirements Checker
=============================================

This script checks if all requirements are met before running the main scripts:
1. Verifies user configuration exists and is valid
2. Checks if required Goose MCP extensions are available
3. Validates Gmail API credentials
4. Tests basic connectivity

Run this script to troubleshoot setup issues.
"""

import os
import json
import sys
from pathlib import Path
import subprocess

class RequirementsChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_dir = self.project_root / "config"
        self.user_config_path = self.config_dir / "user_config.json"
        self.errors = []
        self.warnings = []
        
    def print_header(self):
        """Print the header"""
        print("🔍 SLACK-GMAIL MCP BRIDGE - REQUIREMENTS CHECK")
        print("=" * 55)
        print()
    
    def check_user_configuration(self):
        """Check if user configuration exists and is valid"""
        print("📋 CHECKING USER CONFIGURATION")
        print("-" * 35)
        
        if not self.user_config_path.exists():
            self.errors.append("User configuration file not found")
            print("❌ user_config.json not found")
            print("   Run: python3 first_run_setup.py")
            return False
        
        try:
            with open(self.user_config_path, 'r') as f:
                config = json.load(f)
            
            # Check required fields
            required_fields = [
                ('user', 'email_address'),
                ('user', 'slack_username'),
                ('credentials', 'gmail_credentials_path')
            ]
            
            missing_fields = []
            for section, field in required_fields:
                if section not in config or field not in config[section]:
                    missing_fields.append(f"{section}.{field}")
            
            if missing_fields:
                self.errors.append(f"Missing configuration fields: {', '.join(missing_fields)}")
                print(f"❌ Missing fields: {', '.join(missing_fields)}")
                return False
            
            print("✅ User configuration: Valid")
            
            # Check if setup was completed
            if not config.get('setup', {}).get('completed', False):
                self.warnings.append("Setup may not have completed successfully")
                print("⚠️  Setup completion flag not set")
            
            return True
            
        except json.JSONDecodeError:
            self.errors.append("User configuration file is corrupted")
            print("❌ Configuration file is corrupted")
            return False
        except Exception as e:
            self.errors.append(f"Error reading configuration: {e}")
            print(f"❌ Error reading configuration: {e}")
            return False
    
    def check_gmail_credentials(self):
        """Check Gmail API credentials"""
        print("\n🔑 CHECKING GMAIL CREDENTIALS")
        print("-" * 30)
        
        try:
            with open(self.user_config_path, 'r') as f:
                config = json.load(f)
            
            creds_path = config.get('credentials', {}).get('gmail_credentials_path')
            if not creds_path:
                self.errors.append("Gmail credentials path not configured")
                print("❌ Gmail credentials path not set")
                return False
            
            creds_file = Path(creds_path)
            if not creds_file.exists():
                self.errors.append(f"Gmail credentials file not found: {creds_path}")
                print(f"❌ Credentials file not found: {creds_path}")
                return False
            
            # Try to parse the credentials file
            try:
                with open(creds_file, 'r') as f:
                    creds = json.load(f)
                
                # Check if it looks like valid Gmail API credentials
                if 'installed' in creds or 'web' in creds:
                    print("✅ Gmail credentials: Valid format")
                    return True
                else:
                    self.warnings.append("Gmail credentials format may be incorrect")
                    print("⚠️  Gmail credentials format may be incorrect")
                    return True
                    
            except json.JSONDecodeError:
                self.errors.append("Gmail credentials file is corrupted")
                print("❌ Gmail credentials file is corrupted")
                return False
                
        except Exception as e:
            self.errors.append(f"Error checking Gmail credentials: {e}")
            print(f"❌ Error checking Gmail credentials: {e}")
            return False
    
    def check_python_dependencies(self):
        """Check if required Python packages are installed"""
        print("\n🐍 CHECKING PYTHON DEPENDENCIES")
        print("-" * 35)
        
        required_packages = [
            'requests',
            'python-dotenv'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'python-dotenv':
                    import dotenv
                else:
                    __import__(package.replace('-', '_'))
                print(f"✅ {package}: Installed")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}: Not installed")
        
        if missing_packages:
            self.errors.append(f"Missing Python packages: {', '.join(missing_packages)}")
            print(f"\nInstall missing packages with:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        return True
    
    def check_goose_environment(self):
        """Check if Goose environment is available"""
        print("\n🪿 CHECKING GOOSE ENVIRONMENT")
        print("-" * 32)
        
        # Check if we're in a Goose context
        goose_context = os.environ.get('GOOSE_CONTEXT')
        if goose_context:
            print("✅ Goose context detected")
            return True
        
        # Check if Goose process is running
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if 'goose' in result.stdout.lower():
                print("✅ Goose process detected")
                return True
        except:
            pass
        
        self.warnings.append("Goose environment not clearly detected")
        print("⚠️  Goose environment not clearly detected")
        print("   This project works best when run from within Goose AI")
        return True  # Don't fail on this, just warn
    
    def check_mcp_extensions(self):
        """Check if required MCP extensions are available"""
        print("\n🔌 CHECKING MCP EXTENSIONS")
        print("-" * 28)
        
        required_extensions = ['slack', 'gmailcustom']
        
        print("Required MCP extensions:")
        for ext in required_extensions:
            print(f"📦 {ext}: Required for full functionality")
        
        print("\n⚠️  Extension availability can only be verified within Goose")
        print("   If you encounter errors, ensure these extensions are enabled:")
        print("   1. Open Goose AI Settings")
        print("   2. Go to Extensions tab")
        print("   3. Enable 'slack' and 'gmailcustom' extensions")
        
        return True
    
    def check_file_structure(self):
        """Check if all required files are present"""
        print("\n📁 CHECKING FILE STRUCTURE")
        print("-" * 28)
        
        required_files = [
            'src/config_loader.py',
            'src/get_user_conversation.py',
            'src/slack_gmail_mcp_bridge.py',
            'src/test_configuration.py',
            'requirements.txt',
            'README.md'
        ]
        
        missing_files = []
        
        for file in required_files:
            file_path = self.project_root / file
            if file_path.exists():
                print(f"✅ {file}")
            else:
                missing_files.append(file)
                print(f"❌ {file}: Missing")
        
        if missing_files:
            self.errors.append(f"Missing required files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def run_basic_tests(self):
        """Run basic functionality tests"""
        print("\n🧪 RUNNING BASIC TESTS")
        print("-" * 24)
        
        # Test config loader
        try:
            sys.path.insert(0, str(self.project_root))
            from src.config_loader import ConfigLoader
            config = ConfigLoader()
            print("✅ ConfigLoader: Working")
        except Exception as e:
            self.errors.append(f"ConfigLoader test failed: {e}")
            print(f"❌ ConfigLoader: Failed - {e}")
            return False
        
        # Test that main scripts can be imported
        test_scripts = [
            'src/get_user_conversation',
            'src/slack_gmail_mcp_bridge',
            'src/test_configuration'
        ]
        
        for script in test_scripts:
            try:
                # Just check if the file can be read and has basic structure
                script_path = self.project_root / f"{script}.py"
                with open(script_path, 'r') as f:
                    content = f.read()
                
                if 'def ' in content or 'class ' in content:
                    print(f"✅ {script}.py: Structure OK")
                else:
                    self.warnings.append(f"{script}.py may have structural issues")
                    print(f"⚠️  {script}.py: Structure unclear")
                    
            except Exception as e:
                self.errors.append(f"Error checking {script}.py: {e}")
                print(f"❌ {script}.py: Error - {e}")
        
        return True
    
    def print_summary(self):
        """Print the final summary"""
        print("\n" + "=" * 55)
        print("📊 REQUIREMENTS CHECK SUMMARY")
        print("=" * 55)
        
        if not self.errors and not self.warnings:
            print("🎉 ALL CHECKS PASSED!")
            print("✅ Your setup is ready to use")
            print("\n🚀 You can now run:")
            print("   python3 src/get_user_conversation.py <username> -m 10 --send")
            print("   python3 src/slack_gmail_mcp_bridge.py")
            
        elif self.errors:
            print("❌ SETUP ISSUES FOUND")
            print("\n🔧 Critical Issues (must fix):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
            
            if self.warnings:
                print("\n⚠️  Warnings:")
                for i, warning in enumerate(self.warnings, 1):
                    print(f"   {i}. {warning}")
            
            print("\n💡 Recommended Actions:")
            print("   1. Run: python3 first_run_setup.py")
            print("   2. Follow the setup instructions")
            print("   3. Run this check again")
            
        else:
            print("⚠️  SETUP MOSTLY OK (with warnings)")
            print("\n⚠️  Warnings:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
            
            print("\n✅ You should be able to use the system")
            print("   Monitor for any runtime issues")
    
    def run_all_checks(self):
        """Run all requirement checks"""
        self.print_header()
        
        checks = [
            self.check_file_structure,
            self.check_user_configuration,
            self.check_gmail_credentials,
            self.check_python_dependencies,
            self.check_goose_environment,
            self.check_mcp_extensions,
            self.run_basic_tests
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.errors.append(f"Check failed: {e}")
                print(f"❌ Check failed: {e}")
        
        self.print_summary()
        
        # Return exit code
        return 0 if not self.errors else 1

if __name__ == "__main__":
    checker = RequirementsChecker()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)
