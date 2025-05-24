# agri_entry_bot/main.py

from utilities.automation_helper import AutomationHelper
from utilities.config import *

print("Starting AgriAutomationService...")

if __name__ == "__main__":
    website_url=WEBSITE_URL
    state_name=STATE_NAME
    username=USERNAME
    password=PASSWORD
    village_name=VILLAGE_NAME

    service = AutomationHelper(website_url, state_name, username, password, village_name)
    # Run the automation service
    service.run_automation()