from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import traceback


# ✅ Setup WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")  # Fixes Mac issues
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")  # Headless mode for stability

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# ✅ Ensure Page Fully Loads
def wait_for_page_load(driver, timeout=15):
    WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")


# ✅ Wait for an Element to be Present
def wait_for_element(driver, by, value, timeout=15, condition=EC.presence_of_element_located):
    """
    Waits for an element and ensures it's visible and interactable before returning.
    """
    try:
        element = WebDriverWait(driver, timeout).until(condition((by, value)))
        WebDriverWait(driver, timeout).until(EC.visibility_of(element))
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        return element
    except TimeoutException:
        print(f"❌ Timeout: Could not find element {value}")
        return None


# ✅ Scroll to Element
def scroll_to_element(driver, by, value):
    """
    Scrolls the element into view before interaction.
    """
    try:
        element = wait_for_element(driver, by, value)
        if element:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element
    except Exception as e:
        print(f"❌ Scroll error: {e}")
        return None


# ✅ Handle Stale Element Reference
def retry_find_element(driver, by, value, retries=3):
    """
    Retries finding an element to avoid stale element errors.
    """
    for attempt in range(retries):
        try:
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        except StaleElementReferenceException:
            print(f"🔄 Retrying element: {value} (Attempt {attempt + 1})")
    raise Exception(f"❌ Could not find element after {retries} attempts!")


# ✅ Function to log in
def login(driver):
    driver.get("https://staging-web.wise.live")
    wait_for_page_load(driver)

    mobile_button = wait_for_element(driver, By.XPATH, "//button[contains(., 'Continue with Mobile')]")
    if mobile_button:
        mobile_button.click()

    phone_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='Phone number']")
    if phone_input:
        phone_input.send_keys("1111100000")

    otp_btn = wait_for_element(driver, By.XPATH, "//button[span[contains(text(), 'Get OTP')]]")
    if otp_btn:
        otp_btn.click()

    otp_input = wait_for_element(driver, By.XPATH, "//div[contains(@class, 'v-otp-input')]//input")
    if otp_input:
        otp_input.send_keys("0000")

    verify_btn = wait_for_element(driver, By.XPATH, "//button[span[contains(text(),' Verify')]]")
    if verify_btn:
        verify_btn.click()

    institute_name = wait_for_element(driver, By.XPATH, "//span[contains(text(), 'Testing Institute')]")
    assert institute_name and "Testing Institute" in institute_name.text, "❌ Institute name assertion failed!"

    print("✅ Successfully logged in and verified institute name.")


# ✅ Navigate to Classroom
def navigate_to_classroom(driver):
    group_courses_tab = wait_for_element(driver, By.XPATH, "//span[contains(text(),'Group courses')]")
    if group_courses_tab:
        group_courses_tab.click()

    classroom = wait_for_element(driver, By.XPATH, "//a[contains(text(),'Classroom for Automated testing')]")
    if classroom:
        classroom.click()

    classroom_header = wait_for_element(driver, By.XPATH, "//div[contains(text(),'Classroom for Automated testing')]")
    assert classroom_header and "Classroom for Automated testing" in classroom_header.text, "❌ Classroom assertion failed!"
    print("✅ Classroom opened successfully.")


# ✅ Schedule a session (Fixed)
def schedule_session(driver):
    live_sessions_tab = wait_for_element(driver, By.XPATH, "//a[contains(text(), 'Live Sessions')]")
    if live_sessions_tab:
        live_sessions_tab.click()
    else:
        print("❌ Live Sessions tab not found!")

    schedule_btn_xpath = "//button[.//i[contains(@class, 'mdi-calendar-outline')] and .//span[contains(text(), 'Schedule Sessions')]]"
    scroll_to_element(driver, By.XPATH, schedule_btn_xpath)
    schedule_btn = wait_for_element(driver, By.XPATH, schedule_btn_xpath)
    if schedule_btn:
        schedule_btn.click()

    add_session_xpath = "//button[.//span[@class='v-btn__content' and contains(text(), 'Add session')]]"
    scroll_to_element(driver, By.XPATH, add_session_xpath)
    add_session_btn = wait_for_element(driver, By.XPATH, add_session_xpath)
    if add_session_btn:
        add_session_btn.click()
        print("✅ Add session clicked successfully.")

    time_picker = wait_for_element(driver, By.XPATH, "//input[@type='time']")
    if time_picker:
        time_picker.clear()
        time_picker.send_keys("22:00")

    create_btn = wait_for_element(driver, By.XPATH, "//button[contains(text(),'Create')]")
    if create_btn:
        create_btn.click()

    session_card = wait_for_element(driver, By.XPATH, "//div[contains(@class,'session-card')]")
    assert session_card, "❌ Session card not found!"

    session_details = wait_for_element(driver, By.XPATH, "//div[contains(text(),'Upcoming')]")
    assert session_details and "Upcoming" in session_details.text, "❌ Session status not upcoming!"

    print("✅ Session scheduled successfully and verified!")


# ✅ Main Function
def main():
    driver = setup_driver()

    try:
        login(driver)
        navigate_to_classroom(driver)
        schedule_session(driver)

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        traceback.print_exc()

    finally:
        driver.quit()
        print("✅ Browser closed successfully.")


# ✅ Run script
if __name__ == "__main__":
    main()
