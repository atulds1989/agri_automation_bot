# agri_entry_bot/utilities/automation_helper.py

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
from utilities.driver_helper import setup_driver

class AutomationHelper:
    def __init__(self, website_url, state_name, username, password, village_name):
        self.website_url = website_url
        self.state_name = state_name
        self.username = username
        self.password = password
        self.village_name = village_name

    # --- Main Script Logic ---
    def run_automation(self):
        driver = None
        try:
            driver = setup_driver()
            print(f"Navigating to: {self.website_url}")
            driver.get(self.website_url)

            # --- (A) LOGIN FLOW ---
            print("Waiting for login page to load…")
            WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(1)

            print("Filling State from state list")
            statename_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "state_list")))
            statename_field.send_keys(self.state_name)

            print("Filling username…")
            username_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user_id")))
            username_field.send_keys(self.username)

            print("Filling password…")
            password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "password")))
            password_field.send_keys(self.password)

            print("\n--- ACTION REQUIRED: Select State & enter Captcha in the browser. ---")
            time.sleep(20)
            print("Resuming… Clicking Procced…")
            WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
            login_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "Procced")))
            driver.execute_script("arguments[0].click();", login_btn)
            time.sleep(1)

            print("Waiting for main menu to load…")
            WebDriverWait(driver, 30).until(EC.url_contains("MenuScreen.jsp"))
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Phase II")))
            print("Logged in.")

            # --- (B1) NAVIGATE TO DATA ENTRY SCREEN ---
            print("Clicking Phase II…")
            phase_ii_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Phase II")))
            phase_ii_link.click()
            time.sleep(2)

            print("Clicking Data Entry Screen (Schedule wise)…")
            data_entry_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.LINK_TEXT, "Data Entry Screen (Schedule wise)")))
            data_entry_link.click()
            WebDriverWait(driver, 20).until(EC.url_contains("Schedule_H.jsp"))
            time.sleep(2)
            print("On Schedule_H.jsp.")

            # --- (B2) SELECT VILLAGE NAME FROM BLOCK A ---
            print(f"Selecting Village: {self.village_name}")
            # try:
            #     village_dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "vlg_list")))
            #     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", village_dropdown)
            #     village_dropdown.click()
            #     time.sleep(0.5)
            #     village_dropdown.find_element(By.XPATH, f".//option[normalize-space(text())='{VILLAGE_NAME}']").click()
            #     print(f"→ source_irri set to '{VILLAGE_NAME}'")
            # except Exception as e:
            #     print(f"Could not set Source of Irrigation: {e}")
                
            village_dropdown = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "vlg_list")))
            select_village = Select(village_dropdown)
            select_village.select_by_visible_text(self.village_name)
            time.sleep(1)  # wait briefly after selection

            # --- (C) COUNT HOW MANY FARMERS ARE IN THE POP‐UP (ONCE) ---
            original_window = driver.current_window_handle
            print("\nCounting total farmers in the pop-up…")

            # Open the pop-up
            schedules_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(text(), 'Schedules(Ph.-I)')] | //input[@type='button' and @value='Schedules(Ph.-I)']"
                ))
            )

            schedules_button.click()

            # Switch to pop-up window
            WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
            for handle in driver.window_handles:
                if handle != original_window:
                    popup_window = handle
                    driver.switch_to.window(popup_window)
                    break

            # Wait for the table and count rows
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='myTable']")))
            all_rows = driver.find_elements(By.XPATH, "//table[@id='myTable']/tbody/tr")
            num_farmers = len(all_rows) - 1  # subtract header row
            print(f"Found {num_farmers} farmers to process.")

            # Close pop-up and return
            driver.close()
            driver.switch_to.window(original_window)
            time.sleep(1)

            if num_farmers < 1:
                print("No farmers found. Exiting.")
                return

            # --- (D) LOOP THROUGH EACH FARMER, ALWAYS TARGETING tr[2] ---
            for idx in range(0, 2):
                print(f"\n===== Processing farmer {idx+1} of {2} =====")

                # (D.1) Re-open the “Schedules(Ph.-I)” pop-up
                schedules_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(text(), 'Schedules(Ph.-I)')] | //input[@type='button' and @value='Schedules(Ph.-I)']"
                    ))
                )
                schedules_button.click()

                # Switch to pop-up window
                WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
                for handle in driver.window_handles:
                    if handle != original_window:
                        popup_window = handle
                        driver.switch_to.window(popup_window)
                        break

                # Wait for table to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='myTable']")))

                # (D.2) Extract “Area Operated” from row 2, column 5
                area_xpath = "//table[@id='myTable']/tbody/tr[2]/td[5]"
                print("Extracting Area Operated from the first data row…")
                extracted_area_value = 0.0
                try:
                    area_cell = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, area_xpath)))
                    extracted_area_str = area_cell.text.strip()
                    extracted_area_value = float(extracted_area_str)
                except Exception as e:
                    print(f"Could not extract Area Operated or convert to float: {e}")
                    extracted_area_value = 0.0
                print(f"→ Extracted Area = {extracted_area_value:.4f}")

                # (D.3) Click the checkbox in row[2]
                checkbox_xpath = "//table[@id='myTable']/tbody/tr[2]//input[@type='checkbox']"
                print("Clicking checkbox for that farmer…")
                try:
                    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
                    checkbox.click()
                    print("Farmer selected.")
                except Exception as e:
                    print(f"Could not click farmer checkbox: {e}")

                # Pop-up closes automatically → switch back to main window
                driver.switch_to.window(original_window)
                WebDriverWait(driver, 10).until(EC.url_contains("Schedule_H.jsp"))
                print("Switched back to main data entry form.")

                # --- Calculate fallow_area_value BEFORE using extracted_area_value for total_area ---
                fallow_area_value = 0.0
                # Iterate through field_05 to field_15 to sum their values for fallow_area_value
                for i in range(5, 16): # This loop goes from 5 to 15 (inclusive)
                    field_name = f"field_{i:02d}" # Formats as field_05, field_06, etc.
                    try:
                        fallow_field = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.NAME, field_name))
                        )
                        field_value_str = fallow_field.get_attribute("value").strip()
                        if field_value_str:
                            fallow_area_value += float(field_value_str)
                        print(f"  Fetched {field_name}: {field_value_str}. Current fallow_area_value: {fallow_area_value:.4f}")
                    except TimeoutException:
                        print(f"  {field_name} not found or not visible; skipping for fallow area calculation.")
                    except ValueError:
                        print(f"  Could not convert value of {field_name} ('{field_value_str}') to float; skipping.")
                    except Exception as e:
                        print(f"  An error occurred while fetching {field_name}: {e}")

                print(f"Total calculated fallow_area_value: {fallow_area_value:.4f}")

                # Calculate result_real_area
                result_real_area = extracted_area_value - fallow_area_value
                print(f"Calculated result_real_area (extracted_area_value - fallow_area_value): {result_real_area:.4f}")

                # Now, use result_real_area for your total_area for filling Block C
                total_area = result_real_area # Use the corrected area
                formatted_full = f"{total_area:.4f}"

                # (D.4) BLOCK C → fill field_05, field_06, tot_crops
                print("--- Filling Block C ---")

                # 04. Net Irrigated Area → field_05 (This field is now overwritten based on result_real_area)
                try:
                    field05 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "field_05")))
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field05)
                    field05.clear()
                    field05.send_keys(formatted_full)
                    field05.send_keys(Keys.TAB)
                    time.sleep(0.5)
                    print(f"→ field_05 set to {formatted_full}")
                except Exception as e:
                    print(f"Could not set field_05: {e}")

                # # 05. Net Unirrigated Area → field_06 = "0.0000"
                # try:
                #     field06 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "field_06")))
                #     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field06)
                #     field06.clear()
                #     field06.send_keys("0.0000")
                #     field06.send_keys(Keys.TAB)
                #     time.sleep(0.5)
                #     print("→ field_06 set to 0.0000")
                # except:
                #     print("field_06 not found; skipping")

                # Number of Crops → tot_crops = "3"
                got_crops = False
                try:
                    crops_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "tot_crops")))
                    got_crops = True
                except TimeoutException:
                    try:
                        crops_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.XPATH,
                            "//td[contains(normalize-space(text()), 'Number of Crops grown during the reference year')]/following-sibling::td//input"
                        )))
                        got_crops = True
                    except:
                        got_crops = False

                if got_crops:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", crops_field)
                        crops_field.clear()
                        crops_field.send_keys("3")
                        crops_field.send_keys(Keys.TAB)
                        time.sleep(0.5)
                        print("→ tot_crops set to 3")
                    except Exception as e:
                        print(f"Could not fill tot_crops: {e}")
                        got_crops = False
                else:
                    print("Number of Crops field not found; skipping Block D")

                # # (D.5) BLOCK D → only if got_crops True AND total_area > 0.0
                # if got_crops and total_area > 0.0:
                #     print("--- Filling Block D ---")
                    # first_half_area = np.round(total_area / 2.0)
                    # second_half_area = np.round(total_area - first_half_area)

                    # print(f"total area : {total_area:4f}, Calculated first_half_area: {first_half_area:.4f},\
                    #        second_half_area: {second_half_area:.4f}")
                    
                    # first_formatted_half = f"{first_half_area:.4f}"
                    # second_formatted_half = f"{first_half_area:.4f}"

                # (D.5) BLOCK D → only if got_crops True AND total_area > 0.0
                if got_crops and total_area > 0.0:
                    print("--- Filling Block D ---")
                    half_area = total_area / 2.0
                    formatted_half = f"{half_area:.4f}"

                    print(f"total area : {total_area:4f}, Calculated first_half_area: {half_area:.4f}")
                    
                    # Row 1: cr_code_10 & unirri_ar_10
                    try:
                        code1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "cr_code_10")))
                        unirri1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "unirri_ar_10")))
                        code1.clear()
                        code1.send_keys("1009")
                        unirri1.clear()
                        unirri1.send_keys(formatted_full)
                        unirri1.send_keys(Keys.TAB)
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Could not fill Block D row 1: {e}")

                    # Row 2: cr_code_11 & irri_ar_11
                    try:
                        code2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "cr_code_11")))
                        irr2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "irri_ar_11")))
                        code2.clear()
                        code2.send_keys("201")
                        irr2.clear()
                        irr2.send_keys(formatted_half)
                        irr2.send_keys(Keys.TAB)
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Could not fill Block D row 2: {e}")

                    # Row 3: cr_code_12 & irri_ar_12
                    try:
                        code3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "cr_code_12")))
                        irr3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "irri_ar_12")))
                        code3.clear()
                        code3.send_keys("106")
                        irr3.clear()
                        irr3.send_keys(formatted_half)
                        irr3.send_keys(Keys.TAB)
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"Could not fill Block D row 3: {e}")

                    print("Block D rows filled.\n")
                else:
                    print("Skipping Block D (no Crops or missing field).\n")

                # (D.6) SOURCE OF IRRIGATION → Random pick, fill Remarks, then Save → SweetAlert2 pop-ups
                pick_list = ["2 - Wells", "3 - Tubewells", "5 - Others"]
                pick = random.choice(pick_list)
                try:
                    src_sel = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "source_irr")))
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", src_sel)
                    src_sel.click()
                    time.sleep(0.5)
                    src_sel.find_element(By.XPATH, f".//option[normalize-space(text())='{pick}']").click()
                    print(f"→ source_irri set to '{pick}'")
                except Exception as e:
                    print(f"Could not set Source of Irrigation: {e}")
                time.sleep(0.5)

                try:
                    # field05 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "field_05")))
                    # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field05)

                    rem = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((
                            By.NAME,
                            "remarks"
                        ))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", rem)
                    rem.clear()
                    rem.send_keys("Ok")
                    time.sleep(1.0)
                    print("→ Remarks filled.")
                except:
                    print("Remarks field not found; skipping")

                # Click “Save”
                try:
                    save_b = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//input[@type='button' and @value='Save'] | //button[normalize-space(text())='Save']"
                        ))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_b)
                    save_b.click()
                    time.sleep(1.0)
                except Exception as e:
                    print(f"Could not click Save: {e}")

                # SweetAlert2 “Yes”
                try:
                    print("Waiting for Yes…")
                    yes_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
                    )
                    yes_btn.click()
                    time.sleep(1.0)
                    print("Clicked Yes.")
                except:
                    print("No Yes appeared; moving on…")

                # SweetAlert2 “OK”
                try:
                    print("Waiting for OK…")
                    ok_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
                    )
                    ok_btn.click()
                    time.sleep(2.0)
                    print("Clicked OK. Record saved.\n")
                except:
                    print("No OK appeared; assuming success.\n")

            # End of for-loop
            print("\nAll farmers have been processed!")

        except Exception as e:
            print(f"\n‼ Unhandled exception: {e}")
            if driver:
                print("Browser remains open for inspection. Press ENTER to close.")
                input()
                driver.quit()

        finally:
            print("\nScript complete. Press ENTER to close browser.")
            if driver:
                try:
                    input()
                    driver.quit()
                except:
                    pass
            print("Done.")