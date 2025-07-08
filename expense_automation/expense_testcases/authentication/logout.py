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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



class Logout(BasePage, unittest.TestCase):
    """
    Login test cases for various scenarios.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.logger = get_logger("Logout")
        self.wait = WebDriverWait(driver, 10)


    def logout(self):
        """
        Perform logout operation.
        """
        self.logger.info("Performing logout operation.")

        self.click(Locators.LOGOUT_BT)
        time.sleep(2)  # Wait for logout to complete
        
        self.click(Locators.LOGOUT_CONFIRM_BUTTON)
        time.sleep(2)  # Wait for confirmation to complete
        try:
            self.driver.find_element(By.XPATH, "(//label[@for='EmailId'])[1]")
            self.logger.info("Logout successful.")
        except Exception as e:
            self.logger.error(f"Logout failed: {e}")
            raise e
        