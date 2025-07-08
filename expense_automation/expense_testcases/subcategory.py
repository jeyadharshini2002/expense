import unittest
import time
from logger_file import get_logger
from locators import Locators
from selenium.webdriver.support.ui import WebDriverWait
from base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import random
import logging


class SubCategory(BasePage,unittest.TestCase):
    """
    Login common module for all user roles.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger("Sub Category") 
        
    def test_something(self):
        self.assertTrue(True)
        
    def sub_tab(self):
        fake = Faker()
        self.click(Locators.SUBCATEGORY_SIDEBAR)
        time.sleep(2)

    def test_create_new_subcategory(self):
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)

        # Select a valid category
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)
        subcategory_name = f"SubCategory {random.randint(100,999)}"
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, subcategory_name)
        time.sleep(1)
        
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)
        time.sleep(2)
        
        try:
            subcategory_save=WebDriverWait(self.driver,10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK)
            )
            
            self.assertTrue(subcategory_save.is_displayed())
            self.logger.info("SubCategory saved successfully.")

        except TimeoutException:
            self.fail("SubCategory was not saved. 'Subcategory Code' link not found.")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)

    def test_empty_subcategory_name(self):
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, "")
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)
        
        try:
            subcategory_saved=WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK_TEXT)
            )
            self.assertTrue(subcategory_saved.is_displayed())
            self.logger.error("SubCategory name  not shown required Message.")
            self.fail("SubCategory was saved with empty name. Expected an error message.")
        except TimeoutException:
            self.logger.warning("SubCategory name is showing required message.")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)


    def test_whitespace_subcategory_name(self):
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, "    ")
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)

        save_button_found = False
        code_link_found = False

        try:
            # ✅ Try to find the Save button (expected if validation worked)
            save_button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "(//button[normalize-space()='Save'])[1]"))
            )
            if save_button.is_displayed():
                save_button_found = True
                self.logger.warning("SubCategory correctly rejected whitespace-only name.")
                try:
                    self.click(Locators.SUBCATEGORY_BACK_BUTTON)
                    print("[INFO] Clicked subcategory back button.")
                    time.sleep(2)
                    return
                except Exception as e:
                    print(f"[WARNING] Subcategory back button not found or not clickable: {e}")
        except TimeoutException:
            print("[INFO] Save button not found — maybe validation did not work or page navigated.")

        try:
            # ✅ Try to detect if code link is visible (means it wrongly allowed the whitespace)
            code_link = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(Locators.SUBCATEGORY_CODE_LINK_TEXT)
            )
            if code_link.is_displayed():
                code_link_found = True
                self.logger.error("SubCategory allowed whitespace-only name — should have failed.")
                self.fail("SubCategory was saved with whitespace-only name. Expected an error message.")
        except TimeoutException:
            print("[INFO] Code link not visible — possible validation failure or page issue.")

        # ✅ Fallback: Neither save button nor code link found
        if not save_button_found and not code_link_found:
            print("[WARNING] Neither Save button nor Code link found. Trying JS-based back navigation...")
            try:
                self.driver.execute_script("window.history.go(-2)")
                time.sleep(2)
                print(f"[INFO] JS navigation complete. Current URL: {self.driver.current_url}")
                self.fail("the validation page not shown")
            except Exception as js_err:
                print(f"[ERROR] JS navigation failed: {js_err}")
                print("[INFO] Navigating directly to SubCategory list page as final fallback.")
                self.driver.get("https://dev.mehainfotech.com/expense-manager/SubCategory")
                self.fail("Failed to navigate back to SubCategory list page after whitespace-only name test.")
                time.sleep(2)

    def test_invalid_subcategory_name(self):
        subcategory_name=f"Invalid@Name#123 {random.randint(100, 999)}"
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, subcategory_name)
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)
        time.sleep(3)
        try:
            subcategory_saved=WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK_TEXT)
            )
            self.assertTrue(subcategory_saved.is_displayed())
            print("SubCategory is  not shown Error message on Invalid Name.")
            self.logger.error("SubCategory is not shown Error message on Invalid Name.")
            self.fail("Category was saved with invalid name. Expected an error message.")
            time.sleep(2)
        except TimeoutException:
            self.logger.warning("SubCategory is showing required message on Invalid Name.")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)
            time.sleep(2)
    def test_duplicate_subcategory_name(self):
        existing_subcategory_name = "Tablets"
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, existing_subcategory_name)
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)
        
        try:
            subcategory_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK_TEXT)
            )
            self.assertTrue(subcategory_saved.is_displayed())
            self.logger.error("SubCategory is not shown Error message on Duplicate Name.")
            self.fail ("SubCategory was saved with duplicate name. Expected an error message.")
        except TimeoutException:
            self.logger.warning("SubCategory is showing required message on Duplicate Name.")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)

    def test_subcategory_without_category(self):
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, "NoCategoryTest")
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)
    
        try:
            subcategory_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK_TEXT)
            )
            self.assertTrue(subcategory_saved.is_displayed())
            self.logger.error("SubCategory is not shown Error message when Category is not selected.")
            self.fail("SubCategory was saved without selecting a category. Expected an error message.")
        except TimeoutException:
            self.logger.warning("SubCategory is showing required message when Category is not selected.")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)

    def test_long_subcategory_name(self):
        long_name="A"* 256  # Assuming the limit is 255 characters
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, long_name)
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON) 
        try:
            # Check if long name appears in the sub  category list
            created_name = self.get_text((By.XPATH, "//table//tr[1]/td[1]"))  # Update locator if needed

            if long_name in created_name:
                self.logger.error("Above 250 chars is incorrectly accepted in the subcategory field.")
                self.fail("Long sub category name was accepted when it should not have been.")
            else:
                self.logger.warning("Above 250 characters not accepted in the subcategory field as expected.")

        except Exception as e:
            # If element is not found or text is different
            self.logger.warning("Above 250 characters not accepted, exception raised or not found in table.")
            self.logger.debug(f"Exception details: {e}")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)
            time.sleep(2)
           


    def test_edit_subcategory(self):
        self.click(Locators.SUBCATEGORY_EDIT_BUTTON)
        time.sleep(1)
        self.clear(Locators.SUBCATEGORY_EDIT_NAME_INPUT)
        new_name = f"UpdatedSubCat {random.randint(100,999)}"
        self.enter_text(Locators.SUBCATEGORY_EDIT_NAME_INPUT, new_name)
        self.click(Locators.SUBCATEGORY_UPDATE_BUTTON)
        time.sleep(2)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.info("SubCategory updated successfully.")
            
        except TimeoutException:
            self.fail("SubCategory was not updated. 'SubCategory Code'  not found.")

    def test_edit_subcategory_empty_name(self):
        self.click(Locators.SUBCATEGORY_EDIT_BUTTON)
        time.sleep(1)
        self.clear(Locators.SUBCATEGORY_EDIT_NAME_INPUT)
        self.click(Locators.SUBCATEGORY_UPDATE_BUTTON)

        try:
            subcategory_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.SUBCATEGORY_CODE_LINK)
            )
            self.assertTrue(subcategory_saved.is_displayed())
            self.logger.error("SubCategory is not shown required message on empty name.")
            self.fail("SubCategory was updated with empty name. Expected an error message.")
        except TimeoutException:
            self.logger.warning("SubCategory is showing required message on empty name.")
            self.click(Locators.SUBCATEGORY_BACK_BUTTON)

# edit duplication should only done by manual, system does not able to update disabled category, system 
# system doesnt know which is the duplicate subcategory

    def test_delete_subcategory(self):
        self.click(Locators.SUBCATEGORY_DELETE_BUTTON)
        time.sleep(1)
        self.click(Locators.SUBCATEGORY_DELETE_CONFIRM_BUTTON)
        self.logger.info("SubCategory delete button clicked.")
        
        try:
            toast_locator = (By.XPATH, "//*[contains(text(), 'Subcategory') and contains(text(), 'deleted successfully.')]")
            toast = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(toast_locator)
            )
            self.logger.info("SubCategory deleted successfully: Toast appeared.")
            self.assertIn("deleted successfully", toast.text)
            print(toast.text,"deleted msg")
            time.sleep(1)  # Allow visual confirmation if needed
        except Exception as e:
            self.logger.error("SubCategory deletion failed or toast not found.")
            self.driver.save_screenshot("subcategory_delete_failed.png")
            self.fail("SubCategory deletion failed or toast message not found.")

    def snackbar_add_subcategory(self):
        self.click(Locators.SUBCATEGORY_NEW_BUTTON)
        time.sleep(1)
        self.dropdown_click(Locators.SUBCATEGORY_CATEGORY, 1)

        subcategory_name = f"SnackbarSubCat {random.randint(100,999)}"      
        self.enter_text(Locators.SUBCATEGORY_NAME_INPUT, subcategory_name)
        self.click(Locators.SUBCATEGORY_SAVE_BUTTON)
        time.sleep(2)

        try:
            # Update the locator based on your HTML structure. Adjust class if needed.
            toast_locator = (By.XPATH, "//div[contains(text(),'Subcategory') and contains(text(),'successfully')]")

            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(toast_locator)
            )

            toast_text = toast.text
            self.logger.info(f"Snackbar message displayed: {toast_text}")
            print(toast_text, "snackbar msg")

            self.assertIn("Subcategory", toast_text)
            self.assertIn("successfully", toast_text)

        except TimeoutException:
            self.logger.error("Snackbar message not displayed after adding subcategory.")
            self.driver.save_screenshot("subcategory_add_snackbar_failed.png")
            self.fail("Snackbar message not displayed after adding subcategory.")

    def snackbar_edit_subcategory(self):
        self.click(Locators.SUBCATEGORY_EDIT_BUTTON)
        time.sleep(1)
        self.clear(Locators.SUBCATEGORY_EDIT_NAME_INPUT)
        new_name = f"UpdatedSubCat {random.randint(100,999)}"
        self.enter_text(Locators.SUBCATEGORY_EDIT_NAME_INPUT, new_name)
        self.click(Locators.SUBCATEGORY_UPDATE_BUTTON)
        time.sleep(2)


        try:
            # Update the locator based on your HTML structure. Adjust class if needed.
            toast_locator = (By.XPATH, "//div[contains(text(),'Subcategory') and contains(text(),'successfully')]")

            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(toast_locator)
            )

            toast_text = toast.text
            self.logger.info(f"Snackbar message displayed: {toast_text}")
            print(toast_text, "snackbar msg")

            self.assertIn("Subcategory", toast_text)
            self.assertIn("successfully", toast_text)

        except TimeoutException:
            self.logger.error("Snackbar message not displayed after Updating subcategory.")
            self.driver.save_screenshot("subcategory_edit_snackbar_failed_.png")
            self.fail("Snackbar message not displayed after Editing subcategory.")


        




