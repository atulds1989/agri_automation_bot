# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# import random
# import numpy as np
# from selenium.common.exceptions import TimeoutException
# import time

# # --- Configuration ---
# CHROME_DRIVER_PATH = r"E:\projects\agri_entry_bot\chromedriver-win64\chromedriver-win64\chromedriver.exe"
# WEBSITE_URL = "https://agcensus.gov.in/AgriCensus/Agri_2122.jsp"
# STATE_NAME = "14 Madhya Pradesh"
# USERNAME = "101008881"
# PASSWORD = "1234"
# VILLAGE_NAME = "473746 Mathni"
# # VILLAGE_NAME = "473749 Pipalda"

# # --- Setup WebDriver Function ---
# def setup_driver():
#     options = Options()
#     # options.add_argument("--headless")  # Uncomment if you want headless mode
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--log-level=3")  # Suppress verbose logs
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])

#     service = Service(CHROME_DRIVER_PATH)
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver

# # --- Main Script Logic ---
# def run_automation():
#     driver = None

#     try:
#         driver = setup_driver()
#         print(f"Navigating to: {WEBSITE_URL}")
#         driver.get(WEBSITE_URL)

#         # --- (A) LOGIN FLOW ---
#         print("Waiting for login page to load…")
#         WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
#         time.sleep(1)

#         print("Filling State from state list")
#         statename_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "state_list")))
#         statename_field.send_keys(STATE_NAME)

#         print("Filling username…")
#         username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_id")))
#         username_field.send_keys(USERNAME)

#         print("Filling password…")
#         password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password")))
#         password_field.send_keys(PASSWORD)

#         print("\n--- ACTION REQUIRED: Select State & enter Captcha in the browser. ---")
#         time.sleep(20)
#         print("Resuming… Clicking Procced…")
#         WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
#         login_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "Procced")))
#         driver.execute_script("arguments[0].click();", login_btn)
#         time.sleep(1)

#         print("Waiting for main menu to load…")
#         WebDriverWait(driver, 30).until(EC.url_contains("MenuScreen.jsp"))
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Phase II")))
#         print("Logged in.")

#         # --- (B1) NAVIGATE TO DATA ENTRY SCREEN ---
#         print("Clicking Phase II…")
#         phase_ii_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Phase II")))
#         phase_ii_link.click()
#         time.sleep(2)

#         print("Clicking Data Entry Screen (Schedule wise)…")
#         data_entry_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Data Entry Screen (Schedule wise)")))
#         data_entry_link.click()
#         WebDriverWait(driver, 20).until(EC.url_contains("Schedule_H.jsp"))
#         time.sleep(2)
#         print("On Schedule_H.jsp.")

#         # --- (B2) SELECT VILLAGE NAME FROM BLOCK A ---
#         print(f"Selecting Village: {VILLAGE_NAME}")
#         # try:
#         #     village_dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "vlg_list")))
#         #     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", village_dropdown)
#         #     village_dropdown.click()
#         #     time.sleep(0.5)
#         #     village_dropdown.find_element(By.XPATH, f".//option[normalize-space(text())='{VILLAGE_NAME}']").click()
#         #     print(f"→ source_irri set to '{VILLAGE_NAME}'")
#         # except Exception as e:
#         #     print(f"Could not set Source of Irrigation: {e}")
            
#         village_dropdown = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "vlg_list")))
#         select_village = Select(village_dropdown)
#         select_village.select_by_visible_text(VILLAGE_NAME)
#         time.sleep(1)  # wait briefly after selection

#         # --- (C) COUNT HOW MANY FARMERS ARE IN THE POP‐UP (ONCE) ---
#         original_window = driver.current_window_handle
#         print("\nCounting total farmers in the pop-up…")

#         # Open the pop-up
#         schedules_button = WebDriverWait(driver, 15).until(
#             EC.element_to_be_clickable((
#                 By.XPATH,
#                 "//button[contains(text(), 'Schedules(Ph.-I)')] | //input[@type='button' and @value='Schedules(Ph.-I)']"
#             ))
#         )

#         schedules_button.click()

#         # Switch to pop-up window
#         WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
#         for handle in driver.window_handles:
#             if handle != original_window:
#                 popup_window = handle
#                 driver.switch_to.window(popup_window)
#                 break

#         # Wait for the table and count rows
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='myTable']")))
#         all_rows = driver.find_elements(By.XPATH, "//table[@id='myTable']/tbody/tr")
#         num_farmers = len(all_rows) - 1  # subtract header row
#         print(f"Found {num_farmers} farmers to process.")

#         # Close pop-up and return
#         driver.close()
#         driver.switch_to.window(original_window)
#         time.sleep(1)

#         if num_farmers < 1:
#             print("No farmers found. Exiting.")
#             return

#         # --- (D) LOOP THROUGH EACH FARMER, ALWAYS TARGETING tr[2] ---
#         for idx in range(0, 2):
#             print(f"\n===== Processing farmer {idx+1} of {2} =====")

#             # (D.1) Re-open the “Schedules(Ph.-I)” pop-up
#             schedules_button = WebDriverWait(driver, 15).until(
#                 EC.element_to_be_clickable((
#                     By.XPATH,
#                     "//button[contains(text(), 'Schedules(Ph.-I)')] | //input[@type='button' and @value='Schedules(Ph.-I)']"
#                 ))
#             )
#             schedules_button.click()

#             # Switch to pop-up window
#             WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
#             for handle in driver.window_handles:
#                 if handle != original_window:
#                     popup_window = handle
#                     driver.switch_to.window(popup_window)
#                     break

#             # Wait for table to load
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='myTable']")))

#             # (D.2) Extract “Area Operated” from row 2, column 5
#             area_xpath = "//table[@id='myTable']/tbody/tr[2]/td[5]"
#             print("Extracting Area Operated from the first data row…")
#             extracted_area_value = 0.0
#             try:
#                 area_cell = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, area_xpath)))
#                 extracted_area_str = area_cell.text.strip()
#                 extracted_area_value = float(extracted_area_str)
#             except Exception as e:
#                 print(f"Could not extract Area Operated or convert to float: {e}")
#                 extracted_area_value = 0.0
#             print(f"→ Extracted Area = {extracted_area_value:.4f}")

#             # (D.3) Click the checkbox in row[2]
#             checkbox_xpath = "//table[@id='myTable']/tbody/tr[2]//input[@type='checkbox']"
#             print("Clicking checkbox for that farmer…")
#             try:
#                 checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
#                 checkbox.click()
#                 print("Farmer selected.")
#             except Exception as e:
#                 print(f"Could not click farmer checkbox: {e}")

#             # Pop-up closes automatically → switch back to main window
#             driver.switch_to.window(original_window)
#             WebDriverWait(driver, 10).until(EC.url_contains("Schedule_H.jsp"))
#             print("Switched back to main data entry form.")

#             # --- Calculate fallow_area_value BEFORE using extracted_area_value for total_area ---
#             fallow_area_value = 0.0
#             # Iterate through field_05 to field_15 to sum their values for fallow_area_value
#             for i in range(5, 16): # This loop goes from 5 to 15 (inclusive)
#                 field_name = f"field_{i:02d}" # Formats as field_05, field_06, etc.
#                 try:
#                     fallow_field = WebDriverWait(driver, 5).until(
#                         EC.presence_of_element_located((By.NAME, field_name))
#                     )
#                     field_value_str = fallow_field.get_attribute("value").strip()
#                     if field_value_str:
#                         fallow_area_value += float(field_value_str)
#                     print(f"  Fetched {field_name}: {field_value_str}. Current fallow_area_value: {fallow_area_value:.4f}")
#                 except TimeoutException:
#                     print(f"  {field_name} not found or not visible; skipping for fallow area calculation.")
#                 except ValueError:
#                     print(f"  Could not convert value of {field_name} ('{field_value_str}') to float; skipping.")
#                 except Exception as e:
#                     print(f"  An error occurred while fetching {field_name}: {e}")

#             print(f"Total calculated fallow_area_value: {fallow_area_value:.4f}")

#             # Calculate result_real_area
#             result_real_area = extracted_area_value - fallow_area_value
#             print(f"Calculated result_real_area (extracted_area_value - fallow_area_value): {result_real_area:.4f}")

#             # Now, use result_real_area for your total_area for filling Block C
#             total_area = result_real_area # Use the corrected area
#             formatted_full = f"{total_area:.4f}"

#             # (D.4) BLOCK C → fill field_05, field_06, tot_crops
#             print("--- Filling Block C ---")

#             # 04. Net Irrigated Area → field_05 (This field is now overwritten based on result_real_area)
#             try:
#                 field05 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "field_05")))
#                 driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field05)
#                 field05.clear()
#                 field05.send_keys(formatted_full)
#                 field05.send_keys(Keys.TAB)
#                 time.sleep(0.5)
#                 print(f"→ field_05 set to {formatted_full}")
#             except Exception as e:
#                 print(f"Could not set field_05: {e}")

#             # # 05. Net Unirrigated Area → field_06 = "0.0000"
#             # try:
#             #     field06 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "field_06")))
#             #     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field06)
#             #     field06.clear()
#             #     field06.send_keys("0.0000")
#             #     field06.send_keys(Keys.TAB)
#             #     time.sleep(0.5)
#             #     print("→ field_06 set to 0.0000")
#             # except:
#             #     print("field_06 not found; skipping")

#             # Number of Crops → tot_crops = "3"
#             got_crops = False
#             try:
#                 crops_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "tot_crops")))
#                 got_crops = True
#             except TimeoutException:
#                 try:
#                     crops_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
#                         By.XPATH,
#                         "//td[contains(normalize-space(text()), 'Number of Crops grown during the reference year')]/following-sibling::td//input"
#                     )))
#                     got_crops = True
#                 except:
#                     got_crops = False

#             if got_crops:
#                 try:
#                     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", crops_field)
#                     crops_field.clear()
#                     crops_field.send_keys("3")
#                     crops_field.send_keys(Keys.TAB)
#                     time.sleep(0.5)
#                     print("→ tot_crops set to 3")
#                 except Exception as e:
#                     print(f"Could not fill tot_crops: {e}")
#                     got_crops = False
#             else:
#                 print("Number of Crops field not found; skipping Block D")

#             # # (D.5) BLOCK D → only if got_crops True AND total_area > 0.0
#             # if got_crops and total_area > 0.0:
#             #     print("--- Filling Block D ---")
#                 # first_half_area = np.round(total_area / 2.0)
#                 # second_half_area = np.round(total_area - first_half_area)

#                 # print(f"total area : {total_area:4f}, Calculated first_half_area: {first_half_area:.4f},\
#                 #        second_half_area: {second_half_area:.4f}")
                
#                 # first_formatted_half = f"{first_half_area:.4f}"
#                 # second_formatted_half = f"{first_half_area:.4f}"

#             # (D.5) BLOCK D → only if got_crops True AND total_area > 0.0
#             if got_crops and total_area > 0.0:
#                 print("--- Filling Block D ---")
#                 half_area = total_area / 2.0
#                 formatted_half = f"{half_area:.4f}"

#                 print(f"total area : {total_area:4f}, Calculated first_half_area: {half_area:.4f}")
                
#                 # Row 1: cr_code_10 & unirri_ar_10
#                 try:
#                     code1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "cr_code_10")))
#                     unirri1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "unirri_ar_10")))
#                     code1.clear()
#                     code1.send_keys("1009")
#                     unirri1.clear()
#                     unirri1.send_keys(formatted_full)
#                     unirri1.send_keys(Keys.TAB)
#                     time.sleep(0.3)
#                 except Exception as e:
#                     print(f"Could not fill Block D row 1: {e}")

#                 # Row 2: cr_code_11 & irri_ar_11
#                 try:
#                     code2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "cr_code_11")))
#                     irr2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "irri_ar_11")))
#                     code2.clear()
#                     code2.send_keys("201")
#                     irr2.clear()
#                     irr2.send_keys(formatted_half)
#                     irr2.send_keys(Keys.TAB)
#                     time.sleep(0.3)
#                 except Exception as e:
#                     print(f"Could not fill Block D row 2: {e}")

#                 # Row 3: cr_code_12 & irri_ar_12
#                 try:
#                     code3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "cr_code_12")))
#                     irr3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "irri_ar_12")))
#                     code3.clear()
#                     code3.send_keys("106")
#                     irr3.clear()
#                     irr3.send_keys(formatted_half)
#                     irr3.send_keys(Keys.TAB)
#                     time.sleep(0.3)
#                 except Exception as e:
#                     print(f"Could not fill Block D row 3: {e}")

#                 print("Block D rows filled.\n")
#             else:
#                 print("Skipping Block D (no Crops or missing field).\n")

#             # (D.6) SOURCE OF IRRIGATION → Random pick, fill Remarks, then Save → SweetAlert2 pop-ups
#             pick_list = ["2 - Wells", "3 - Tubewells", "5 - Others"]
#             pick = random.choice(pick_list)
#             try:
#                 src_sel = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "source_irr")))
#                 driver.execute_script("arguments[0].scrollIntoView({block:'center'});", src_sel)
#                 src_sel.click()
#                 time.sleep(0.5)
#                 src_sel.find_element(By.XPATH, f".//option[normalize-space(text())='{pick}']").click()
#                 print(f"→ source_irri set to '{pick}'")
#             except Exception as e:
#                 print(f"Could not set Source of Irrigation: {e}")
#             time.sleep(0.5)

#             try:
#                 # field05 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "field_05")))
#                 # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field05)

#                 rem = WebDriverWait(driver, 5).until(
#                     EC.element_to_be_clickable((
#                         By.NAME,
#                         "remarks"
#                     ))
#                 )
#                 driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rem)
#                 rem.clear()
#                 rem.send_keys("Ok")
#                 time.sleep(1.0)
#                 print("→ Remarks filled.")
#             except:
#                 print("Remarks field not found; skipping")

#             # Click “Save”
#             try:
#                 save_b = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((
#                         By.XPATH,
#                         "//input[@type='button' and @value='Save'] | //button[normalize-space(text())='Save']"
#                     ))
#                 )
#                 driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_b)
#                 save_b.click()
#                 time.sleep(1.0)
#             except Exception as e:
#                 print(f"Could not click Save: {e}")

#             # SweetAlert2 “Yes”
#             try:
#                 print("Waiting for Yes…")
#                 yes_btn = WebDriverWait(driver, 5).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
#                 )
#                 yes_btn.click()
#                 time.sleep(1.0)
#                 print("Clicked Yes.")
#             except:
#                 print("No Yes appeared; moving on…")

#             # SweetAlert2 “OK”
#             try:
#                 print("Waiting for OK…")
#                 ok_btn = WebDriverWait(driver, 5).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
#                 )
#                 ok_btn.click()
#                 time.sleep(2.0)
#                 print("Clicked OK. Record saved.\n")
#             except:
#                 print("No OK appeared; assuming success.\n")

#         # End of for-loop
#         print("\nAll farmers have been processed!")

#     except Exception as e:
#         print(f"\n‼ Unhandled exception: {e}")
#         if driver:
#             print("Browser remains open for inspection. Press ENTER to close.")
#             input()
#             driver.quit()

#     finally:
#         print("\nScript complete. Press ENTER to close browser.")
#         if driver:
#             try:
#                 input()
#                 driver.quit()
#             except:
#                 pass
#         print("Done.")

# if __name__ == "__main__":
#     run_automation()









# import time
# import random
# import numpy as np # Though np.round is not explicitly used, it's imported in original
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# # Assuming utilities.driver_helper exists and has setup_driver
# from utilities.driver_helper import setup_driver

# class AutomationHelper:
#     """
#     Automates data entry on an agricultural website, handling login,
#     navigation, data extraction, form filling, and pop-up interactions.
#     """

#     def __init__(self, website_url, state_name, username, password, village_name):
#         self.website_url = website_url
#         self.state_name = state_name
#         self.username = username
#         self.password = password
#         self.village_name = village_name
#         self.driver = setup_driver()
#         self.original_window = None

#     def _wait_for_page_load(self, timeout=30):
#         """Waits until the document.readyState is 'complete'."""
#         WebDriverWait(self.driver, timeout).until(
#             lambda d: d.execute_script("return document.readyState") == "complete"
#         )
#         time.sleep(1) # Small buffer after readyState is complete

#     def _fill_input_field(self, by_locator, value, field_name, tab_after=True):
#         """Helper to locate, clear, and fill an input field."""
#         try:
#             field = WebDriverWait(self.driver, 20).until(
#                 EC.presence_of_element_located(by_locator)
#             )
#             # Scroll into view if needed, especially for elements lower on the page
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
#             field.clear()
#             field.send_keys(value)
#             if tab_after:
#                 field.send_keys(Keys.TAB)
#             print(f"→ Filled '{field_name}' with: {value}")
#             time.sleep(0.5) # Short delay for UI updates
#             return True
#         except TimeoutException:
#             print(f"Error: Field '{field_name}' not found within timeout.")
#             return False
#         except Exception as e:
#             print(f"Error filling '{field_name}': {e}")
#             return False

#     def _click_element(self, by_locator, element_name, timeout=15, use_js_click=False):
#         """Helper to locate and click an element."""
#         try:
#             element = WebDriverWait(self.driver, timeout).until(
#                 EC.element_to_be_clickable(by_locator)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
#             if use_js_click:
#                 self.driver.execute_script("arguments[0].click();", element)
#             else:
#                 element.click()
#             print(f"→ Clicked '{element_name}'.")
#             time.sleep(1) # Small buffer after click
#             return True
#         except TimeoutException:
#             print(f"Error: '{element_name}' not clickable within timeout.")
#             return False
#         except Exception as e:
#             print(f"Error clicking '{element_name}': {e}")
#             return False

#     def _handle_sweet_alert(self, button_text, timeout=5):
#         """Handles SweetAlert2 confirmation pop-ups (Yes/OK)."""
#         try:
#             print(f"Waiting for SweetAlert '{button_text}' button…")
#             btn = WebDriverWait(self.driver, timeout).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
#             )
#             btn.click()
#             print(f"Clicked SweetAlert '{button_text}'.")
#             time.sleep(1.0)
#             return True
#         except TimeoutException:
#             print(f"SweetAlert '{button_text}' did not appear or was not clickable; continuing.")
#             return False
#         except Exception as e:
#             print(f"Error handling SweetAlert '{button_text}': {e}")
#             return False

#     # --- Step Functions for Automation Flow ---

#     def _perform_login(self):
#         """Performs the login sequence."""
#         print("--- (A) Initiating Login Flow ---")
#         self._wait_for_page_load()

#         self._fill_input_field((By.ID, "state_list"), self.state_name, "State dropdown")
#         self._fill_input_field((By.ID, "user_id"), self.username, "Username field")
#         self._fill_input_field((By.ID, "password"), self.password, "Password field")

#         print("\n*** ACTION REQUIRED: Please select State & enter Captcha in the browser within 20 seconds. ***")
#         time.sleep(20) # Manual intervention for captcha
#         print("Resuming automation…")
#         self._wait_for_page_load() # Wait for any post-captcha load

#         if not self._click_element((By.ID, "Procced"), "Login 'Procced' button", use_js_click=True):
#             raise Exception("Failed to click Procced button, login likely failed.")

#         WebDriverWait(self.driver, 30).until(EC.url_contains("MenuScreen.jsp"))
#         WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Phase II")))
#         print("Successfully logged in.")

#     def _navigate_to_data_entry(self):
#         """Navigates to the Data Entry Screen."""
#         print("\n--- (B1) Navigating to Data Entry Screen ---")
#         self._click_element((By.LINK_TEXT, "Phase II"), "Phase II link")
#         self._click_element((By.LINK_TEXT, "Data Entry Screen (Schedule wise)"), "Data Entry Screen link")
#         WebDriverWait(self.driver, 20).until(EC.url_contains("Schedule_H.jsp"))
#         print("Reached 'Schedule_H.jsp' (Data Entry Screen).")

#     def _select_village(self):
#         """Selects the village from the dropdown."""
#         print(f"\n--- (B2) Selecting Village: {self.village_name} ---")
#         try:
#             village_dropdown_element = WebDriverWait(self.driver, 15).until(
#                 EC.presence_of_element_located((By.NAME, "vlg_list"))
#             )
#             select = Select(village_dropdown_element)
#             select.select_by_visible_text(self.village_name)
#             print(f"→ Village '{self.village_name}' selected.")
#             time.sleep(1)
#             return True
#         except NoSuchElementException:
#             print(f"Error: Village dropdown 'vlg_list' not found.")
#             return False
#         except TimeoutException:
#             print(f"Error: Village dropdown 'vlg_list' not present within timeout.")
#             return False
#         except Exception as e:
#             print(f"Error selecting village '{self.village_name}': {e}")
#             return False

#     def _count_farmers_in_popup(self):
#         """Opens the pop-up, counts farmers, and closes it."""
#         print("\n--- (C) Counting Total Farmers in Pop-up ---")
#         self.original_window = self.driver.current_window_handle # Store main window handle

#         if not self._click_element((By.XPATH, "//button[contains(text(), 'Schedules(Ph.-I)')] | //input[@type='button' and @value='Schedules(Ph.-I)']"), "Schedules(Ph.-I) button"):
#             return 0

#         # Switch to pop-up window
#         WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(2))
#         popup_window = None
#         for handle in self.driver.window_handles:
#             if handle != self.original_window:
#                 popup_window = handle
#                 self.driver.switch_to.window(popup_window)
#                 break
#         if not popup_window:
#             print("Error: Pop-up window did not appear.")
#             return 0

#         try:
#             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='myTable']")))
#             all_rows = self.driver.find_elements(By.XPATH, "//table[@id='myTable']/tbody/tr")
#             num_farmers = len(all_rows) - 1  # Subtract header row
#             print(f"Found {num_farmers} farmers to process in the pop-up.")
#         except TimeoutException:
#             print("Error: Farmer table in pop-up not found within timeout.")
#             num_farmers = 0
#         except Exception as e:
#             print(f"Error counting farmers: {e}")
#             num_farmers = 0
#         finally:
#             self.driver.close() # Close pop-up
#             self.driver.switch_to.window(self.original_window) # Switch back to main
#             time.sleep(1)

#         return num_farmers

#     def _process_single_farmer(self):
#         """
#         Processes a single farmer entry by opening the pop-up, extracting data,
#         clicking the checkbox, and filling the main form.
#         Assumes the driver is currently on the main data entry page.
#         """
#         print("\n--- (D.1) Re-opening Schedules Pop-up ---")
#         if not self._click_element((By.XPATH, "//button[contains(text(), 'Schedules(Ph.-I)')] | //input[@type='button' and @value='Schedules(Ph.-I)']"), "Schedules(Ph.-I) button"):
#             return 0.0 # Indicate failure to open pop-up

#         # Switch to pop-up window
#         WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(2))
#         popup_window = None
#         for handle in self.driver.window_handles:
#             if handle != self.original_window:
#                 popup_window = handle
#                 self.driver.switch_to.window(popup_window)
#                 break
#         if not popup_window:
#             print("Error: Pop-up window did not appear after re-opening.")
#             return 0.0

#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='myTable']")))

#         # (D.2) Extract “Area Operated” from row 2, column 5
#         area_xpath = "//table[@id='myTable']/tbody/tr[2]/td[5]"
#         extracted_area_value = 0.0
#         try:
#             area_cell = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, area_xpath)))
#             extracted_area_str = area_cell.text.strip()
#             extracted_area_value = float(extracted_area_str)
#             print(f"→ Extracted Area Operated = {extracted_area_value:.4f}")
#         except Exception as e:
#             print(f"Could not extract Area Operated from pop-up or convert to float: {e}")

#         # (D.3) Click the checkbox in row[2]
#         checkbox_xpath = "//table[@id='myTable']/tbody/tr[2]//input[@type='checkbox']"
#         try:
#             checkbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
#             checkbox.click()
#             print("→ Farmer selected by clicking checkbox.")
#         except Exception as e:
#             print(f"Could not click farmer checkbox in pop-up: {e}")
#             # If checkbox fails, we can't proceed, so set area to 0 to skip main form fill
#             extracted_area_value = 0.0

#         # Pop-up closes automatically → switch back to main window
#         self.driver.switch_to.window(self.original_window)
#         WebDriverWait(self.driver, 10).until(EC.url_contains("Schedule_H.jsp"))
#         print("Switched back to main data entry form.")

#         return extracted_area_value

#     def _calculate_fallow_and_real_area(self, extracted_area):
#         """Calculates fallow area and then the real area to be filled."""
#         fallow_area_value = 0.0
#         print("Calculating fallow area from fields 05-15...")
#         for i in range(5, 16):
#             field_name = f"field_{i:02d}"
#             try:
#                 fallow_field = WebDriverWait(self.driver, 2).until( # Shorter wait here
#                     EC.presence_of_element_located((By.NAME, field_name))
#                 )
#                 field_value_str = fallow_field.get_attribute("value").strip()
#                 if field_value_str:
#                     fallow_area_value += float(field_value_str)
#                 # print(f"   Fetched {field_name}: {field_value_str}. Current fallow_area_value: {fallow_area_value:.4f}")
#             except TimeoutException:
#                 # print(f"   {field_name} not found or not visible; skipping for fallow area calculation.")
#                 pass # It's normal for some fields to be empty
#             except ValueError:
#                 print(f"   Warning: Could not convert value of {field_name} ('{field_value_str}') to float; skipping.")
#             except Exception as e:
#                 print(f"   An error occurred while fetching {field_name} for fallow area: {e}")

#         print(f"Total calculated fallow_area_value: {fallow_area_value:.4f}")
#         return extracted_area - fallow_area_value

#     def _fill_block_c_and_d(self, total_area_to_fill):
#         """Fills Block C and D fields based on the calculated area."""
#         formatted_full_area = f"{total_area_to_fill:.4f}"
#         print("--- Filling Block C (Net Irrigated Area) ---")
#         if not self._fill_input_field((By.NAME, "field_05"), formatted_full_area, "Net Irrigated Area (field_05)"):
#             print("Skipping Block D due to field_05 error.")
#             return

#         # Check for and fill "Number of Crops"
#         got_crops_field = False
#         try:
#             crops_field = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.NAME, "tot_crops"))
#             )
#             got_crops_field = True
#         except TimeoutException:
#             try: # Fallback XPath
#                 crops_field = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//td[contains(normalize-space(text()), 'Number of Crops grown during the reference year')]/following-sibling::td//input"))
#                 )
#                 got_crops_field = True
#             except:
#                 pass # Still not found

#         if got_crops_field:
#             if not self._fill_input_field((By.NAME, "tot_crops"), "3", "Number of Crops (tot_crops)"):
#                 print("Skipping Block D due to tot_crops error.")
#                 got_crops_field = False
#         else:
#             print("Number of Crops field not found; skipping Block D.")

#         # Fill Block D only if crops field was successfully found and filled
#         if got_crops_field and total_area_to_fill > 0.0:
#             print("--- Filling Block D (Crop Details) ---")
#             half_area = total_area_to_fill / 2.0
#             formatted_half_area = f"{half_area:.4f}"
#             print(f"Split Area: Full={formatted_full_area}, Half={formatted_half_area}")

#             # Row 1: cr_code_10 & unirri_ar_10 (Full area)
#             self._fill_input_field((By.NAME, "cr_code_10"), "1009", "Crop Code 1", tab_after=False)
#             self._fill_input_field((By.NAME, "unirri_ar_10"), formatted_full_area, "Unirrigated Area 1")

#             # Row 2: cr_code_11 & irri_ar_11 (Half area)
#             self._fill_input_field((By.NAME, "cr_code_11"), "201", "Crop Code 2", tab_after=False)
#             self._fill_input_field((By.NAME, "irri_ar_11"), formatted_half_area, "Irrigated Area 2")

#             # Row 3: cr_code_12 & irri_ar_12 (Half area)
#             self._fill_input_field((By.NAME, "cr_code_12"), "106", "Crop Code 3", tab_after=False)
#             self._fill_input_field((By.NAME, "irri_ar_12"), formatted_half_area, "Irrigated Area 3")
#             print("Block D rows filled.")
#         elif total_area_to_fill <= 0.0:
#             print("Skipping Block D (total area is 0 or less).")

#     def _fill_fallow_area(self, area_value):
#         """Fills field_06 for fallow area if extracted area is small."""
#         print(f"--- Handling Small Area (extracted area <= 0.10) ---")
#         formatted_value = f"{area_value:.4f}"
#         # This will be field_06 (Net Unirrigated Area) as per the original logic
#         if not self._fill_input_field((By.NAME, "field_06"), formatted_value, "Net Unirrigated Area (field_06)"):
#             print("Failed to set field_06 for small area.")

#     def _complete_entry_and_save(self):
#         """Fills source of irrigation, remarks, and saves the entry."""
#         print("\n--- (D.6) Completing Entry and Saving ---")
#         pick_list = ["2 - Wells", "3 - Tubewells", "5 - Others"]
#         chosen_source = random.choice(pick_list)

#         try:
#             src_sel_element = WebDriverWait(self.driver, 20).until(
#                 EC.element_to_be_clickable((By.NAME, "source_irr"))
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", src_sel_element)
#             select = Select(src_sel_element)
#             select.select_by_visible_text(chosen_source)
#             print(f"→ Source of Irrigation set to '{chosen_source}'")
#             time.sleep(0.5)
#         except Exception as e:
#             print(f"Could not set Source of Irrigation: {e}")

#         self._fill_input_field((By.NAME, "remarks"), "Ok", "Remarks field", tab_after=False)

#         if not self._click_element((By.XPATH, "//input[@type='button' and @value='Save'] | //button[normalize-space(text())='Save']"), "Save button"):
#             print("Failed to click Save button.")
#             return

#         # Handle SweetAlert2 pop-ups
#         self._handle_sweet_alert("Yes") # Confirmation dialog
#         self._handle_sweet_alert("OK")  # Success dialog

#     def run_automation(self):
#         """Executes the full automation sequence."""
#         try:
#             self.driver = setup_driver()
#             print(f"Navigating to: {self.website_url}")
#             self.driver.get(self.website_url)

#             self._perform_login()
#             self._navigate_to_data_entry()

#             if not self._select_village():
#                 print("Failed to select village, cannot proceed with farmer processing.")
#                 return

#             num_farmers_total = self._count_farmers_in_popup()
#             if num_farmers_total < 1:
#                 print("No farmers found for processing. Exiting.")
#                 return

#             # Loop through first 2 farmers as per original logic (range(0,2))
#             for i in range(0, 2):
#                 print(f"\n===== Processing farmer {i} =====")
#                 extracted_area = self._process_single_farmer()

#                 if extracted_area > 0.10:
#                     result_real_area = self._calculate_fallow_and_real_area(extracted_area)
#                     if result_real_area > 0:
#                         self._fill_block_c_and_d(result_real_area)
#                     else:
#                         print(f"Real area is 0 or less ({result_real_area:.4f}); skipping Block C and D.")
#                         self._fill_fallow_area(extracted_area) # If real area is zero, treat original as fallow
#                 else:
#                     self._fill_fallow_area(extracted_area)

#                 self._complete_entry_and_save()
#                 print(f"===== Finished processing farmer {i+1} =====")

#             print("\nAll specified farmers have been processed!")

#         except WebDriverException as e:
#             print(f"\n‼ WebDriver error: {e}")
#             print("Ensure ChromeDriver is compatible with your Chrome version and properly set up.")
#         except Exception as e:
#             print(f"\n‼ An unexpected error occurred: {e}")
#             import traceback
#             traceback.print_exc() # Print full traceback for debugging
#         finally:
#             print("\nScript complete. Press ENTER to close browser.")
#             if self.driver:
#                 try:
#                     input() # Keep browser open until user presses enter
#                     self.driver.quit()
#                 except:
#                     pass # Ignore errors if driver is already closed or input fails
#             print("Done.")

# # # Example Usage (replace with your actual data)
# # if __name__ == "__main__":
# #     # These would typically come from a config file or environment variables
# #     WEBSITE_URL = "http://your.agri.website.com/login" # Replace with actual URL
# #     STATE_NAME = "UTTAR PRADESH"
# #     USERNAME = "your_username"
# #     PASSWORD = "your_password"
# #     VILLAGE_NAME = "NAGLA KHEM (50005)" # Replace with actual village name

# #     automator = SeleniumAutomator(WEBSITE_URL, STATE_NAME, USERNAME, PASSWORD, VILLAGE_NAME)
# #     automator.run_automation()