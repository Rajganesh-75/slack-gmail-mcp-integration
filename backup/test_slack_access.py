#!/usr/bin/env python3
"""
Quick test to check if we can access Slack Web
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def test_slack_web_access():
    print("🧪 Testing Slack Web Access...")
    print("=" * 50)
    
    driver = None
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Create driver
        print("🔧 Starting Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1200, 800)
        
        # Navigate to Slack
        print("🌐 Navigating to Slack Web...")
        driver.get("https://slack.com/signin")
        time.sleep(5)
        
        # Check if page loaded
        page_title = driver.title
        print(f"📄 Page title: {page_title}")
        
        if "slack" in page_title.lower():
            print("✅ Slack Web is accessible!")
            print("🔍 Looking for sign-in elements...")
            
            # Look for sign-in form
            signin_elements = driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[type='text']")
            if signin_elements:
                print("✅ Sign-in form found!")
            else:
                print("⚠️ Sign-in form not immediately visible")
            
            print(f"🌐 Current URL: {driver.current_url}")
            print("\n💡 You should see a Chrome window with Slack's sign-in page")
            print("💡 This confirms that our automation can access Slack Web")
            
            # Wait a bit for you to see
            print("\n⏳ Keeping browser open for 10 seconds so you can see...")
            time.sleep(10)
            
            return True
        else:
            print(f"❌ Unexpected page: {page_title}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if driver:
            print("🧹 Closing browser...")
            driver.quit()

if __name__ == "__main__":
    success = test_slack_web_access()
    if success:
        print("\n🎉 Slack Web access test PASSED!")
        print("✅ Ready to proceed with full integration")
    else:
        print("\n❌ Slack Web access test FAILED")
        print("💡 Check your internet connection and try again")
