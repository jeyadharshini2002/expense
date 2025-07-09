import unittest
import os
import uuid
import configparser
import tempfile
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from logger_file import get_logger

# Load config
config = configparser.ConfigParser()
settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.conf')
config.read(settings_path)

if 'expense' not in config:
    raise ValueError("Missing 'expense' section in settings.conf!")

class TestBase(unittest.TestCase):
    """
    Base test class using WebDriverManager to automatically manage ChromeDriver.
    Uses class-level setup to create single Chrome instance for all tests.
    """
    driver = None
    logger = None

    @classmethod
    def setUpClass(cls):
        """
        Set up Chrome driver once for all tests in the class
        """
        cls.logger = get_logger(cls.__name__)
        cls.logger.info("Setting up Chrome driver for all tests")

        # Ensure TEST_URL is present
        if 'TEST_URL' not in config['expense']:
            raise ValueError("Missing 'TEST_URL' in expense section!")

        try:
            # Use webdriver-manager to fetch the correct driver
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = webdriver.ChromeOptions()

            # Profile isolation
            unique_profile = os.path.join(tempfile.gettempdir(), f"profile-{uuid.uuid4()}")
            chrome_options.add_argument(f"--user-data-dir={unique_profile}")
            chrome_options.add_argument("--remote-debugging-port=0")

            # COMMON OPTIONS
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")

            # ⚪️ UNCOMMENT THIS BLOCK FOR GITHUB ACTIONS (HEADLESS)
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # chrome_options.add_argument('--window-size=1920x1080')

            # ⚪️ COMMENT THIS LINE IF USING HEADLESS (GitHub)
            # chrome_options.add_argument("--start-maximized")

            # Initialize driver
            cls.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            cls.driver.get(config['expense']['TEST_URL'])

            # ⚪️ UNCOMMENT THIS FOR CI (already handled by window-size)
            cls.driver.set_window_size(1920, 1080)

            cls.driver.implicitly_wait(10)
            cls.logger.info(f"Browser initialized and navigated to {config['expense']['TEST_URL']}")

        except Exception as e:
            cls.logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise

    @classmethod
    def tearDownClass(cls):
        """
        Close Chrome driver after all tests are completed
        """
        if cls.driver:
            try:
                cls.logger.info("Closing browser after all tests completed")
                cls.driver.quit()
                cls.logger.info("Browser closed and driver quit successfully")
            except Exception as e:
                cls.logger.error(f"Error closing browser: {str(e)}")
            finally:
                cls.driver = None

    def setUp(self) -> None:
        """
        Setup before each individual test - no new driver creation
        """
        if not self.driver:
            raise Exception("WebDriver not initialized. Check setUpClass method.")

        # Get logger for individual test
        self.test_logger = get_logger(f"{self.__class__.__name__}.{self._testMethodName}")
        self.test_logger.info(f"Starting test: {self._testMethodName}")

    def tearDown(self):
        """
        Cleanup after each test - don't close the driver
        """
        self.test_logger.info(f"Completed test: {self._testMethodName}")
        # Optional cleanup like clearing cookies
        # self.driver.delete_all_cookies()
