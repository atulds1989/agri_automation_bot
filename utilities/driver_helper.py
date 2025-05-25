# agri_entry_bot/utilities/driver_helper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utilities.config import CHROME_DRIVER_PATH

# --- Setup WebDriver Function ---
def setup_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Suppress verbose logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver