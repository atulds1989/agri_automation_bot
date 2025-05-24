from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import random
import numpy as np
from selenium.common.exceptions import TimeoutException
import time
from utilities.config import CHROME_DRIVER_PATH

# --- Setup WebDriver Function ---
def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Uncomment if you want headless mode
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Suppress verbose logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
