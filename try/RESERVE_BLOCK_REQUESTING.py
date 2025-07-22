import requests
import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated.*")
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import re
import pygame
import time
import os
import logging

# --- Logging Setup ---
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "claimed_blocks.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Constants ---
GECKO_DRIVER_PATH = r'.\geko\geko\geckodriver.exe'
PROFILE_PATH = r"C:\Users\amits\AppData\Roaming\Mozilla\Firefox\Profiles\71lyw803.default-release"
SOUND_PATH = r"try\mixkit-video-game-win-2016.wav"
CALENDAR_URL = "https://cloudfactory.app/calendar/"
WORK_DESC_TEXT1 = "Advance Review - Element Status"
WORK_DESC_TEXT2 = "Floor-Adv. Reviewer"
WORK_DESC_TEXT3 = "Image Annotation"

# --- Initialize Sound ---
pygame.mixer.init()
sound = pygame.mixer.Sound(SOUND_PATH)

def play_sound():
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))

# --- WebDriver Setup ---
def get_driver():
    options = Options()
    options.profile = FirefoxProfile(PROFILE_PATH)
    service = Service(executable_path=GECKO_DRIVER_PATH)
    return webdriver.Firefox(service=service, options=options)

# --- Login Function ---
def login():
    try:
        driver = get_driver()
        driver.get(CALENDAR_URL)
        driver.maximize_window()
        time.sleep(3)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.element_to_be_clickable((By.ID, "google-login"))).click()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "yAlK0b"))).click()
        return driver
    except Exception:
        print(f"Login failed")
        logging.error(f"Login failed")
        return None

def _try_close_modal(modal):
    """Helper to safely close the modal dialog."""
    try:
        cancel = modal.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[1]')
        cancel.click()
    except Exception as close_err:
        logging.warning(f"Couldn't close modal: {close_err}")

def reserve_block(worker_id, demand_pool_id, cookie_string):
    url = f"https://cloudfactory.app/calendar/api/workers/{worker_id}/demand_pools/{demand_pool_id}/reserve"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Cookie": cookie_string
    }
    payload = {"commitmentDuration": 120, "timeZone": "Asia/Katmandu"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Successfully reserved block for demand_pool {demand_pool_id}")
            logging.info(f"Reserved block for demand_pool {demand_pool_id} at {time.ctime()}")
            return True
        else:
            print(f"❌ Failed to reserve block: {response.status_code} - {response.text}")
            logging.error(f"Failed to reserve block for demand_pool {demand_pool_id}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending POST request: {e}")
        logging.error(f"Error sending POST request for demand_pool {demand_pool_id}: {e}")
        return False

def find_block(driver):
    wait = WebDriverWait(driver, 10)
    day_classes = ['fc-day-mon', 'fc-day-tue', 'fc-day-wed', 'fc-day-thu', 'fc-day-fri']
    
    # Get cookies after login
    cookies = driver.get_cookies()
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    worker_id = "fd5d793f-9982-4c77-aa8f-07fb5475c376"

    while True:
        blocks = []
        for day_class in day_classes:
            for day_element in driver.find_elements(By.CLASS_NAME, day_class):
                for block in day_element.find_elements(By.CLASS_NAME, 'event-opportunity'):
                    try:
                        desc = block.find_element(By.CLASS_NAME, 'ws-des').text
                        if any(text in desc for text in [WORK_DESC_TEXT1, WORK_DESC_TEXT2, WORK_DESC_TEXT3]):
                            # Clear previous requests to avoid memory issues
                            driver.requests.clear()
                            
                            # Click block to trigger eligibility_check request
                            block.click()
                            
                            # Wait for modal and close it quickly
                            modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-content')))
                            _try_close_modal(modal)
                            # Extract demand_pool_id from eligibility_check request
                            demand_pool_id = None
                            for request in driver.requests:
                                if "eligibility_check" in request.url and "demand_pools" in request.url:
                                    match = re.search(r'demand_pools/([0-9a-f-]+)/eligibility_check', request.url)
                                    if match:
                                        demand_pool_id = match.group(1)
                                        break
                            
                            if not demand_pool_id:
                                print(f"❌ Skipped block — No demand_pool_id found in eligibility_check request")
                                logging.warning(f"Skipped block: No demand_pool_id found for block with desc '{desc}'")
                                continue

                            blocks.append({
                                "demand_pool_id": demand_pool_id,
                                "description": desc,
                                "day_class": day_class
                            })
                            print(f"🔔 Found block: '{desc}' on {day_class}, demand_pool_id {demand_pool_id}")
                            logging.info(f"Found block: '{desc}' on {day_class}, demand_pool_id {demand_pool_id}")
                    except Exception as e:
                        print(f"❌ Error processing block: {e}")
                        logging.error(f"Error processing block: {e}")
                        _try_close_modal(modal)

        # Process collected blocks
        for block in blocks:
            demand_pool_id = block["demand_pool_id"]
            desc = block["description"]
            print(f"🔔 Attempting to reserve block: '{desc}', demand_pool_id {demand_pool_id}")
            logging.info(f"Attempting to reserve block: '{desc}', demand_pool_id {demand_pool_id}")

            # Reserve block
            if reserve_block(worker_id, demand_pool_id, cookie_string):
                play_sound()
                # Optionally stop after first successful reservation
                # return

def main():
    while True:
        driver = login()
        time.sleep(7)
        driver.get("https://cloudfactory.app/calendar/")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fc-dom-1"]')))
        while True:
            try:
                find_block(driver)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/button'))).click()
                time.sleep(0.4)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/button[1]'))).click()
                time.sleep(0.4)
            except Exception as e:
                print("Session Expired... Reloading....c")
                driver.quit()
                main()

if __name__ == "__main__":
    main()
