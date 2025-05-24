import os
from dotenv import load_dotenv

load_dotenv(override=True)

# --- Configuration ---
CHROME_DRIVER_PATH = r"E:\projects\agri_entry_bot\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
WEBSITE_URL = os.getenv("WEBSITE_URL")
STATE_NAME = os.getenv("STATE_NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
VILLAGE_NAME = os.getenv("VILLAGE_NAME")
