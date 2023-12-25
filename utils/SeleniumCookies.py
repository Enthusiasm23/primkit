from ..utils.WebdriverInitializer import get_chrome_driver
from ..config import DEFAULT_TIMEOUT, CHROME_DRIVER_PATH, XSRF_NAME
from ..utils.SysProfiler import get_headers as get_system_headers

import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)


class WebDriverUtility:
    """
    Utility class to interact with a website using Selenium WebDriver.
    """

    def __init__(self, url, driver_path=CHROME_DRIVER_PATH, timeout=DEFAULT_TIMEOUT):
        """
        Initializes a WebDriverUtility instance to manage a WebDriver session.

        This constructor sets up a Chrome WebDriver using the specified driver path and URL.
        It waits for the page to load within the given timeout period.

        Parameters:
        :param url (str): The URL to be accessed by the WebDriver.
        :param driver_path (str, optional): The file path to the ChromeDriver executable. If not provided,
                                       a default path defined by CHROME_DRIVER_PATH is used.
        :param timeout (int, optional): The maximum time in seconds to wait for the page to load.
                                   If not provided, a default timeout defined by DEFAULT_TIMEOUT is used.

        The driver is set to the `self.driver` attribute and can be accessed by instance methods.
        """
        self.driver = get_chrome_driver(driver_path=driver_path)
        self.driver.maximize_window()
        self.driver.get(url)
        self.wait_page_load(timeout)

    @staticmethod
    def get_headers():
        """
        # Call the function imported from primertools.utils.gather_system_details
        """
        return get_system_headers()

    def get_cookies(self):
        """
        Navigate to a URL and return the cookies found on the page.

        :return: 'cookies' in requests format.
        """
        cookies = self.driver.get_cookies()

        return self.convert_cookies_for_requests(cookies)

    def get_token(self, token_name=XSRF_NAME):
        """
        the specified token found on the page.

        :param token_name: The name of the token to retrieve (default is '_xsrf').
        :return: the specified 'token'.
        """
        token = self.get_dynamic_token(token_name)

        return token

    @staticmethod
    def convert_cookies_for_requests(cookies):
        """
        Convert cookies from WebDriver format to requests format.

        :param cookies: A list of cookies from WebDriver.
        :return: A dictionary of cookies in requests format.
        """
        return {cookie['name']: cookie['value'] for cookie in cookies}

    def wait_page_load(self, timeout=DEFAULT_TIMEOUT):
        """
        Wait until the page is fully loaded.

        :param timeout: Maximum time in seconds to wait for the page to load.
        """
        for _ in range(timeout):
            if self.driver.execute_script("return document.readyState") == "complete":
                return
            time.sleep(1)

    def wait_appear_element(self, locator, by=By.CSS_SELECTOR, timeout=DEFAULT_TIMEOUT):
        """
        Wait for an element to appear and be visible on the page.

        :param locator: The locator of the element to wait for.
        :param by: The type of strategy to locate the element (default is By.CSS_SELECTOR).
        :param timeout: Maximum time in seconds to wait for the element to appear.
        :return: True if the element appears within the timeout, False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def get_dynamic_token(self, token_name, timeout=DEFAULT_TIMEOUT):
        """
        Retrieve a dynamic token from the page.

        :param token_name: The name of the token to retrieve.
        :param timeout: Maximum time in seconds to wait for the token to become available.
        :return: The value of the token if found, None otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.NAME, token_name))
            )
            return self.driver.find_element(By.NAME, token_name).get_attribute('value')
        except Exception as e:
            logger.error(f"Error retrieving token: {e}")
            return None

    def close(self):
        """
        Close the WebDriver instance.
        """
        self.driver.quit()
