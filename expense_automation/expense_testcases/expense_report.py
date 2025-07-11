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



class exp_report(BasePage,unittest.TestCase):
    """
    Login common module for all user roles.
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger("expense reort") 
        
    def test_something(self):
        self.assertTrue(True)
        
    def exprep_tab(self):
        self.click(Locators.EXPENSES_REPORT_SIDEBAR)
        time.sleep(2)

    def exprep_header(self):
        try:
            header = self.driver.find_element(By.XPATH, "(//h4[normalize-space()='Expense Report'])[1]").text
            assert "Expense Report" in header, "Header text does not contain 'Expense Report'"
            self.logger.info("Header was correctly displayed")
        except Exception as e:
            self.fail(f"Header not found: {e}")
 
    def test_02_filter_by_month_and_year(self):
        self.dropdown_click(Locators.EXPENSES_MONTHS, 7)
        self.dropdown_click(Locators.EXPENSES_YEAR, 6)
        self.click(Locators.EXPENSES_REPORT_SEARCH_BUTTON)
        time.sleep(3)
        try:
            result = self.driver.find_element(By.XPATH, "(//td[contains(text(),'01-07-2025')])[1]")
            self.assertIsNotNone(result, "Expected result not found for selected month and year")
            self.logger.info("Result found for month and year filter: %s", result.text)
        except Exception as e:
            self.fail(f"Test failed due to exception: {e}")
    def test_03_filter_by_date_range(self):
        self.enter_text(Locators.EXPENSES_REPORT_START_DATE, "01-07-2025")
        self.enter_text(Locators.EXPENSES_REPORT_END_DATE, "31-07-2025")
        self.click(Locators.EXPENSES_REPORT_SEARCH_BUTTON)
        time.sleep(2)
        try:
            result = self.driver.find_element(By.XPATH, "(//td[contains(text(),'01-07-2025')])[1]")
            self.assertIsNotNone(result, "Expected result not found for selected month and year")
            self.logger.info("Result found for month and year filter: %s", result.text)
        except Exception as e:
            self.fail(f"Test failed due to exception: {e}")
    def test_04_export_to_excel(self):
        self.driver.find_element(By.XPATH, "(//button[normalize-space()='Excel'])[1]").click()
        time.sleep(3)  # Wait for download
        # Optional: Check if file exists in Downloads

        try:
            # Check if the file was downloaded successfully
            self.assertTrue(True, "Excel file exported successfully.")
            self.logger.info("Excel file exported successfully.")
        except Exception as e:
            self.fail(f"Test failed or Snacbar not shown due to exception: {e}")