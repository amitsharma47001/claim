from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import pygame
import time
import gc
import os
import logging
import telebot

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

# Your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7386608764:AAHFxKAde4iEH5u7hAz2KohsV_yV4_QFRcs'
CHAT_ID = '5961182905'

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Function to send a Telegram message
def send_telegram_message(message):
    bot.send_message(CHAT_ID, message)

# --- Constants ---
GECKO_DRIVER_PATH = r'.\geko\geko\geckodriver.exe'
PROFILE_PATH = r"C:\Users\amits\AppData\Roaming\Mozilla\Firefox\Profiles\71lyw803.default-release"
SOUND_PATH = r"try\mixkit-video-game-win-2016.wav"
SOUND_START_PATH = r"try\mixkit-slot-machine-win-alert-1931.wav"
CALENDAR_URL = "https://cloudfactory.app/calendar/"
RELOAD_BTN_XPATH = '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/button'
FILTER_BTN_XPATH = '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/button[1]'
WORK_DESC_TEXT1 = "Advance Review - Element Status"
WORK_DESC_TEXT2 = "Floor-Adv. Reviewer"
WORK_DESC_TEXT3 = "Floor-Annotators"
WORK_DESC_TEXT4 = "Element Status"
WORK_DESC_TEXT5 = "On-Call Basic Review"


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
# def claim_block(driver, block, allowed_times=['02:00','08:00','06:00','12:00','10:00','16:00', '14:00','20:00', '18:00','00:00']):
def claim_block(driver, block, allowed_times=['06:00']):
    try:
        block.click()
        time.sleep(0.1)
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'modal-content'))
        )

        # Extract start time from modal body
        description = modal.find_element(By.ID, 'work-reserve-description').text
        match_time = re.search(r'(\d{2}:\d{2})', description)
        start_time = match_time.group(1) if match_time else None


        if not start_time:
            print("❌ Skipped: No start time found in modal.")
            logging.warning("Skipped block because no start time was found.")
            _try_close_modal(modal)
            return

        if start_time not in allowed_times:
            print(f"❌ Skipped block — Start time {start_time} not in desired list {allowed_times}")
            logging.info(f"Skipped block with start time {start_time} (not in allowed list)")
            _try_close_modal(modal)
            return

        # ✅ Proceed to claim
        
        slider = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "rc-slider-handle"))
        )
        slider.click()
        for _ in range(1):
            slider.send_keys(Keys.ARROW_UP)

        claim = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[2]")))
        claim.click()
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "modal-content"))
            )
            play_sound()
            timestamp = time.ctime()
            print(f"✅ Claimed block at {timestamp} — Start time: {start_time}")
            send_telegram_message(f"✅ Claimed block at {timestamp} — Start time: {start_time}")
            logging.info(f"CLAIMED block at {timestamp} — Start time: {start_time}")
        except:
            print("Claim may have failed.")
        time.sleep(2)
    except Exception :
        logging.error(f"FAILED to claim block at {time.ctime()}")
        print(f"❌ Error claiming block")
        time.sleep(1)
        _try_close_modal(modal)

def _try_close_modal(modal):
    """Helper to safely close the modal dialog."""
    try:
        cancel = modal.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[1]')
        cancel.click()
    except Exception as close_err:
        logging.warning(f"Couldn't close modal: {close_err}")


# --- Find Work Blocks ---
def find_block(driver):
    wait = WebDriverWait(driver, 10)
    day_classes = ['fc-day-sun', 'fc-day-mon', 'fc-day-tue', 'fc-day-wed']
    for day_class in day_classes:
        for day_element in driver.find_elements(By.CLASS_NAME, day_class):
            try:
                for block in day_element.find_elements(By.CLASS_NAME, 'event-opportunity'):
                    try:
                        desc = block.find_element(By.CLASS_NAME, 'ws-des')
                        if (WORK_DESC_TEXT1 in desc.text) or (WORK_DESC_TEXT2 in desc.text) or (WORK_DESC_TEXT3 in desc.text) or (WORK_DESC_TEXT4 in desc.text) or (WORK_DESC_TEXT5 in desc.text):
                            wait.until(EC.element_to_be_clickable(block))
                            claim_block(driver, block)
                    except NoSuchElementException:
                        continue
            except Exception:
                continue

# --- Main Loop ---
def main():
    while True:
        driver = login()
        time.sleep(7)
        driver.get("https://cloudfactory.app/calendar/")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fc-dom-1"]')))
        while True:
            gc.collect()
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
