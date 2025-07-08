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
from faker import Faker
import random

class Category(BasePage,unittest.TestCase):
    """
    Login common module for all user roles.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger("Category") 

    def test_something(self):
        self.assertTrue(True)

    def cat_tab(self):
        fake = Faker()
        self.click(Locators.CATEGORY_SIDEBAR)
        time.sleep(2)

    def test_create_new_category(self):
        self.click(Locators.NEW_CATEGORY_BUTTON)
        time.sleep(2)
        category_name = f"category {random.randint(100, 999)}"
        self.enter_text(Locators.CATEGORY_NAME_INPUT, category_name)
        time.sleep(1)
        self.click(Locators.EXPENSE_RADIO_BUTTON)
        time.sleep(1)
        self.click(Locators.SAVE_CATEGORY_BUTTON)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.info("Category created successfully!")
        except TimeoutException:
            self.fail("Category was not saved. 'Category Code' link not found.")
            
    def test_empty_category_name(self):
        self.click(Locators.NEW_CATEGORY_BUTTON)
        self.enter_text(Locators.CATEGORY_NAME_INPUT, "")
        self.click(Locators.SAVE_CATEGORY_BUTTON)
        
        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.error("Category is  not shown required message.")
            self.fail("Category was saved with an empty name. Expected an error message.")
        except TimeoutException:
            self.logger.warning("Category is showing required message.")
            self.click(Locators.BACK_CATEGORY)

    def test_category_name_whitespace_only(self):
        self.click(Locators.NEW_CATEGORY_BUTTON)
        self.enter_text(Locators.CATEGORY_NAME_INPUT, "     ")
        self.click(Locators.SAVE_CATEGORY_BUTTON)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.error("Category is  not shown required message on White space.")
            self.fail("Category was saved with whitespace only. Expected an error message.")
        except TimeoutException:
            self.logger.warning("Category is showing required message on white space.")
            self.click(Locators.BACK_CATEGORY)

    def test_invalid_category_name(self):
        category_name=f"Invalid@Name#123 {random.randint(100, 999)}"
        self.click(Locators.NEW_CATEGORY_BUTTON)
        self.enter_text(Locators.CATEGORY_NAME_INPUT, category_name)
        self.click(Locators.SAVE_CATEGORY_BUTTON)
        time.sleep(3)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.error("Category is  not shown Error message on Invalid Name.")
            print("Category is  not shown Error message on Invalid Name.")
            self.fail("Category was saved with invalid name. Expected an error message.")
            time.sleep(2)
        except TimeoutException:
            self.logger.warning("Category is showing Error message on Invalid Name.")
            self.click(Locators.BACK_CATEGORY)
            print("Category is showing Error message on Invalid Name.")
            time.sleep(2)
            

    def test_duplicate_category_name(self):
    
        existing_name = "GROCERIES"

        # First insert
        self.click(Locators.NEW_CATEGORY_BUTTON)
        self.enter_text(Locators.CATEGORY_NAME_INPUT, existing_name)
        self.click(Locators.EXPENSE_RADIO_BUTTON)
        self.click(Locators.SAVE_CATEGORY_BUTTON)
        time.sleep(2)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.error("Allready Existing category is adding Again")
            self.fail("Duplicate category name was accepted when it should not have been.")
        except TimeoutException:
            self.logger.warning("Allready Existing category is not adding Again, showing required message.")
            self.click(Locators.BACK_CATEGORY)
 

    def test_long_category_name(self):
        long_name = "A" * 300  # Exceeds typical limits
        print("ime")
        self.logger.info(f"Testing with long category name of length {len(long_name)}")

        self.click(Locators.NEW_CATEGORY_BUTTON)
        self.enter_text(Locators.CATEGORY_NAME_INPUT, long_name)
        self.click(Locators.EXPENSE_RADIO_BUTTON)
        self.click(Locators.SAVE_CATEGORY_BUTTON)
        print("ime")

        time.sleep(2)  # Optional: Add wait if necessary for UI update

        try:
            # Check if long name appears in the category list
            created_name = self.get_text((By.XPATH, "//table//tr[1]/td[1]"))  # Update locator if needed

            if long_name in created_name:
                self.logger.error("Above 250 chars is incorrectly accepted in the category field.")
                self.fail("Long category name was accepted when it should not have been.")
            else:
                self.logger.warning("Above 250 characters not accepted in the category field as expected.")

        except Exception as e:
            # If element is not found or text is different
            self.logger.warning("Above 250 characters not accepted, exception raised or not found in table.")
            self.logger.debug(f"Exception details: {e}")
            self.click(Locators.BACK_CATEGORY)
            time.sleep(2)

    def test_edit_category(self):
        # Edit "Food" to "Travel"
        category_name = f"Categry {random.randint(100,999)}"
        self.click(Locators.EDIT_CATEGORY_BUTTON)
        self.clear(Locators.EDIT_CATEGORY_NAME_INPUT)
        self.enter_text(Locators.EDIT_CATEGORY_NAME_INPUT, category_name)
        self.click(Locators.UPDATE_CATEGORY_BUTTON)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.info("Category updated successfully.")
        except TimeoutException:
            self.fail("Category was not updated. 'Category Code'  not found.")



    def test_edit_category_empty_name(self):
        self.click(Locators.EDIT_CATEGORY_BUTTON)
        self.clear(Locators.EDIT_CATEGORY_NAME_INPUT)
        self.click(Locators.UPDATE_CATEGORY_BUTTON)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.error("Category is  not shown required message.")
            self.fail("Category was updated to an empty name. Expected an error message.")  
        except TimeoutException:
            self.logger.warning("Category is showing required message.")
            self.click(Locators.BACK_CATEGORY)

    def test_edit_to_duplicate_category_name(self):

        # Edit "Food" to "Travel"
        self.click(Locators.EDIT_CATEGORY_BUTTON)
        self.clear(Locators.EDIT_CATEGORY_NAME_INPUT)
        self.enter_text(Locators.EDIT_CATEGORY_NAME_INPUT, "Dummy")
        self.click(Locators.UPDATE_CATEGORY_BUTTON)

        try:
            category_saved = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(Locators.CATEGORY_CODE_LINK)
            )
            self.assertTrue(category_saved.is_displayed())
            self.logger.error("Allready Existing category is adding Again during edit")
            self.fail("Duplicate category name was accepted when it should not have been.")
        except TimeoutException:
            self.logger.warning("Allready Existing category is not adding Again, showing required message during Edit.")
            self.click(Locators.BACK_CATEGORY)
    def delete_category_and_verify(self):
        self.click(Locators.DELETE_BUTTON)
        time.sleep(1)
        self.click(Locators.DELETE_CONFIRM_BUTTON)

        toast_message = "Category deleted successfully"
        toast_locator = (By.XPATH, f"//*[contains(text(), '{toast_message}')]")

        try:
            # Try to get the toast immediately with low wait time
            toast = WebDriverWait(self.driver, 1, poll_frequency=0.1).until(
                EC.presence_of_element_located(toast_locator)
            )
            toast_text = toast.text.strip()
            self.assertIn("deleted successfully", toast_text)
            print(f"[INFO] Toast text found: '{toast_text}'")
            self.logger.info(f"Toast found: {toast_text}")

        except Exception:
            # If not visible, fallback to page source check
            print("[WARNING] Toast not found in WebDriverWait, checking page source...")

            html_snapshot = self.driver.page_source
            if toast_message in html_snapshot:
                print("[INFO] Toast message found in page source!")
                self.logger.info("Toast message found in page source.")
            else:
                self.driver.save_screenshot("category_delete_failed.png")
                self.logger.error("Category deletion toast not found.")
                self.fail("Toast message not found — category deletion failed.")

    def snackbar_add_category(self):
        self.click(Locators.NEW_CATEGORY_BUTTON)
        time.sleep(2)
        category_name = f"category {random.randint(100, 999)}"
        self.enter_text(Locators.CATEGORY_NAME_INPUT, category_name)
        time.sleep(1)
        self.click(Locators.EXPENSE_RADIO_BUTTON)
        time.sleep(1)
        self.click(Locators.SAVE_CATEGORY_BUTTON)
        try:
            # Wait for the snackbar to appear (short lifespan)
            toast_locator = (By.XPATH, "//div[contains(text(),'Category') and contains(text(),'successfully')]")
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(toast_locator)
            )
            toast_text = toast.text
            self.logger.info(f"Snackbar message displayed: {toast_text}")
            print(toast_text, "snackbar msg")

            self.assertIn("Category", toast_text)
            self.assertIn("successfully", toast_text)

        except TimeoutException:
            self.logger.error("Snackbar message not displayed after adding category.")
            self.driver.save_screenshot("category_add_snackbar_failed.png")
            self.fail("Snackbar message not displayed after adding category.")

            
        except Exception:
            self.logger.error("Category save failed or toast message not found.")
            # Optional: take screenshot
            self.driver.save_screenshot("category_save_failed.png")
            self.fail("Category save failed or toast message not found.")   
 
    def snackbar_edit_category(self):
        # Edit "Food" to "Travel"
        category_name = f"Category {random.randint(100,999)}"
        self.click(Locators.EDIT_CATEGORY_BUTTON)
        self.clear(Locators.EDIT_CATEGORY_NAME_INPUT)
        self.enter_text(Locators.EDIT_CATEGORY_NAME_INPUT, category_name)
        self.click(Locators.UPDATE_CATEGORY_BUTTON)

        try:
            # Update the locator based on your HTML structure. Adjust class if needed.
            toast_locator = (By.XPATH, "//div[contains(text(),'Category') and contains(text(),'successfully')]")

            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(toast_locator)
            )

            toast_text = toast.text
            self.logger.info(f"Snackbar message displayed: {toast_text}")
            print(toast_text, "snackbar msg")

            self.assertIn("Category", toast_text)
            self.assertIn("successfully", toast_text)

        except TimeoutException:
            self.logger.error("Snackbar message not displayed after Updating category.")
            self.driver.save_screenshot("category_edit_snackbar_failed_.png")
            self.fail("Snackbar message not displayed after Editing category.")

