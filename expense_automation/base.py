import configparser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

config = configparser.ConfigParser()
config.read("./settings.conf")


class BasePage:
    """This class is the parent class for all the pages in our application."""
    """It contains all common elements and functionalities available to all pages."""

    # this function is called every time a new object of the base class is created.
    def __init__(self, driver):
        self.driver: WebDriver = driver

    # this function performs click on web element whose locator is passed to it.
    def click(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).click()

    # this function asserts comparison of a web element's text with passed in text.
    def assert_element_text(self, by_locator, element_text):
        web_element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        assert web_element.text == element_text

    # this function performs text entry of the passed in text, in a web element whose locator is passed to it.
    def enter_text(self, by_locator, text):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)


    # this function checks if the web element whose locator has been passed to it, is enabled or not and returns
    # web element if it is enabled.
    def is_enabled(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))

    def is_clickable(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))

    # this function checks if the web element whose locator has been passed to it, is visible or not and returns
    # true or false depending upon its visibility.
    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    # this function moves the mouse pointer over a web element whose locator has been passed to it.
    def hover_to(self, by_locator):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
        ActionChains(self.driver).move_to_element(element).perform()

    def send_keys(self, by_locator, text):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def file_upload(self, by_locator, file_path):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(by_locator)).send_keys(file_path)

        # this function is used to check if element is present

    def is_element_present(self, by_locator):
        try:
            self.driver.find_element(by_locator[0], by_locator[1])
        except NoSuchElementException:
            return False
        return True

    def is_element_clickable(self, by_locator):
        try:
            self.driver.find_element(by_locator[0], by_locator[1])
        except NoSuchElementException:
            return False
        return True

    # this function performs to get the text of web element whose locator is passed to it.
    def get_text(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).text

    # this function performs to get the value of input field whose locator is passed to it.
    def get_attribute(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).get_attribute('value')

    # this function perform
    def is_selected(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).is_selected()

    # this function performs to get the location of multiple web elements whose locator is passed to it.
    def locate_elements(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(by_locator))

    # this function performs to clear the text of web element whose locator is passed to it.
    def clear(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(Keys.CONTROL + "a" + Keys.DELETE)

    # def drag_and_drop(self, by_source, by_target):
    #     source = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_source))
    #     target = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_target))
    #     ActionChains(self.driver).drag_and_drop(source, target).perform()
    #     ActionChains(self.driver).drag_and_drop_by_offset()

    def static_dropdown(self, by_locator, text):
        a = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(by_locator))

        for b in a:
            if b.text == text:
                b.click()

    def dropdown_click(self, by_locator, n):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).click()
        for i in range(n):
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(Keys.ARROW_DOWN)

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(Keys.ENTER)

    def ag_grid_row(self, by_locator):
        x = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).text
        return x.split("\n")

    def scroll_down(self, scroll=0):
        script = "window.scrollBy(0,{})"
        return self.driver.execute_script(script.format(scroll))

    def loc(self, by_locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator))
    
    def is_element_present(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def select_dropdown_by_index(self, locator, index=1):
        from selenium.webdriver.support.ui import Select
        select = Select(self.find(locator))
        select.select_by_index(index)
