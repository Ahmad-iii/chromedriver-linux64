# Import statements
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from selenium.webdriver.chrome.options import Options
import os

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
    """Find the email input field - optimized version"""
    try:
        # Wait for inputs to be present
        time.sleep(1)  # Brief wait for page load
        inputs = driver.find_elements(By.XPATH, "//input[@type='text' and @class='form-control entry-disabled']")
        for inp in inputs:
            if inp.is_displayed() and inp.is_enabled():
                print("Found email field")
                return inp
    except Exception as e:
        print(f"Error finding email field: {e}")
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

def get_target_number_by_lens():
    """Extract target number using Google Lens OCR with optimized speed and reliability"""
    print("🔍 Using Google Lens to extract target number...")
    
    try:
        # Take focused screenshot of CAPTCHA area only
        screenshot_path = "captcha_debug.png"
        try:
            # More specific CAPTCHA area selector for faster location
            captcha_area = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'captcha') or .//div[contains(text(), 'Please select all boxes')]]"))
            )
            captcha_area.screenshot(screenshot_path)
            print("✅ Captured CAPTCHA area")
        except:
            # Quick fallback to full screenshot
            driver.save_screenshot(screenshot_path)
            print("⚠️ Using full page screenshot")

        # Store original window handle
        original_window = driver.current_window_handle
        
        try:
            # Open Google Lens in new tab
            driver.execute_script("window.open('https://www.google.com/imghp');")
            lens_window = [w for w in driver.window_handles if w != original_window][0]
            driver.switch_to.window(lens_window)
            
            # Wait for page to fully load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Search by image']"))
            )
            print("✅ Google Lens page loaded")
            time.sleep(1)  # Extra wait to ensure page is fully interactive
            
            # Click camera icon with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    camera_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Search by image']"))
                    )
                    camera_btn.click()
                    print("✅ Clicked camera icon")
                    
                    # Wait for file input to be present after click
                    upload_input = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )
                    
                    # Prepare absolute path and upload
                    abs_path = os.path.abspath(screenshot_path)
                    upload_input.send_keys(abs_path)
                    print("✅ Uploaded image")
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    else:
                        raise
            
            # Wait for and check Gemini response with progressive delay
            print("Checking for Gemini response...")
            start_time = time.time()
            check_intervals = [0.5, 0.5, 1, 1, 2]  # Progressive delays
            
            for wait_time in check_intervals:
                time.sleep(wait_time)
                
                try:
                    gemini_element = driver.find_element(By.XPATH, "//div[@class='rPeykc']")
                    text = gemini_element.text.strip()
                    
                    if text:
                        print(f"Found Gemini response: {text}")
                        matches = re.findall(r'\b(\d{3})\b', text)
                        if matches:
                            number = matches[0]
                            print(f"✅ Extracted number: {number}")
                            driver.close()
                            driver.switch_to.window(original_window)
                            return number
                except:
                    continue
            
            # If no early response, try search
            try:
                print("No immediate response, trying search...")
                search_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "APjFqb"))
                )
                
                search_box.clear()
                search_box.send_keys("what number to select")
                time.sleep(0.5)
                search_box.send_keys(Keys.RETURN)
                print("✅ Performed search")
                
                # Wait longer for search results
                time.sleep(2)
                
                # Final check for response
                gemini_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='rPeykc']"))
                )
                text = gemini_element.text.strip()
                matches = re.findall(r'\b(\d{3})\b', text)
                if matches:
                    number = matches[0]
                    print(f"✅ Found number after search: {number}")
                    driver.close()
                    driver.switch_to.window(original_window)
                    return number
                    
            except Exception as e:
                print(f"Search attempt failed: {e}")
            
            # Cleanup
            driver.close()
            driver.switch_to.window(original_window)
            
        except Exception as e:
            print(f"Error during Lens process: {e}")
            try:
                driver.close()
                driver.switch_to.window(original_window)
            except:
                pass
            
    except Exception as e:
        print(f"Error in overall process: {e}")
    
    return None

def get_target_number():
    """Get the target number using multiple methods"""
    # First try Google Lens method as it's most reliable
    target = get_target_number_by_lens()
    if target:
        return target
        
    print("⚠️ Google Lens method failed, trying fallback methods...")
    
    # Step 1: Find all elements containing the instruction text
    instruction_selectors = [
        # Most specific selectors first
        "//div[@class='box-label' and contains(text(), 'Please select all boxes with number')]",
        "//div[contains(@class, 'captcha')]//div[contains(text(), 'Please select all boxes with number')]",
        "//*[contains(text(), 'Please select all boxes with number')]"
    ]
    
    all_instructions = []
    for selector in instruction_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            for element in elements:
                try:
                    # Complex visibility check
                    if not element.is_displayed():
                        continue
                        
                    # Check element dimensions
                    size = element.size
                    if size['height'] == 0 or size['width'] == 0:
                        continue
                        
                    # Check if hidden by CSS
                    style = element.get_attribute('style')
                    if style and ('display: none' in style or 'visibility: hidden' in style):
                        continue
                        
                    # Check if parent elements are visible
                    parent = element
                    is_visible = True
                    for _ in range(3):  # Check up to 3 parent levels
                        try:
                            parent = parent.find_element(By.XPATH, '..')
                            parent_style = parent.get_attribute('style')
                            if (not parent.is_displayed() or
                                (parent_style and ('display: none' in parent_style or 'visibility: hidden' in parent_style))):
                                is_visible = False
                                break
                        except:
                            break
                    
                    if not is_visible:
                        continue
                        
                    # Element passed all visibility checks
                    text = element.text.strip()
                    if text:
                        score = 0
                        
                        # Score the element based on various factors
                        if 'box-label' in (element.get_attribute('class') or ''):
                            score += 5
                            
                        if element.location['y'] < 500:  # Near top of page
                            score += 3
                            
                        if len(text) < 100:  # Not too long (probably not concatenated)
                            score += 2
                            
                        # Clean instruction text (no other numbers)
                        other_numbers = len(re.findall(r'\d+', text))
                        if other_numbers == 1:  # Only one number
                            score += 3
                            
                        all_instructions.append({
                            'element': element,
                            'text': text,
                            'score': score
                        })
                        
                except Exception as e:
                    print(f"Error checking element: {e}")
                    continue
                    
        except Exception as e:
            print(f"Selector failed: {selector} - {e}")
            continue
    
    # Sort instructions by score
    all_instructions.sort(key=lambda x: x['score'], reverse=True)
    
    # Try each instruction, starting with highest score
    for instruction in all_instructions:
        try:
            text = instruction['text']
            print(f"Checking instruction (score {instruction['score']}): {text[:50]}...")
            
            # Look for 3-digit number with word boundaries
            matches = re.findall(r'\b(\d{3})\b', text)
            if matches:
                number = matches[0]
                
                # Validate number appears in grid
                try:
                    # Get all visible grid cell numbers
                    grid_numbers = set()
                    grid_cells = driver.find_elements(
                        By.XPATH,
                        "//div[string-length(normalize-space(text()))=3 and number(normalize-space(text()))=normalize-space(text())]"
                    )
                    
                    for cell in grid_cells:
                        if (cell.is_displayed() and
                            cell.size['width'] > 20 and
                            cell.size['height'] > 20):
                            cell_text = cell.text.strip()
                            if cell_text.isdigit():
                                grid_numbers.add(cell_text)
                    
                    print(f"Grid numbers found: {grid_numbers}")
                    
                    if number in grid_numbers:
                        print(f"✅ Validated target number {number} exists in grid")
                        return number
                    else:
                        print(f"❌ Number {number} not found in grid")
                        continue
                        
                except Exception as e:
                    print(f"Error validating grid numbers: {e}")
                    # If we can't validate against grid, still return the number
                    print(f"⚠️ Returning unvalidated number {number}")
                    return number
                    
        except Exception as e:
            print(f"Error processing instruction: {e}")
            continue
    
    print("❌ Could not find valid target number")
    return None

def get_captcha_cells(driver, target_number):
    """Find CAPTCHA cells - optimized version"""
    try:
        # The cells are in a grid with specific class
        wait = WebDriverWait(driver, 5)
        
        # Look for all cells containing numbers
        cells = wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[string-length(normalize-space(text()))=3 and translate(text(),' ','')=translate(text(),'0123456789','0123456789')]")
            )
        )
        
        if cells:
            # Filter for visible cells only
            valid_cells = [cell for cell in cells if cell.is_displayed()]
            print(f"Found {len(valid_cells)} CAPTCHA cells")
            return valid_cells
            
    except Exception as e:
        print(f"Error finding CAPTCHA cells: {e}")
        
    return []

def click_captcha_cell(cell, driver):
    """Optimized CAPTCHA cell clicking"""
    try:
        if not cell.is_displayed():
            return False
            
        # Try JavaScript click first as it's usually most reliable
        driver.execute_script("arguments[0].click();", cell)
        time.sleep(0.1)  # Minimal wait
        
        # Verify click through class change
        new_class = cell.get_attribute('class')
        if 'selected' in new_class.lower():
            return True
            
        # Fallback to regular click if needed
        cell.click()
        time.sleep(0.1)
        
        return True
        
    except Exception as e:
        print(f"Error clicking cell: {e}")
        return False

def solve_captcha():
    """Main function to solve the CAPTCHA - optimized for speed"""
    # Get target number - maximum 2 retries
    for attempt in range(2):
        target_number = get_target_number_by_lens()
        if target_number:
            break
        print(f"Retry {attempt + 1}/2")
    
    if not target_number:
        print("❌ Could not get target number")
        return False
    
    print(f"Target number: {target_number}")
    
    # Quick lookup for matching cells
    try:
        cells = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, f"//div[text()='{target_number}']")
            )
        )
        
        clicks = 0
        for cell in cells:
            if cell.is_displayed() and cell.size['width'] > 20:
                try:
                    driver.execute_script("arguments[0].click();", cell)
                    clicks += 1
                except:
                    continue
        
        return clicks > 0
        
    except Exception as e:
        print(f"Error clicking cells: {e}")
        return False

# Main execution block
try:
    # Open website
    driver.get(WEBSITE_URL)
    print("Website opened")
    
    # Handle popup if present (quick check)
    try:
        popup = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close')]"))
        )
        popup.click()
    except:
        pass
    
    # Click login
    login_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/header/nav[1]/div/ul/li[2]/a/span"))
    )
    login_button.click()
    
    # Find and enter email
    email_field = find_email_field()
    if not email_field:
        raise Exception("Email field not found")
        
    email_field.send_keys(EMAIL)
    
    # Click verify
    verify_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "btnVerify"))
    )
    verify_button.click()
    
    # Enter password
    password_field = find_password_field()
    if not password_field:
        raise Exception("Password field not found")

    try:
        # Clear first just in case
        password_field.clear()
        # Try JavaScript to set value first
        driver.execute_script("arguments[0].value = arguments[1];", password_field, PASSWORD)
        time.sleep(0.5)  # Short wait
        
        # Then send keys to trigger any necessary events
        password_field.send_keys("")  # Empty string to trigger events
        
        # Verify the value was set
        actual_value = driver.execute_script("return arguments[0].value;", password_field)
        if not actual_value:
            # If JavaScript approach didn't work, try conventional sendKeys
            password_field.send_keys(PASSWORD)
    except Exception as e:
        print(f"Error entering password: {e}")
        raise Exception("Failed to enter password")
    
    # Solve CAPTCHA
    if not solve_captcha():
        raise Exception("CAPTCHA solving failed")
    
    # Click submit
    submit_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()
    
    # Quick success check
    time.sleep(2)
    if "dashboard" in driver.current_url.lower():
        print("Login successful!")
    
except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("error.png")
    
finally:
    time.sleep(5)  # Reduced wait time
    driver.quit()
