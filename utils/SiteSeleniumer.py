import logging
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from ..utils.WebdriverInitializer import get_chrome_driver
from ..config import DEFAULT_TIMEOUT, CHROME_DRIVER_PATH, XSRF_NAME
from ..utils.SysProfiler import get_headers as get_system_headers, is_url

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
        self.url = url
        self.driver_path = driver_path
        self.timeout = timeout
        self.driver = None

    def init_driver(self, return_driver=False):
        """
        Initializes the WebDriver if it has not been initialized already.
        """
        if not self.driver:
            self.driver = get_chrome_driver(driver_path=self.driver_path)
            self.driver.maximize_window()
        if return_driver:
            logging.warning("Direct access to the WebDriver is granted. This reduces encapsulation and abstraction.")
            return self.driver

    def load_url(self):
        """
        Navigates to the URL set during initialization after ensuring the driver is ready.
        If the URL is not valid, raises a ValueError.
        """
        if not is_url(self.url):
            raise ValueError(f"Invalid URL: {self.url}")

        self.init_driver()
        self.driver.get(self.url)
        self.ensure_loaded(self.timeout)

    def ensure_loaded(self, timeout=DEFAULT_TIMEOUT):
        """
        Waits for the page to load within the given timeout period.
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    @staticmethod
    def get_headers():
        """
        # Call the function imported from primertools.utils.gather_system_details
        """
        return get_system_headers()

    @staticmethod
    def format_cookies(cookies):
        """
        Convert cookies from WebDriver format to requests format.

        :param cookies: A list of cookies from WebDriver.
        :return: A dictionary of cookies in requests format.
        """
        return {cookie['name']: cookie['value'] for cookie in cookies}

    def get_cookies(self):
        """
        Navigate to a URL and return the cookies found on the page.

        :return: 'cookies' in requests format.
        """
        cookies = self.driver.get_cookies()

        return self.format_cookies(cookies)

    def get_token(self, token_name=XSRF_NAME):
        """
        the specified token found on the page.

        :param token_name: The name of the token to retrieve (default is '_xsrf').
        :return: the specified 'token'.
        """
        token = self.get_dynamic_token(token_name)

        return token

    def refresh_page(self):
        """
        Refreshes the current page.
        """
        self.driver.refresh()

    def ensure_element(self, locator, by=By.CSS_SELECTOR, timeout=DEFAULT_TIMEOUT):
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

    def get_page_source(self):
        """
        Retrieves the source code of the current page loaded in the WebDriver.

        :return: A string representing the source code of the current page.
        """
        return self.driver.page_source

    def scroll_to_element(self, element):
        """
        Scrolls the browser window to an element.

        :param element: The WebElement to scroll to.
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def is_driver_active(self):
        """
        Checks if the WebDriver is still active.

        :return: True if the WebDriver session is still active, False if it has been closed.
        """
        try:
            # Attempt to get the current URL. If the driver is closed, this will raise an exception.
            _ = self.driver.current_url
            return True
        except WebDriverException:
            return False

    def find_element(self, by, value):
        """
        Finds an element on the page based on the provided locator.

        :param by: The method to locate the element (e.g., By.ID, By.CSS_SELECTOR).
        :param value: The value of the locator.
        :return: The found web element.
        """
        return self.driver.find_element(by, value)

    def click_by_locator(self, by, value):
        """
        Clicks an element on the page identified by a locator.

        :param by: The method to locate the element.
        :param value: The value of the locator.
        """
        element = self.find_element(by, value)
        element.click()

    @staticmethod
    def click_element(element):
        """
        Clicks a web element.

        :param element: The web element to click.
        """
        element.click()

    def clear_by_locator(self, by, value):
        """
        Clears the content of an input field identified by a locator.

        :param by: The method to locate the element.
        :param value: The value of the locator.
        """
        element = self.find_element(by, value)
        element.clear()

    @staticmethod
    def clear_element(element):
        """
        Clears the content of a web element.

        :param element: The web element to clear.
        """
        element.clear()

    def input_by_locator(self, by, value, text):
        """
        Inputs text into an element identified by a locator.

        :param by: The method to locate the element.
        :param value: The value of the locator.
        :param text: The text to input into the element.
        """
        element = self.find_element(by, value)
        element.send_keys(text)

    @staticmethod
    def input_element(element, *args):
        """
        Inputs text or key sequences into a web element.

        Usage Examples:
        - utility.input_element(element, "Text to input")
        - utility.input_element(element, Keys.SHIFT, Keys.SPACE)

        :param element: The web element where the text or key sequences will be input.
        :param args: The text or key sequences to input into the element.
        """
        for arg in args:
            element.send_keys(arg)

    def input_values(self, locator_or_element, input_value, by=None):
        """
        Inputs the given value into the element identified by the locator or directly into the provided element.

        Usage Examples:
        - Using a Locator Tuple:
          utility.input_values((By.CSS_SELECTOR, "#inputElementId"), "Input Value")
          utility.input_values((By.ID, "inputElementId"), "Input Value")

        - Using a Web Element:
          element = utility.find_element(By.CSS_SELECTOR, "#inputElementId")
          utility.input_values(element, "Input Value")

        - Using locator value with by parameter:
          utility.input_values("inputElementId", "Input Value", by=By.ID)

        :param locator_or_element: Either a locator tuple, an element object, or a locator string.
        :param input_value: The value to input into the element.
        :param by: Optional; The type of the locator (By.CSS_SELECTOR, By.ID, etc.).
                   Required if the first parameter is a locator string.
        :raises: Exception if the locator_or_element is not a valid WebElement or locator tuple.
        """
        if isinstance(locator_or_element, tuple):
            # Check if the first element of the tuple is a valid By attribute
            if not (locator_or_element[0] in vars(By).values() and isinstance(locator_or_element[1], str)):
                raise ValueError("Locator tuple is not in the correct order (By method, locator value).")
            element = self.find_element(*locator_or_element)
        elif by is not None:
            element = self.find_element(by, locator_or_element)
        elif isinstance(locator_or_element, WebElement):
            element = locator_or_element
        else:
            raise ValueError("The locator_or_element argument must be a locator tuple, WebElement, or string with 'by' parameter.")

        # Perform actions on the located element
        self.click_element(element)
        self.clear_element(element)
        self.input_element(element, input_value)

    def get_element_attribute(self, locator, attribute, by=By.CSS_SELECTOR):
        """
        Gets the specified attribute of an element.

        Usage Example:
        - utility.get_element_attribute("#myElement", "href")

        :param locator: The locator of the element.
        :param attribute: The attribute to retrieve from the element.
        :param by: The method to locate the element (default is By.CSS_SELECTOR).
        :return: The value of the specified attribute, or None if the element is not found.
        """
        try:
            element = self.driver.find_element(by, locator)
            return element.get_attribute(attribute)
        except Exception as e:
            logger.error(f'Error getting attribute from element: {e}')
            return None

    def select_dropdown_option(self, dropdown_selector, option_value):
        """
        Selects an option from a dropdown select element based on the value attribute of the option.
        Raises an exception if the option_value is not found in the dropdown.

        :param dropdown_selector: The CSS selector for the dropdown select element.
        :param option_value: The value attribute of the option to be selected.
        :raises NoSuchElementException: If the option_value is not found in the dropdown options.
        """
        # Find the dropdown select element
        dropdown_element = self.find_element(By.CSS_SELECTOR, dropdown_selector)

        # Create a Select object for the dropdown element
        select = Select(dropdown_element)

        # Check if the option value is present in the dropdown
        if not any(option.get_attribute('value') == option_value for option in select.options):
            available_options = [option.get_attribute('value') for option in select.options]
            raise NoSuchElementException(f"The option value '{option_value}' was not found in the dropdown. "
                                         f"Available options are: {available_options}")

        # Select the option by its value attribute
        select.select_by_value(option_value)

    def close(self):
        """
        Closes the WebDriver session.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
