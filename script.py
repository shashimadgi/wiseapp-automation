from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")  # Fixes issues on Mac
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



# Set an explicit wait time
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Visit the staging website
    driver.get("https://staging-web.wise.live")

    # Step 2: Login using phone number
    mobile_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue with Mobile')]")))

    mobile_button.click()

    time.sleep(3)

    Phone_number_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone number']")))
    Phone_number_input.send_keys("1111100000")
    time.sleep(3)

    # Click "Next" or "Submit" button (adjust selector accordingly)
    submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[span[contains(text(), 'Get OTP')]]")))  # Adjust as per UI
    submit_btn.click()
    time.sleep(3)

    # Step 3: Enter OTP
    otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'v-otp-input')]//input")))
    otp_input.send_keys("0000")
    time.sleep(3)

    # Click "Submit"
    Verify_otp_btn = driver.find_element(By.XPATH, "//button[span[contains(text(),' Verify')]]")
    Verify_otp_btn.click()
    # Step 4: Assert that "Testing Institute" is displayed
    institute_name = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Testing Institute')]")))
    assert "Testing Institute" in institute_name.text, "Institute name assertion failed!"

    print("✅ Successfully logged in and verified institute name.")

    # Step 5: Navigate to Classroom
    group_courses_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Group courses')]")))
    group_courses_tab.click()
    time.sleep(3)

    classroom = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Classroom for Automated testing')]")))
    classroom.click()
    time.sleep(3)

    # Assert classroom opened successfully
    classroom_header = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Classroom for Automated testing')]")))
    assert "Classroom for Automated testing" in classroom_header.text, "Classroom assertion failed!"
    print("✅ Classroom opened successfully.")

    time.sleep(3)

    # Step 6: Schedule a session
    live_sessions_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Live Sessions')]")))
    live_sessions_tab.click()
    time.sleep(3)

    schedule_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//i[contains(@class, 'mdi-calendar-outline')] and .//span[contains(text(), 'Schedule Sessions')]]")))
    schedule_btn.click()
    time.sleep(3)

    add_session_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[@class='v-btn__content' and contains(text(), 'Add session')]]")))
    add_session_btn.click()
    print("Add session clicked success.....")
    time.sleep(10)

    # Set session time (Select Today 10PM)
    time_picker = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='time']")))  # Adjust based on UI
    time_picker.clear()
    time_picker.send_keys("22:00")

    create_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create')]")))
    create_btn.click()

    # Step 7: Assert session details
    session_card = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'session-card')]")))
    assert session_card, "Session card not found!"

    session_details = driver.find_element(By.XPATH, "//div[contains(text(),'Upcoming')]")
    assert "Upcoming" in session_details.text, "Session status not upcoming!"

    print("✅ Session scheduled successfully and verified!")

except Exception as e:
    print(f"❌ Error occurred: {e}")

finally:
    # Close the browser
    time.sleep(3)
    driver.quit()
