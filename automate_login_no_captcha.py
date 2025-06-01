from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.chrome.options import Options

# Configuration
CHROMEDRIVER_PATH = "/home/ahmad/chromedriver-linux64/chromedriver"
WEBSITE_URL = "https://appointment.theitalyvisa.com/Global/home/index"
EMAIL = "muhammadaqibjaved061@gmail.com"
PASSWORD = "Aqibrao@232"

# Chrome options
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Random user agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# Initialize the Chrome WebDriver with options
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Add headers via CDP
driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
    'headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'DNT': '1'
    }
})

def find_email_field():
    """Find the email input field using the known working strategy"""
    # First, try to remove the 'entry-disabled' class from all inputs
    try:
        driver.execute_script("""
            var inputs = document.querySelectorAll('input.entry-disabled');
            for (var i = 0; i < inputs.length; i++) {
                inputs[i].classList.remove('entry-disabled');
                inputs[i].disabled = false;
                inputs[i].readOnly = false;
            }
        """)
        print("Removed entry-disabled class from inputs")
        time.sleep(1)
    except Exception as e:
        print(f"Could not remove entry-disabled class: {e}")
    
    # Find visible input with form-control class
    try:
        inputs = driver.find_elements(By.CSS_SELECTOR, "input.form-control")
        for inp in inputs:
            if inp.is_displayed():
                print(f"Found email field with name: {inp.get_attribute('name')}")
                return inp
    except Exception as e:
        print(f"Failed to find email field: {e}")
    
    return None

def find_password_field():
    """Try multiple strategies to find the password field after verify is clicked"""
    print("Looking for password field...")
    
    # Wait a bit for the page to update after verify
    time.sleep(2)
    
    # Debug: Check all visible inputs again after verify
    try:
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(all_inputs)} total inputs after verify:")
        for i, inp in enumerate(all_inputs):
            if inp.is_displayed():
                print(f"Visible Input {i+1}: type={inp.get_attribute('type')}, name={inp.get_attribute('name')}, id={inp.get_attribute('id')}")
    except Exception as e:
        print(f"Error debugging inputs: {e}")
    
    # Strategy 1: Look for password type inputs
    password_strategies = [
        (By.XPATH, "//input[@type='password']"),
        (By.CSS_SELECTOR, "input[type='password']"),
        # Look for any visible input that might be the password field
        (By.XPATH, "//input[@type='text' and contains(@class, 'form-control') and not(contains(@class, 'entry-disabled'))]"),
        # Look for input near password label
        (By.XPATH, "//label[contains(text(), 'Password')]/following-sibling::input"),
        (By.XPATH, "//label[contains(text(), 'Password')]/..//input"),
        # Look for any input below the email that's visible
        (By.XPATH, "//form//input[@type='text' and @class='form-control'][last()]"),
        # Try to find by position - password field often comes after email
        (By.XPATH, "(//input[@type='text' and @class='form-control'])[last()]"),
    ]
    
    for by, selector in password_strategies:
        try:
            elements = driver.find_elements(by, selector)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    print(f"Found potential password field using: {selector}")
                    return element
        except Exception as e:
            print(f"Password strategy failed - {selector}: {e}")
            continue
    
    # Strategy 2: Look for any visible, enabled input that's not the email field
    try:
        visible_inputs = driver.find_elements(By.XPATH, "//input[@type='text' or @type='password']")
        for inp in visible_inputs:
            if inp.is_displayed() and inp.is_enabled():
                # Check if this input is empty and not the email field
                current_value = inp.get_attribute('value')
                if not current_value or current_value != EMAIL:
                    print(f"Found empty visible input, trying as password field: {inp.get_attribute('name')}")
                    return inp
    except Exception as e:
        print(f"Alternative password search failed: {e}")
    
    # Strategy 3: JavaScript approach to find password field
    try:
        password_element = driver.execute_script("""
            var inputs = document.querySelectorAll('input');
            for (var i = 0; i < inputs.length; i++) {
                var input = inputs[i];
                if (input.type === 'password' || 
                    (input.offsetParent !== null && input.value === '' && input !== arguments[0])) {
                    return input;
                }
            }
            return null;
        """, find_email_field())
        
        if password_element:
            print("Found password field using JavaScript")
            return password_element
    except Exception as e:
        print(f"JavaScript password search failed: {e}")
    
    return None

def debug_page_state():
    """Debug function to understand the page state"""
    print("\n=== DEBUGGING PAGE STATE ===")
    print(f"Current URL: {driver.current_url}")
    print(f"Page Title: {driver.title}")
    
    # Find all input elements
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"\nFound {len(inputs)} input elements:")
    for i, inp in enumerate(inputs):
        try:
            print(f"Input {i+1}:")
            print(f"  - Type: {inp.get_attribute('type')}")
            print(f"  - Name: {inp.get_attribute('name')}")
            print(f"  - ID: {inp.get_attribute('id')}")
            print(f"  - Class: {inp.get_attribute('class')}")
            print(f"  - Placeholder: {inp.get_attribute('placeholder')}")
            print(f"  - Visible: {inp.is_displayed()}")
            print(f"  - Enabled: {inp.is_enabled()}")
            print("---")
        except Exception as e:
            print(f"  - Error getting attributes: {e}")

try:
    # Step 1: Open the website
    driver.get(WEBSITE_URL)
    print("Website opened successfully.")
    time.sleep(3)  # Give page time to load

    # Step 1.5: Handle the pop-up notification if it appears
    try:
        popup_selectors = [
            "//button[contains(@class, 'close')]",
            "//span[contains(text(), '×')]",
            "//div[contains(@class, 'close')]",
            "//button[contains(text(), 'Close')]",
            "//button[contains(text(), 'OK')]",
            "//*[@class='close']",
            "//*[contains(@class, 'modal')]//button"
        ]
        
        popup_closed = False
        for selector in popup_selectors:
            try:
                popup = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, selector)))
                popup.click()
                popup_closed = True
                print("Closed popup using selector:", selector)
                break
            except:
                continue
        
        if not popup_closed:
            print("No popup found or unable to close")
            
    except Exception as e:
        print("Pop-up handling completed:", e)

    # Step 2: Click the "Login" button
    login_selectors = [
        "/html/body/header/nav[1]/div/ul/li[2]/a/span",
        "//a[contains(text(), 'Login')]",
        "//span[contains(text(), 'Login')]",
        "//button[contains(text(), 'Login')]",
        "//*[contains(@class, 'login')]",
        "//a[contains(@href, 'login')]"
    ]
    
    login_clicked = False
    for selector in login_selectors:
        try:
            login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, selector)))
            login_button.click()
            login_clicked = True
            print("Clicked login using selector:", selector)
            break
        except:
            continue
    
    if not login_clicked:
        raise Exception("Could not find or click login button")
    
    # Wait for login page to load
    time.sleep(3)
    
    # Debug page state before trying email
    debug_page_state()

    # Step 3: Find and enter email
    print("\n=== ATTEMPTING EMAIL ENTRY ===")
    
    # First, try to wait for the page to fully load and execute any JavaScript
    time.sleep(2)
    
    # Find and fill email field
    email_field = find_email_field()
    if not email_field:
        raise Exception("Could not find email field")
    
    # Clear and enter email
    email_field.clear()
    email_field.send_keys(EMAIL)
    print("Entered email address")
    
    # Find and click the Verify button specifically
    verify_button_selectors = [
        (By.ID, "btnVerify"),  # Try ID first
        (By.XPATH, "//button[@id='btnVerify']"),  # Then by ID with button tag
        (By.XPATH, "//button[contains(text(), 'Verify')]"),  # Then by text
        (By.XPATH, "//input[@value='Verify']"),  # Then by input value
        (By.XPATH, "//*[contains(@class, 'verify-button')]")  # Then by class
    ]
    
    verify_clicked = False
    for by, selector in verify_button_selectors:
        try:
            verify_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((by, selector)))
            # Add a small delay before clicking
            time.sleep(1)
            verify_button.click()
            verify_clicked = True
            print(f"Successfully clicked Verify button using selector: {selector}")
            break
        except Exception as e:
            print(f"Failed to click Verify with selector {selector}: {e}")
            continue
    
    if not verify_clicked:
        raise Exception("Could not find or click Verify button")

    # Wait for password field to appear
    time.sleep(2)  # Give time for the page to update

    # Step 4: Enter password
    print("\n=== ATTEMPTING PASSWORD ENTRY ===")
    password_field = find_password_field()
    
    if password_field is None:
        print("Could not find password field, trying manual approach...")
        # Take screenshot to see current state
        driver.save_screenshot("password_debug.png")
        print("Screenshot saved as 'password_debug.png'")
        
        # Try clicking on likely password field location
        try:
            # Look for any empty input field
            empty_inputs = driver.find_elements(By.XPATH, "//input[@type='text' or @type='password']")
            for inp in empty_inputs:
                if inp.is_displayed() and not inp.get_attribute('value'):
                    print(f"Trying empty input: {inp.get_attribute('name')}")
                    try:
                        inp.click()
                        inp.send_keys(PASSWORD)
                        password_field = inp
                        print("Password entered in empty input")
                        break
                    except:
                        continue
        except Exception as e:
            print(f"Manual password approach failed: {e}")
    
    if password_field:
        try:
            # Multiple methods to enter password
            password_methods = [
                lambda: password_field.clear() and password_field.send_keys(PASSWORD),
                lambda: driver.execute_script("arguments[0].value = '';", password_field) or password_field.send_keys(PASSWORD),
                lambda: driver.execute_script("arguments[0].value = arguments[1];", password_field, PASSWORD),
                lambda: password_field.send_keys(Keys.CONTROL + "a") and password_field.send_keys(PASSWORD)
            ]
            
            password_entered = False
            for i, method in enumerate(password_methods):
                try:
                    method()
                    current_value = password_field.get_attribute("value")
                    if current_value == PASSWORD:
                        print(f"Password entered successfully using method {i+1}")
                        password_entered = True
                        break
                    else:
                        print(f"Password method {i+1} failed - value length: {len(current_value) if current_value else 0}")
                except Exception as e:
                    print(f"Password method {i+1} failed: {e}")
                    continue
            
            if not password_entered:
                print("All password entry methods failed!")
        except Exception as e:
            print(f"Error entering password: {e}")
    else:
        print("Could not find password field!")

    print("\n=== REMOVING CAPTCHA STEPS - Implement your own CAPTCHA solution here ===")
    time.sleep(2)

    # Step 6: Click the "Submit" button
    print("\n=== ATTEMPTING SUBMIT ===")
    submit_selectors = [
        "//button[@type='submit']",
        "//input[@type='submit']",
        "//button[contains(text(), 'Submit')]",
        "//button[contains(text(), 'Login')]",
        "//*[contains(@class, 'submit')]",
        "//button[contains(@class, 'btn-success')]",  # Green submit button
        "//form//button[last()]"
    ]
    
    submit_clicked = False
    for selector in submit_selectors:
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            submit_button.click()
            print(f"Clicked Submit button using: {selector}")
            submit_clicked = True
            break
        except Exception as e:
            print(f"Submit selector failed {selector}: {e}")
            continue
    
    if not submit_clicked:
        print("Warning: Could not find Submit button")

    # Wait to observe the result
    time.sleep(5)

    # Optional: Verify login success
    current_url = driver.current_url.lower()
    if "dashboard" in current_url or "home" in current_url or "appointment" in current_url:
        print("Login appears successful!")
    else:
        print(f"Login status unclear. Current URL: {driver.current_url}")

except Exception as e:
    print(f"An error occurred: {e}")
    # Take screenshot for debugging
    try:
        driver.save_screenshot("error_screenshot.png")
        print("Error screenshot saved as 'error_screenshot.png'")
    except:
        pass

finally:
    # Wait a bit before closing to see results
    print("Waiting 10 seconds before closing browser...")
    time.sleep(30)
    driver.quit()
