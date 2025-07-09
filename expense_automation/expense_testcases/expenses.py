import unittest
import time
from faker import Faker
from datetime import datetime
from datetime import date

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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
from selenium.common.exceptions import TimeoutException
class Expenses(BasePage,unittest.TestCase):
    """
    Login common module for all user roles.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger("Expenses") 

    def test_something(self):
        self.assertTrue(True)

    def expense_tab(self):
        fake = Faker()
        self.click(Locators.EXPENSE_SIDEBAR)
        time.sleep(2)
    def test_expense_search_functionality(self):
        self.click(Locators.EXPENSE_SEARCH)
        self.enter_text(Locators.EXPENSE_SEARCH, "water can")
        time.sleep(2)  # wait for result to populate

        try:
            search_result = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "(//td[contains(text(),'WATER CAN')])[1]"))
            )
            assert search_result.is_displayed()
            self.logger.info("Search functionality working. 'WATER CAN' found in results.")
        except Exception:
            self.driver.save_screenshot("expense_search_failed.png")
            self.logger.error("'WATER CAN' not found — search functionality failed.")
            self.fail("Search for 'water can' did not return expected result.")

    def test_valid_income_add(self):

        self.click(Locators.EXPENSES_ADD_INCOME_BT)

        fake = Faker()
        self.enter_text(
            Locators.EXPENSES_INCOME_DATE,
            fake.date_between_dates(date_start=datetime(1900, 1, 1), date_end=datetime(2020, 12, 31)).strftime("%m-%d-%Y")
        )
        self.dropdown_click(Locators.EXPENSES_INCOME_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSES_INCOME_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_INCOME_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_INCOME_NOTES, "Valid income")

        # Upload file
        try:
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )

            self.driver.execute_script("""
                arguments[0].style.display = 'block';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.opacity = 1;
            """, file_input)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.abspath(os.path.join(current_dir, "../screenshot.png"))

            if os.path.exists(file_path):
                file_input.send_keys(file_path)
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            self.driver.save_screenshot("file_upload_failed.png")
            self.fail(f"File input not found or upload failed: {e}")
        os.makedirs("screenshots", exist_ok=True)
        self.driver.save_screenshot("screenshots/before_save_click.png")

        # Click Save
        self.click(Locators.EXPENSES_INCOME_SAVE)
       
        self.driver.save_screenshot("screenshots/after_save_click.png")
        time.sleep(6)

        # Wait for and verify toast/snackbar
        try:
            toast = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Income saved successfully!')]"))
            )
            self.driver.save_screenshot("screenshots/Toast_visible.png")
            assert "Income saved successfully!" in toast.text
        except Exception as e:
            self.driver.save_screenshot("screenshots/Toast_notvisible.png")
            toasts = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Income saved successfully!')]")
            if any("Income saved successfully!" in t.text for t in toasts):
                print("Toast was present but not caught in wait.")
            else:
                self.fail(f"Toast not Came: {e}")


            
    def test_income_empty_required_fields_add(self):
        self.click(Locators.EXPENSES_INCOME_BACK)
        self.click(Locators.EXPENSES_ADD_INCOME_BT)
        self.click(Locators.EXPENSES_INCOME_SAVE)
        time.sleep(1)  # Give time for validations to show

        try:
            error = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'This field is required.')]"))
            )
            assert error.is_displayed()
            self.logger.info("Mandatory field validation message displayed correctly.")
            self.click(Locators.EXPENSES_INCOME_BACK)

        except Exception:
            self.driver.save_screenshot("required_field_validation_failed.png")
            self.logger.error("Mandatory field validation message not shown.")
            self.fail("There is no Mandatory Indication on income configuration.")
            self.click(Locators.EXPENSES_INCOME_BACK)
          



    def test_income_file_upload_invalid_type_add(self):
        
        fake = Faker()

        # Start filling the form
        self.click(Locators.EXPENSES_ADD_INCOME_BT)
        fake = Faker()
        self.enter_text(Locators.EXPENSES_INCOME_DATE, Faker().date_between_dates(date_start=datetime(2000, 1, 1), date_end=datetime(2020, 12, 31)).strftime("%m-%d-%Y"))
        self.dropdown_click(Locators.EXPENSES_INCOME_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSES_INCOME_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_INCOME_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_INCOME_NOTES, "Valid Expense")

        # Debug info for file inputs
        inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
        print("Found file inputs:", len(inputs))
        for i, el in enumerate(inputs):
            print(f"{i}: id={el.get_attribute('id')}, name={el.get_attribute('name')}")

        # Upload invalid file type
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )

        self.driver.execute_script("""
            arguments[0].style.display = 'block';
            arguments[0].style.visibility = 'visible';
            arguments[0].style.opacity = 1;
        """, file_input)

        file_path = r"C:/Users/admin/Desktop/Cucumber.xml"  # Invalid file type
        file_input.send_keys(file_path)

        # Submit form
        self.click(Locators.EXPENSES_INCOME_SAVE)
        time.sleep(2)

        try:
            # Try to find an error message related to file type
            error = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'invalid file')]"))
            )
            assert error.is_displayed(), "Error message not visible"
            self.logger.info("Correctly detected invalid file upload.")
        except TimeoutException:
            self.logger.warning("No invalid file error message not displayed.")
            self.fail("Invalid file upload did not show expected error message.")

        # # Always click Back (even if error not shown)
        # try:
        #     self.click(Locators.EXPENSES_INCOME_BACK)
        #     self.logger.info("Navigated back after invalid file upload attempt.")
        # except Exception as e:
        #     self.logger.error(f"Failed to click back button: {str(e)}")


    def test_income_snackbar_add(self):
        self.click(Locators.EXPENSES_INCOME_BACK)
        self.click(Locators.EXPENSES_ADD_INCOME_BT)
        fake = Faker()
        self.enter_text(Locators.EXPENSES_INCOME_DATE, Faker().date_between_dates(date_start=datetime(2000, 1, 1), date_end=datetime(2020, 12, 31)).strftime("%m-%d-%Y"))
        
        self.dropdown_click(Locators.EXPENSES_INCOME_CATEGORY,1)
        self.dropdown_click(Locators.EXPENSES_INCOME_SUBCATEGORY,1)
        self.enter_text(Locators.EXPENSES_INCOME_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_INCOME_NOTES, "snackbar test response")
        self.click(Locators.EXPENSES_INCOME_SAVE)
        time.sleep(2)  # Wait for the snackbar to appear
        try:
            # Update the locator based on your HTML structure. Adjust class if needed.
            toast_locator = (By.XPATH, "//div[contains(text(),'Income') and contains(text(),'successfully!')]")

            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(toast_locator)
            )

            toast_text = toast.text
            self.logger.info(f"Snackbar message displayed: {toast_text}")
            print(toast_text, "snackbar msg")

            self.assertIn("Income", toast_text)
            self.assertIn("successfully!", toast_text)
            self.click(Locators.EXPENSES_EXPENSE_BACK)

        except TimeoutException:
            self.logger.error("Snackbar message not displayed after adding Income.")
            self.driver.save_screenshot("Income_add_snackbar_failed.png")
            self.fail("Snackbar message not displayed after adding Income.")
            self.click(Locators.EXPENSES_INCOME_BACK)
    def income_invalid_date_add(self):
        
        self.click(Locators.EXPENSES_ADD_INCOME_BT)
        self.enter_text(Locators.EXPENSES_INCOME_DATE, "10-10-2026")
        self.dropdown_click(Locators.EXPENSES_INCOME_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSES_INCOME_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_INCOME_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_INCOME_NOTES, "Valid Expense")
        self.click(Locators.EXPENSES_INCOME_SAVE)
        time.sleep(2)

        try:
            error = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "(//span[@id='ExpenseDate-error'])[1]"))
            )
            assert error.is_displayed()
            self.logger.info("Correctly detected invalid date format.")
            # self.click(Locators.EXPENSES_INCOME_BACK)
           
        except Exception:
            self.driver.save_screenshot("invalid_date_error_not_displayed.png")
            self.logger.error("Invalid date format was accepted without showing an error.")
            self.fail("Invalid date format accepted and no error message shown.")
            # self.click(Locators.EXPENSES_INCOME_BACK)


    def test_valid_expense_add(self):
        self.click(Locators.EXPENSES_INCOME_BACK)
  
        self.click(Locators.EXPENSES_ADD_EXPENSE_BT) 
        fake = Faker()
        self.enter_text(Locators.EXPENSES_EXPENSE_DATE, Faker().date_between_dates(date_start=datetime(2000, 1, 1), date_end=datetime(2020, 12, 31)).strftime("%m-%d-%Y"))
        
        self.dropdown_click(Locators.EXPENSES_EXPENSE_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSE_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_EXPENSE_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_EXPENSE_NOTES, "Valid Expense")
        try:
            # Debug list of file inputs
            inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
            print("Found file inputs:", len(inputs))
            for i, el in enumerate(inputs):
                print(f"{i}: id={el.get_attribute('id')}, name={el.get_attribute('name')}")

            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))  # fallback generic
            )

            # Make it visible
            self.driver.execute_script("""
                arguments[0].style.display = 'block';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.opacity = 1;
            """, file_input)

            file_path = r"C:\Users\admin\Downloads\expense\expense\expense\expense_automation\screenshot.png"
            file_input.send_keys(file_path)


        except Exception as e:
            self.driver.save_screenshot("file_upload_failed.png")
            self.fail(f"File input not found or upload failed: {e}")
        time.sleep(3)
        self.click(Locators.EXPENSES_INCOME_SAVE)
        

        # try:
        #     toast = WebDriverWait(self.driver, 3).until(
        #         EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Expense saved successfully!')]"))
        #     )
        #     assert "Expense saved successfully!" in toast.text
        #     self.click(Locators.EXPENSES_INCOME_BACK)
        # except Exception as e:
        #     self.driver.save_screenshot("expense_save_failed.png")
        #     self.fail("Snackbar not found or message incorrect") 
        #     self.click(Locators.EXPENSES_INCOME_BACK)
            
    def test_expense_empty_required_fields_add(self):

        self.click(Locators.EXPENSES_EXPENSE_SAVE)
        time.sleep(1)
        try:
            error = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'This field is required.')]"))
            )
            assert error.is_displayed()
            self.logger.info("Mandatory field validation message displayed correctly.")
        except Exception:
            self.driver.save_screenshot("required_field_validation_failed.png")
            self.logger.error("Mandatory field validation message not shown.")
            self.fail("There is no Mandatory Indication on expense configuration.")
        finally:
            self.click(Locators.EXPENSES_EXPENSE_BACK)
    def test_expense_file_upload_invalid_type_add(self):

        
        self.click(Locators.EXPENSES_ADD_EXPENSE_BT)
        fake = Faker()
        self.enter_text(Locators.EXPENSES_EXPENSE_DATE, Faker().date_between(start_date=date(2000, 1, 1), end_date=date(2010, 1, 1)).strftime("%m-%d-%Y"))
        self.dropdown_click(Locators.EXPENSES_EXPENSE_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSE_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_EXPENSE_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_EXPENSE_NOTES, "invalid file upload")

         # Debug info for file inputs
        inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
        print("Found file inputs:", len(inputs))
        for i, el in enumerate(inputs):
            print(f"{i}: id={el.get_attribute('id')}, name={el.get_attribute('name')}")

        # Upload invalid file type
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )

        self.driver.execute_script("""
            arguments[0].style.display = 'block';
            arguments[0].style.visibility = 'visible';
            arguments[0].style.opacity = 1;
        """, file_input)

        file_path = r"C:/Users/admin/Desktop/Cucumber.xml"  # Invalid file type
        file_input.send_keys(file_path)

        # Submit form
        self.click(Locators.EXPENSES_EXPENSE_SAVE)
        time.sleep(2)


        try:
            # Wait to see if success message appears—this SHOULD NOT happen
            success_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Expense saved successfully!')]"))
            )
            if success_message.is_displayed():
                self.logger.error("Invalid file was uploaded and accepted without error.")
                self.driver.save_screenshot("invalid_file_upload.png")
                self.fail("Invalid file upload incorrectly triggered a success message.")
        except TimeoutException:
            self.logger.info("No success message appeared, which is expected for an invalid file.")
        # Always click Back, regardless of outcome
        # try:
        #     self.click(Locators.EXPENSES_EXPENSE_BACK)
        #     self.logger.info("Navigated back after invalid file upload attempt.")
        # except Exception as e:
        #     self.logger.error(f"Failed to click back button: {str(e)}")

        
       

    def test_expense_snackbar_add(self):
        self.click(Locators.EXPENSES_EXPENSE_BACK)
        
        self.click(Locators.EXPENSES_ADD_EXPENSE_BT)
        self.enter_text(Locators.EXPENSES_INCOME_DATE, Faker().date_between_dates(date_start=datetime(2000, 1, 1), date_end=datetime(2020, 12, 31)).strftime("%m-%d-%Y"))
        self.dropdown_click(Locators.EXPENSES_EXPENSE_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSE_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_EXPENSE_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_EXPENSE_NOTES, "Snackbar test expense")
        self.click(Locators.EXPENSES_EXPENSE_SAVE)
        time.sleep(2)  # Wait for the snackbar to appear
        try:
            # Update the locator based on your HTML structure. Adjust class if needed.
            toast_locator = (By.XPATH, "//div[contains(text(),'Expense') and contains(text(),'successfully!')]")

            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(toast_locator)
            )

            toast_text = toast.text
            self.logger.info(f"Snackbar message displayed: {toast_text}")
            print(toast_text, "snackbar msg")

            self.assertIn("Expense", toast_text)
            self.assertIn("successfully!", toast_text)

        except TimeoutException:
            self.logger.error("Snackbar message not displayed after adding Expense.")
            self.driver.save_screenshot("Expense_add_snackbar_failed.png")
            self.fail("Snackbar message not displayed after adding Expense.")
        # Always click Back, regardless of outcome
        # try:
        #     self.click(Locators.EXPENSES_EXPENSE_BACK)
        #     self.logger.info("Navigated back after invalid file upload attempt.")
        # except Exception as e:
        #     self.logger.error(f"Failed to click back button: {str(e)}")

 

    def expense_invalid_date_add(self):
        
        # self.click(Locators.EXPENSES_EXPENSE_BACK)
        time.sleep(5)
        print("Invalid date test")
        # self.click(Locators.EXPENSES_ADD_EXPENSE_BT)
        self.enter_text(Locators.EXPENSES_INCOME_DATE, Faker().date_between_dates(date_start=datetime(2025, 1, 1), date_end=datetime(2030, 12, 31)).strftime("%m-%d-%Y"))
        self.dropdown_click(Locators.EXPENSES_EXPENSE_CATEGORY, 1)
        self.dropdown_click(Locators.EXPENSE_SUBCATEGORY, 1)
        self.enter_text(Locators.EXPENSES_EXPENSE_AMOUNT, "1000")
        self.enter_text(Locators.EXPENSES_EXPENSE_NOTES, "invalid date add in expense")
        self.click(Locators.EXPENSES_EXPENSE_SAVE)
        time.sleep(3)

        try:
            error = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "(//span[@id='ExpenseDate-error'])[1]"))
            )
            assert error.is_displayed()
            self.logger.info("Correctly detected invalid date format.")

        except Exception:
            self.driver.save_screenshot("invalid_date_error_not_displayed.png")
            self.logger.error("Invalid date format was accepted without showing an error.")
            self.fail("Invalid date format accepted and no error message shown.")
        # try:
        #     self.click(Locators.EXPENSES_EXPENSE_BACK)
        #     self.logger.info("Navigated back after invalid date format.")
        # except Exception as e:
        #     self.logger.error(f"Failed to click back button: {str(e)}")
        #     self.driver.save_screenshot("expense_invalid_date_back_failed.png")
        #     self.fail("Failed to navigate back after invalid date format.")


    def test_expense_edit(self):
        self.click(Locators.EXPENSES_EXPENSE_BACK)
        
        self.click(Locators.EXPENSES_EDIT_BUTTON)
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.click(Locators.EXPENSE_1_EDIT)
        self.driver.execute_script("window.scrollBy(0,0);") 

        self.clear(Locators.EXPENSES_EDIT_AMOUNT)
        self.enter_text(Locators.EXPENSES_EDIT_AMOUNT, "1600")
        self.click(Locators.EXPENSES_EDIT_SAVE)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # Wait for toast first
        try:
            toast = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Expense updated successfully!')]"))
            )
            assert "Expense updated successfully!" in toast.text
            self.logger.info("Update toast appeared.")
        except Exception as e:
            self.driver.save_screenshot("expense_edit_failed.png")
            self.fail("Expense not updated or toast not shown.")

        # # Now try to go back using JS
        # try:
        #     time.sleep(1)  # wait for toast to fade
        #     self.driver.execute_script("window.history.go(-2);")
        #     time.sleep(2)  # wait for back to load
        #     self.logger.info("Navigated back using window.history.go(-2).")
        # except Exception as e:
        #     self.logger.error("JS history back failed: " + str(e))
        #     self.driver.save_screenshot("js_go_back_failed.png")
        #     self.fail("JS go(-2) failed.")

        # # Optional: verify you are back on the listing screen
        # try:
        #     WebDriverWait(self.driver, 5).until(
        #         EC.presence_of_element_located((By.XPATH, "//h4[contains(text(),'Expense List')]"))
        #     )
        #     self.logger.info("Returned to Expense List screen successfully.")
        # except:
        #     self.driver.save_screenshot("back_navigation_failed.png")
        #     self.fail("Not redirected to expense list after go back.")

    def test_expense_edit_empty_required_fields(self):
        # self.click(Locators.EXPENSES_EDIT_BUTTON)
        # time.sleep(2)
        # Scroll to bottom of the page
        self.click(Locators.EXPENSE_SIDEBAR)
        self.click(Locators.EXPENSES_EDIT_BUTTON)
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.click(Locators.EXPENSE_1_EDIT)
        self.driver.execute_script("window.scrollBy(0,0);") 

        self.enter_text(Locators.EXPENSES_EDIT_AMOUNT, "1600")
        self.clear(Locators.EXPENSES_EDIT_AMOUNT)
        self.click(Locators.EXPENSES_EDIT_SAVE)
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 1200);")
        try:
            toast= WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'This field is required.')]"))
            )
            assert toast.is_displayed()
            self.logger.info("Mandatory field validation message displayed correctly.")
        except Exception as e:
            self.driver.save_screenshot("expense_edit_required_field_validation_failed.png")
            self.logger.error("Mandatory field validation message not shown.")
            self.fail("There is no Mandatory Indication on expense configuration.")
 
    def test_expense_edit_invalid_amount(self):
       
        self.click(Locators.EXPENSE_1_EDIT)
        self.driver.execute_script("window.scrollBy(0, -600);")
        self.clear(Locators.EXPENSES_EDIT_AMOUNT)
        self.enter_text(Locators.EXPENSES_EDIT_AMOUNT, "invalid_amount")
        self.click(Locators.EXPENSES_EDIT_SAVE)
        self.driver.execute_script("window.scrollBy(0, 600);")
        
        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid amount format.')]"))
            )
            assert toast.is_displayed()
            self.logger.info("Correctly detected invalid amount format.")
        except Exception as e:
            self.driver.save_screenshot("expense_edit_invalid_amount_error_not_displayed.png")
            self.logger.error("Invalid amount format was accepted without showing an error.")
            self.fail("Invalid amount format accepted and no error message shown.")

    def test_snackbar_expense_edit(self):
        self.click(Locators.EXPENSE_SIDEBAR)
        self.click(Locators.EXPENSES_EDIT_BUTTON)
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.click(Locators.EXPENSE_1_EDIT)
        self.driver.execute_script("window.scrollBy(0,0);") 
        self.clear(Locators.EXPENSES_EDIT_AMOUNT)
        self.enter_text(Locators.EXPENSES_EDIT_AMOUNT, "1600")
        self.click(Locators.EXPENSES_EDIT_SAVE)
        self.driver.execute_script("window.scrollBy(0, 600);")
        
        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Expense updated successfully!')]"))
            )
            assert "Expense updated successfully!" in toast.text
            self.logger.info("Snackbar message displayed after expense edit.")
        except Exception as e:
            self.driver.save_screenshot("expense_edit_snackbar_failed.png")
            self.logger.error("Snackbar not found or message incorrect after expense edit.")
            self.fail("Snackbar not found or message incorrect after expense edit.")
    
    def test_expense_edit_delete(self):
        self.click(Locators.EXPENSE_SIDEBAR)
        self.click(Locators.EXPENSES_EDIT_BUTTON)   
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.click(Locators.EXPENSE_1_DELETE)
        self.click(Locators.EXPENSE_DELETE1_CONFIRM_BUTTON)

        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Expense deleted successfully!')]"))
            )
            assert "Expense deleted successfully!" in toast.text
            self.logger.info("Expense deleted successfully after edit.")
        except Exception as e:
            self.driver.save_screenshot("expense_edit_delete_failed.png")
            self.logger.error("Expense deletion failed or snackbar not found after edit.")
            self.fail("Expense deletion failed or snackbar not found after edit.")

    def test_expense_delete(self):
        self.click(Locators.EXPENSE_DELETE)
        self.click(Locators.EXPENSE_DELETE1_CONFIRM_BUTTON)

        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "(//a[normalize-space()='Add Income'])[1]"))
            )
            assert "Income" in toast.text
            self.logger.info("Expense deleted successfully.")   
        except Exception as e:
            self.driver.save_screenshot("expense_delete_failed.png")
            self.logger.error("Expense deletion failed or snackbar not found.")
            self.fail("Expense deletion failed or snackbar not found.")
            self.click(Locators.EXPENSES_EXPENSE_BACK)

    def snackbar_expense_delete(self):
        self.click(Locators.EXPENSE_DELETE)
        self.click(Locators.EXPENSE_DELETE1_CONFIRM_BUTTON)

        try:
            toast = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Expense deleted successfully!')]"))
            )
            assert "Expense deleted successfully!" in toast.text
            self.logger.info("Snackbar message displayed after expense deletion.")
        except Exception as e:
            self.driver.save_screenshot("expense_delete_snackbar_failed.png")
            self.logger.error("Snackbar not found or message incorrect after expense deletion.")
            self.fail("Snackbar not found or message incorrect after expense deletion.")