# agri_automation/main.py
from utilities.automation_helper import AutomationHelper
from utilities.config import *

print("Starting AgriAutomationService...")

if __name__ == "__main__":
    # You can instantiate the service with default config values
    # or override them here if needed.
    # For example, to use a different village:

    service = AutomationHelper()
    service.run_automation()