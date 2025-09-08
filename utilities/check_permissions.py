#!/usr/bin/env python3
"""
Check Accessibility Permissions Status
"""

import subprocess
import os

def test_permission_level():
    """Test different levels of Accessibility permissions"""
    
    print("🔧 Accessibility Permission Diagnostic")
    print("="*60)
    
    # Test 1: Basic System Events access
    print("\n1. Testing Basic System Events Access...")
    script1 = '''
    tell application "System Events"
        try
            set processCount to count of application processes
            return "SUCCESS: " & processCount & " processes found"
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    result1 = run_applescript(script1)
    print(f"   Result: {result1}")
    
    # Test 2: Slack process detection
    print("\n2. Testing Slack Process Detection...")
    script2 = '''
    tell application "System Events"
        try
            set slackExists to exists (process "Slack")
            return "SUCCESS: Slack process exists = " & slackExists
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    result2 = run_applescript(script2)
    print(f"   Result: {result2}")
    
    # Test 3: Slack UI access
    print("\n3. Testing Slack UI Access...")
    script3 = '''
    tell application "System Events"
        try
            tell process "Slack"
                set windowCount to count of windows
                return "SUCCESS: " & windowCount & " Slack windows found"
            end tell
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    result3 = run_applescript(script3)
    print(f"   Result: {result3}")
    
    # Test 4: Slack window content access
    print("\n4. Testing Slack Window Content Access...")
    script4 = '''
    tell application "System Events"
        try
            tell process "Slack"
                if (count of windows) > 0 then
                    set windowTitle to title of window 1
                    return "SUCCESS: Window title = " & windowTitle
                else
                    return "ERROR: No Slack windows found"
                end if
            end tell
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    result4 = run_applescript(script4)
    print(f"   Result: {result4}")
    
    # Analyze results
    print("\n" + "="*60)
    print("📊 PERMISSION ANALYSIS:")
    print("="*60)
    
    if "SUCCESS" in result1:
        print("✅ Basic System Events: WORKING")
    else:
        print("❌ Basic System Events: FAILED")
    
    if "SUCCESS" in result2:
        print("✅ Process Detection: WORKING")
    else:
        print("❌ Process Detection: FAILED")
    
    if "SUCCESS" in result3:
        print("✅ Application UI Access: WORKING")
    else:
        print("❌ Application UI Access: FAILED - THIS IS THE ISSUE")
    
    if "SUCCESS" in result4:
        print("✅ Window Content Access: WORKING")
    else:
        print("❌ Window Content Access: FAILED - THIS IS THE ISSUE")
    
    # Provide recommendations
    print("\n🔧 RECOMMENDATIONS:")
    print("="*60)
    
    if "ERROR" in result3 or "ERROR" in result4:
        print("❌ You need to grant FULL Accessibility permissions:")
        print()
        print("1. System Settings → Privacy & Security → Accessibility")
        print("2. Make sure these are ALL present and enabled:")
        print("   □ Terminal")
        print("   □ Python/python3") 
        print("   □ osascript")
        print("3. If missing, add them manually")
        print("4. RESTART Terminal after changes")
        print("5. Run this test again")
    else:
        print("✅ All permissions are working correctly!")
        print("The Slack integration should work perfectly now.")

def run_applescript(script):
    """Run AppleScript and return result"""
    try:
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"ERROR: {result.stderr.strip()}"
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    test_permission_level()
