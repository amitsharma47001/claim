import random
import re
import time
import gc
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import pygame
import telebot

# --- Obfuscated Constants ---
_LOG_DIR = "".join(["l", "o", "g", "s"])
_LOG_FILE = os.path.join(_LOG_DIR, "".join(["c", "l", "a", "i", "m", "e", "d", "_", "b", "l", "o", "c", "k", "s", ".", "l", "o", "g"]))
os.makedirs(_LOG_DIR, exist_ok=True)

# --- Randomized Logging Setup ---
logging.basicConfig(
    filename=_LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Obfuscated Telegram credentials
_TELEGRAM_BOT_TOKEN = ''.join(['7', '3', '8', '6', '6', '0', '8', '7', '6', '4', ':', 'A', 'A', 'H', 'F', 'x', 'K', 'A', 'd', 'e', '4', 'i', 'E', 'H', '5', 'u', '7', 'h', 'A', 'z', '2', 'K', 'o', 'h', 's', 'V', '_', 'y', 'V', '4', '_', 'Q', 'F', 'R', 'c', 's'])
_CHAT_ID = ''.join(['5', '9', '6', '1', '1', '8', '2', '9', '0', '5'])

# Initialize the Telegram bot with random delays
time.sleep(random.uniform(0.5, 1.5))
bot = telebot.TeleBot(_TELEGRAM_BOT_TOKEN)

def _send_telegram_message(message):
    """Send message with random delay to mimic human behavior"""
    time.sleep(random.uniform(1, 3))
    try:
        bot.send_message(_CHAT_ID, message)
    except Exception as e:
        logging.warning(f"Telegram send failed: {str(e)}")

# --- Randomized Paths ---
_GECKO_DRIVER_PATH = os.path.join('.', 'geko', 'geko', 'geckodriver.exe')
_PROFILE_PATH = os.path.join("C:", "Users", "amits", "AppData", "Roaming", "Mozilla", "Firefox", "Profiles", "71lyw803.default-release")
_SOUND_PATHS = {
    'success': os.path.join("try", "mixkit-video-game-win-2016.wav"),
    'start': os.path.join("try", "mixkit-slot-machine-win-alert-1931.wav")
}

# --- Randomized URLs and XPaths ---
_URLS = {
    'calendar': "https://cloudfactory.app/calendar/",
    'login': "https://cloudfactory.app/login"
}

_XPATHS = {
    'reload_button': '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/button',
    'filter_button': '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/button[1]',
    'claim_button': "/html/body/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[2]",
    'cancel_button': '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[1]'
}

# --- Work Description Variations ---
_WORK_DESCS = ["Advanced", "Adv", "Advanced Work"]

# --- Human-like Behavior Patterns ---
class HumanLike:
    @staticmethod
    def random_delay(min=0.1, max=0.5):
        time.sleep(random.uniform(min, max))
    
    @staticmethod
    def random_mouse_movement(driver, element=None):
        try:
            action = ActionChains(driver)
            if element:
                action.move_to_element_with_offset(element, random.randint(-5, 5), random.randint(-5, 5))
            else:
                action.move_by_offset(random.randint(-50, 50), random.randint(-50, 50))
            action.perform()
            HumanLike.random_delay(0.05, 0.2)
        except:
            pass

# --- Sound Manager ---
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'success': pygame.mixer.Sound(_SOUND_PATHS['success']),
            'start': pygame.mixer.Sound(_SOUND_PATHS['start'])
        }
    
    def play(self, sound_type):
        try:
            self.sounds[sound_type].play()
            pygame.time.wait(int(self.sounds[sound_type].get_length() * 1000))
        except:
            pass

sound_manager = SoundManager()

# --- Stealth WebDriver Setup ---
def _get_driver():
    options = Options()
    
    # Disable automation flags
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    
    # Randomize user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    options.set_preference("general.useragent.override", random.choice(user_agents))
    
    # Enable profile with random settings
    profile = FirefoxProfile(_PROFILE_PATH)
    profile.set_preference("privacy.trackingprotection.enabled", random.choice([True, False]))
    options.profile = profile
    
    # Randomize window size
    options.add_argument(f"--window-size={random.randint(1200, 1400)},{random.randint(800, 1000)}")
    
    # Disable logging
    service = Service(executable_path=_GECKO_DRIVER_PATH, log_path=os.devnull)
    
    driver = webdriver.Firefox(service=service, options=options)
    
    # Remove navigator.webdriver flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# --- Login with Human-like Behavior ---
def _login():
    try:
        driver = _get_driver()
        HumanLike.random_delay(1, 2)
        
        # Randomize starting page
        if random.random() > 0.5:
            driver.get(_URLS['login'])
            HumanLike.random_delay(2, 3)
            driver.get(_URLS['calendar'])
        else:
            driver.get(_URLS['calendar'])
        
        # Randomize window management
        if random.random() > 0.3:
            driver.maximize_window()
        else:
            driver.set_window_size(random.randint(1200, 1400), random.randint(800, 1000))
        
        HumanLike.random_delay(2, 4)
        
        wait = WebDriverWait(driver, random.randint(10, 20))
        
        # Human-like mouse movement before clicking
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "google-login")))
        HumanLike.random_mouse_movement(driver, login_btn)
        HumanLike.random_delay(0.5, 1.5)
        login_btn.click()
        
        HumanLike.random_delay(1, 2)
        
        # Random account selection behavior
        account_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "yAlK0b")))
        for _ in range(random.randint(1, 3)):
            HumanLike.random_mouse_movement(driver, account_btn)
        account_btn.click()
        
        return driver
    except Exception as e:
        logging.error(f"Login failed: {str(e)}")
        return None

# --- Claim Block with Randomized Behavior ---
def _claim_block(driver, block, allowed_times=['10:45', '14:45']):
    try:
        # Human-like interaction with block
        for _ in range(random.randint(1, 3)):
            HumanLike.random_mouse_movement(driver, block)
        block.click()
        HumanLike.random_delay(0.2, 0.8)
        
        modal = WebDriverWait(driver, random.randint(8, 12)).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'modal-content'))
        )

        # Extract start time with regex
        description = modal.find_element(By.ID, 'work-reserve-description').text
        match_time = re.search(r'(\d{2}:\d{2})', description)
        start_time = match_time.group(1) if match_time else None

        if not start_time:
            logging.warning("Skipped block - no start time found")
            _try_close_modal(modal)
            return

        if start_time not in allowed_times:
            logging.info(f"Skipped block - time {start_time} not allowed")
            _try_close_modal(modal)
            return

        # Human-like slider interaction
        slider = WebDriverWait(driver, random.randint(5, 10)).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "rc-slider-handle"))
        )
        
        for _ in range(3):
            HumanLike.random_mouse_movement(driver, slider)
            slider.click()
            slider.send_keys(Keys.ARROW_UP)
            HumanLike.random_delay(0.1, 0.3)

        # Random delay before claiming
        HumanLike.random_delay(0.5, 1.5)
        
        claim_btn = WebDriverWait(driver, random.randint(5, 10)).until(
            EC.element_to_be_clickable((By.XPATH, _XPATHS['claim_button']))
        )
        HumanLike.random_mouse_movement(driver, claim_btn)
        claim_btn.click()

        try:
            WebDriverWait(driver, random.randint(3, 7)).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "modal-content"))
            )
            sound_manager.play('success')
            timestamp = time.ctime()
            msg = f"✅ Claimed block at {timestamp} - Start: {start_time}"
            print(msg)
            _send_telegram_message(msg)
            logging.info(f"CLAIMED block at {timestamp} - Start: {start_time}")
        except:
            logging.warning("Possible claim failure")
        
        HumanLike.random_delay(1, 3)
        
    except Exception as e:
        logging.error(f"Block claim error: {str(e)}")
        _try_close_modal(modal)

def _try_close_modal(modal):
    """Safely close modal with human-like behavior"""
    try:
        cancel = modal.find_element(By.XPATH, _XPATHS['cancel_button'])
        for _ in range(random.randint(1, 2)):
            HumanLike.random_mouse_movement(modal.parent, cancel)
        cancel.click()
        HumanLike.random_delay(0.5, 1)
    except Exception as e:
        logging.warning(f"Modal close failed: {str(e)}")

# --- Find Blocks with Randomization ---
def _find_blocks(driver):
    wait = WebDriverWait(driver, random.randint(8, 15))
    day_classes = ['fc-day-sun', 'fc-day-mon', 'fc-day-tue', 'fc-day-wed', 'fc-day-thu', 'fc-day-fri']
    
    # Randomize search order
    random.shuffle(day_classes)
    
    for day_class in day_classes:
        for day_element in driver.find_elements(By.CLASS_NAME, day_class):
            try:
                blocks = day_element.find_elements(By.CLASS_NAME, 'event-opportunity')
                random.shuffle(blocks)  # Randomize block processing order
                
                for block in blocks:
                    try:
                        desc = block.find_element(By.CLASS_NAME, 'ws-des')
                        if any(work_desc in desc.text for work_desc in _WORK_DESCS):
                            HumanLike.random_mouse_movement(driver, block)
                            wait.until(EC.element_to_be_clickable(block))
                            _claim_block(driver, block)
                            HumanLike.random_delay(0.5, 1.5)
                    except NoSuchElementException:
                        continue
            except Exception as e:
                logging.warning(f"Day element error: {str(e)}")
                continue

# --- Main Loop with Randomized Patterns ---
def _main():
    while True:
        driver = _login()
        if not driver:
            HumanLike.random_delay(30, 60)  # Longer delay if login fails
            continue
            
        try:
            # Random navigation pattern
            nav_sequence = random.choice([
                lambda: driver.get(_URLS['calendar']),
                lambda: (driver.get(_URLS['login']), HumanLike.random_delay(2, 4), driver.get(_URLS['calendar']))
            ])
            nav_sequence()
            
            HumanLike.random_delay(5, 10)
            
            wait = WebDriverWait(driver, random.randint(12, 20))
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fc-dom-1"]')))
            
            while True:
                gc.collect()
                try:
                    # Randomize search frequency
                    _find_blocks(driver)
                    
                    # Randomize reload pattern
                    if random.random() > 0.3:  # 70% chance to reload
                        reload_btn = wait.until(EC.presence_of_element_located((By.XPATH, _XPATHS['reload_button'])))
                        HumanLike.random_mouse_movement(driver, reload_btn)
                        reload_btn.click()
                        HumanLike.random_delay(0.3, 0.8)
                        
                        if random.random() > 0.4:  # 60% chance to filter
                            filter_btn = wait.until(EC.presence_of_element_located((By.XPATH, _XPATHS['filter_button'])))
                            HumanLike.random_mouse_movement(driver, filter_btn)
                            filter_btn.click()
                            HumanLike.random_delay(0.2, 0.6)
                    
                    # Random sleep between iterations
                    sleep_time = random.uniform(0.5, 3.5)
                    time.sleep(sleep_time)
                    
                except Exception as e:
                    logging.error(f"Main loop error: {str(e)}")
                    driver.quit()
                    HumanLike.random_delay(5, 15)
                    break
                    
        except Exception as e:
            logging.error(f"Session error: {str(e)}")
            try:
                driver.quit()
            except:
                pass
            HumanLike.random_delay(30, 120)  # Longer delay on major errors

if __name__ == "__main__":
    sound_manager.play('start')
    _main()