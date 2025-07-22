from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
import time
import pygame
import telebot
import gc

WORK_DESC_TEXT1 = "Advance Review - Element Status"
WORK_DESC_TEXT2 = "Floor-Adv. Reviewer"
WORK_DESC_TEXT3 = "Floor-Annotators"
WORK_DESC_TEXT4 = "Element Status"
WORK_DESC_TEXT5 = "On-Call Basic Review"


# Initialize pygame mixer
pygame.mixer.init()
sound = pygame.mixer.Sound(r'try\mixkit-video-game-win-2016.wav')
sound_start = pygame.mixer.Sound(r'try\mixkit-slot-machine-win-alert-1931.wav')

def play():
    # Play the sound
    sound.play()

    # Keep the program running long enough to hear the sound
    pygame.time.wait(int(sound.get_length() * 1000))

# Your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7386608764:AAHFxKAde4iEH5u7hAz2KohsV_yV4_QFRcs'
CHAT_ID = '5961182905'

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Function to send a Telegram message
def send_telegram_message(message):
    bot.send_message(CHAT_ID, message)

# Path to the Firefox profile
profile_path = r"C:\Users\amits\AppData\Roaming\Mozilla\Firefox\Profiles\71lyw803.default-release"
print(profile_path)

# Set up the Firefox options and specify the profile
options = Options()

# Set profile directory
options.profile = FirefoxProfile(profile_path)

# Initialize the WebDriver with the options
service = Service(executable_path=r'.\geko\geko\geckodriver.exe')  # Update with your actual geckodriver path

def login():
    try:
        driver = webdriver.Firefox(service=service,options=options)
        driver.get("https://cloudfactory.app/calendar/")
        driver.maximize_window()
        time.sleep(3)
        wait  = WebDriverWait(driver, 10)
        glogin =  wait.until(EC.element_to_be_clickable((By.ID, "google-login")))
        glogin.click()
        choose = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "yAlK0b")))
        choose.click()
        time.sleep(4)
        return driver
    except Exception as e:
        print("Login Failed !")
        
def _try_close_modal(modal):
    """Helper to safely close the modal dialog."""
    try:
        cancel = modal.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[1]')
        cancel.click()
    except Exception as close_err:
        print(f"Couldn't close modal: {close_err}")
        
def claim_block(block, driver):
    try:
        block.click()
        wait = WebDriverWait(driver, 10)
        time.sleep(0.2)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'modal-content')))
        slider = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "rc-slider-handle")))
        slider.click()
        slider.send_keys(Keys.ARROW_UP)*3
        claim = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[3]/button[2]")))
        claim.click()
        print(
            f"-------------------------$$$$$$$$$$----------######   Work Block Claimed !!!  :) ######----------$$$$$$$$$$----------------------------------at ::: {str(time.ctime())}"
        )
    except Exception:
        print(f"❌ Error claiming block")
        time.sleep(0.1)
        _try_close_modal()
        
def find_block(driver):
    wait = WebDriverWait(driver, 10)
    elements_list = driver.find_elements(By.CLASS_NAME, "event-opportunity")
    extra = driver.find_elements(By.CLASS_NAME, 'fa-info-circle')
    # Step 4: Store elements in a list and loop through each     
    elements_list = list(elements_list)
    extra_list = list(extra)
    result = elements_list + extra_list

    if (result):
        play()
        print(f"Work Block Available !!! at ::: {str(time.ctime())}")
        for block in result:
            try:
                desc = block.find_element(By.CLASS_NAME, 'ws-des')
                if (WORK_DESC_TEXT1 in desc.text) or (WORK_DESC_TEXT2 in desc.text) or (WORK_DESC_TEXT3 in desc.text) or (WORK_DESC_TEXT4 in desc.text) or (WORK_DESC_TEXT5 in desc.text):
                    play()
                    wait.until(EC.element_to_be_clickable(block))
                    print(f"🔔 Block available at {time.ctime()}")
                    claim_block(block, driver)
            except Exception as ex:
                continue
      
def main():
    while True:
        # Log in initially
        driver = login()
        driver.get("https://cloudfactory.app/calendar/")
        wait = WebDriverWait(driver, 10)
        while True:
            gc.collect()
            try:
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/button'))).click()
                time.sleep(0.5)
                find_block(driver)
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div[1]/div/div/div[3]/div[2]/div/div/div[1]/div[1]/div/button[1]'))).click()
                time.sleep(0.5)
            except Exception as e:
                driver.quit()
                main()
                    
if __name__ == "__main__":
    main()