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



class LoginPage(BasePage, unittest.TestCase):
    """
    Login test cases for various scenarios.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.logger = get_logger("LoginPage")
        self.wait = WebDriverWait(driver, 10)

    def a_login_invalid_credentials(self):
        self.driver.execute_script("window.scrollTo(0,500);")
        time.sleep(2)

        self.enter_text(Locators.EMAIL_INPUT, "invalid_username")
        self.enter_text(Locators.PASSWORD_INPUT, "invalid_password")
        self.click(Locators.LOGIN_SUBMIT_BUTTON)

        try:
            LOGIN_INVALID_CREDENTIALS = (By.XPATH, "//p[normalize-space()='Invalid email or password.']")
            message = self.get_text(LOGIN_INVALID_CREDENTIALS)

            if message != "Invalid email or password.":
                raise AssertionError(f"Expected 'Invalid email or password.' but got '{message}'")

            self.logger.warning("Invalid credentials entered.")
            print("Invalid credentials entered.")

        except Exception as e:
            print("Expected error message not found on invalid credentials.")
            raise AssertionError(f"Expected error message not found. Exception: {e}")

    def b_login_invalid_password(self):
        self.driver.execute_script("window.scrollTo(0,500);")
        time.sleep(2)

        self.clear(Locators.EMAIL_INPUT)
        self.clear(Locators.PASSWORD_INPUT)
        self.enter_text(Locators.EMAIL_INPUT, "diyas@gmail.com")
        self.enter_text(Locators.PASSWORD_INPUT, "wrong password")
        self.click(Locators.LOGIN_SUBMIT_BUTTON)

        try:
            message = self.get_text(Locators.LOGIN_INVALID_CREDENTIALS)
            if message != "Invalid email or password.":
                raise AssertionError(f"Expected 'Invalid email or password.' but got '{message}'")
            self.logger.warning("Invalid password entered.")
        except Exception as e:
            raise AssertionError(f"Expected error message not found on invalid password. Exception: {e}")



    def c_login_invalid_username(self):
        self.driver.execute_script("window.scrollTo(0,500);")
        time.sleep(2)

        self.clear(Locators.EMAIL_INPUT)
        self.clear(Locators.PASSWORD_INPUT)
        self.enter_text(Locators.EMAIL_INPUT, "wrong username")
        self.enter_text(Locators.PASSWORD_INPUT, "Diya@7482")
        self.click(Locators.LOGIN_SUBMIT_BUTTON)

        try:
            message = self.get_text(Locators.LOGIN_INVALID_CREDENTIALS)
            if message != "Invalid email or password.":
                raise AssertionError(f"Expected 'Invalid email or password.' but got '{message}'")
            self.logger.warning("Invalid username entered.")
        except Exception as e:
            raise AssertionError(f"Expected error message not found on invalid username. Exception: {e}")

    def d_login_without_password(self):
        self.driver.execute_script("window.scrollTo(0,500);")
        time.sleep(2)

        self.clear(Locators.EMAIL_INPUT)
        self.clear(Locators.PASSWORD_INPUT)
        self.enter_text(Locators.EMAIL_INPUT, "diyas@gmail.com")
        self.click(Locators.LOGIN_SUBMIT_BUTTON)

        try:
            message = self.get_text(Locators.LOGIN_PASSWORD_ONLY_REQUIRED)
            if message != "The Password field is required.":
                raise AssertionError(f"Expected 'The Password field is required.' but got '{message}'")
            self.logger.warning("Password not entered.")
        except Exception as e:
            raise AssertionError(f"Expected password validation message not found. Exception: {e}")

    def e_login_without_username(self):
        self.driver.execute_script("window.scrollTo(0,500);")
        time.sleep(2)

        self.clear(Locators.EMAIL_INPUT)
        self.clear(Locators.PASSWORD_INPUT)
        self.enter_text(Locators.PASSWORD_INPUT, "Diya@7482")
        self.click(Locators.LOGIN_SUBMIT_BUTTON)

        try:
            message = self.get_text(Locators.LOGIN_USERNAME_ONLY_REQUIRED)
            if message != "The EmailId field is required.":
                raise AssertionError(f"Expected 'The EmailId field is required.' but got '{message}'")
            self.logger.warning("Username not entered.")
        except Exception as e:
            raise AssertionError(f"Expected username validation message not found. Exception: {e}")


    def f_login_successful(self):
        self.driver.execute_script("window.scrollTo(0,500);")

        time.sleep(2)
        self.clear(Locators.EMAIL_INPUT)
        self.clear(Locators.PASSWORD_INPUT)
        self.enter_text(Locators.EMAIL_INPUT, "diyas@gmail.com")
        self.enter_text(Locators.PASSWORD_INPUT, "Diya@7482")
        time.sleep(2)

        self.click(Locators.LOGIN_SUBMIT_BUTTON)
        time.sleep(2)
        try:
            self.wait.until(EC.presence_of_element_located(Locators.DASHBOARD_HEADER))
            self.logger.info("Login successful, no error message found.")    

        except AssertionError:
            self.logger.error("Expected error message found, login failed.")

        
        self.logger.info("Login successful.")
        time.sleep(2)

