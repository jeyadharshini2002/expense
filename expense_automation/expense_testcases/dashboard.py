from test_base import TestBase
from locators import Locators
from selenium.webdriver.common.by import By
import unittest
import time
from logger_file import get_logger
from base import BasePage

from selenium.webdriver.support import expected_conditions as EC


from logger_file import get_logger
def parse_amount(text):
    # Removes currency symbol, commas and converts to int
    return int(text.replace("₹", "").replace(",", "").strip())

class TestDashboard(BasePage,unittest.TestCase):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger("dashboard") 
        
    def test_something(self):
        self.assertTrue(True)

    def dash_header(self):
        try:
            header = self.driver.find_element(By.XPATH, "(//h3[normalize-space()='Dashboard'])[1]").text
            assert "Dashboard" in header, "Header text does not contain 'Dashboard'"
            self.logger.info("Header was correctly displayed")
        except Exception as e:
            self.fail(f"Header not found: {e}")
     
    def test_dashboard_balance_calculation(self):
        try:
            income_text = self.driver.find_element(By.XPATH, "//h4[contains(text(),'Income')]/following-sibling::h2").text
            expense_text = self.driver.find_element(By.XPATH, "//h4[contains(text(),'Expense')]/following-sibling::h2").text
            balance_text = self.driver.find_element(By.XPATH, "//h4[contains(text(),'Balance')]/following-sibling::h2").text

            print("[DEBUG] Raw values:")
            print(f"Income: {income_text}")
            print(f"Expense: {expense_text}")
            print(f"Balance: {balance_text}")

            income = int(income_text.replace("₹", "").replace(",", "").strip())
            expense = int(expense_text.replace("₹", "").replace(",", "").strip())
            balance = int(balance_text.replace("₹", "").replace(",", "").strip())

            assert income - expense == balance, f"Mismatch: Income({income}) - Expense({expense}) != Balance({balance})"
        except Exception as e:
            self.driver.save_screenshot("dashboard_balance_fail.png")
            with open("dashboard_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.fail(f"Test failed due to: {e}")



    def test_dashboard_balance_non_negative(self):
        try:
            balance_text = self.driver.find_element(By.XPATH, "//h4[contains(text(),'Balance')]/following-sibling::h2").text
            print(f"[DEBUG] Balance text: {balance_text}")
            balance = int(balance_text.replace("₹", "").replace(",", "").strip())
            assert balance >= 0, f"Balance is negative: {balance}"
        except Exception as e:
            self.driver.save_screenshot("balance_non_negative_fail.png")
            with open("dashboard_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.fail(f"Test failed due to: {e}")
            
    def test_dashboard_amounts_displayed(self):
        try:
            income_text = self.driver.find_element(By.XPATH, "//h4[contains(text(),'Income')]/following-sibling::h2").text
            expense_text = self.driver.find_element(By.XPATH, "//h4[contains(text(),'Expense')]/following-sibling::h2").text

            print(f"[DEBUG] Income text: {income_text}")
            print(f"[DEBUG] Expense text: {expense_text}")

            assert "₹" in income_text and income_text.strip() != "₹ 0", "Income not displayed or is ₹ 0"
            assert "₹" in expense_text and expense_text.strip() != "₹ 0", "Expense not displayed or is ₹ 0"
        except Exception as e:
            self.driver.save_screenshot("dashboard_amounts_displayed_fail.png")
            with open("dashboard_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.fail(f"Test failed due to: {e}")       