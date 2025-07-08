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
import os
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class category_ledger(BasePage,unittest.TestCase):
    """
    Login common module for all user roles.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger("category ledger") 
        
    def test_something(self):
        self.assertTrue(True)
        
    def catledg_tab(self):
        time.sleep(5)
        self.click(Locators.CATEGORY_WISE_LEDGER_SIDEBAR)
        time.sleep(2)
    def test_filter_by_date(self):
        self.click(Locators.CATEGORY_WISE_LEDGER_SIDEBAR)
        self.enter_text(Locators.CATEGORY_WISE_LEDGER_STARTDATE, "01-07-2025")
        self.enter_text(Locators.CATEGORY_WISE_LEDGER_ENDDATE, "31-07-2025")
        self.click(Locators.CATEGORY_WISE_LEDGER_SEARCH_BUTTON)
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, -500);")
        self.logger.info("Applying date filter from 01-07-2025 to 31-07-2025")
        time.sleep(2)  # Wait for the page to load completely
        try:
            # Try to locate the result row
            result = self.driver.find_element(By.XPATH, "(//td[contains(text(),'01-07-2025')])[1]")
            self.assertIsNotNone(result, "Expected result not found for selected date range")
            self.logger.info("Result found for date filter: %s", result.text)
        except Exception as e:
            self.fail(f"Test failed due to exception: {e}")
        
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)  # Wait for the page to load completely
        

    def test_export_to_excel(self):
        try:
            # Click Excel export button (already assumed working)
            excel_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(Locators.CATEGORY_WISE_LEDGER_EXCEL_BUTTON)
            )
            try:
                excel_button.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", excel_button)

            time.sleep(5)  # Give time for download to complete

            # Check Downloads folder
            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            expected_prefix = "CATEGORY_WISE_LEDGER_01-07-2025_to_31-07-2025"
            matching_files = [
                f for f in os.listdir(downloads_dir)
                if f.startswith(expected_prefix) and f.endswith(".xls")
            ]

            self.assertTrue(
                len(matching_files) > 0,
                f"[FAIL] No downloaded file found with prefix: {expected_prefix} in {downloads_dir}"
            )

            # Optional: log the latest file name
            latest_file = max(
                [os.path.join(downloads_dir, f) for f in matching_files],
                key=os.path.getctime
            )
            self.logger.info(f"[PASS] File downloaded successfully: {latest_file}")

        except Exception as e:
            self.driver.save_screenshot("export_excel_fail.png")
            self.fail(f"[FAIL] Export test failed due to: {e}")

    def test_totals_calculation(self):
        self.click(Locators.CATEGORY_WISE_LEDGER_CLEAR_BUTTON)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        def parse_amount(text):
            try:
                return float(text.replace(',', '').replace('Cr', '').replace('Dr', '').strip())
            except ValueError:
                print(f"[WARN] Could not parse amount: '{text}'")
                return 0.0

        try:
            # Get displayed values from footer (Total row)
            displayed_income = parse_amount(self.driver.find_element(
                By.XPATH, "//td[normalize-space()='Total']/following-sibling::td[1]"
            ).text)

            displayed_expense = parse_amount(self.driver.find_element(
                By.XPATH, "//td[normalize-space()='Total']/following-sibling::td[2]"
            ).text)

            displayed_closing = parse_amount(self.driver.find_element(
                By.XPATH, "//td[normalize-space()='Total']/following-sibling::td[3]"
            ).text)

            #  Calculate expected closing balance
            expected_closing = round(displayed_income - displayed_expense, 2)

            self.assertAlmostEqual(expected_closing, displayed_closing, places=2, msg="Closing total mismatch")

            self.logger.info(f"[PASS]  Income: {displayed_income} | Expense: {displayed_expense} | Expected Closing: {expected_closing} | Displayed Closing: {displayed_closing}")


        except Exception as e:
            self.driver.save_screenshot("totals_fail.png")
            self.fail(f"[FAIL]  Total calculation failed: {e}")
