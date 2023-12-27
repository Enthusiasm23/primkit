import unittest
import logging
from ..utils import get_chrome_driver
from ..config import TEST_URL, DEFAULT_HEADLESS

logger = logging.getLogger(__name__)


class TestSeleniumEnvironment(unittest.TestCase):
    def setUp(self):
        try:
            # Attempt to obtain Chrome driver
            self.driver = get_chrome_driver(headless=DEFAULT_HEADLESS)
        except Exception as e:
            self.driver = None
            logger.error(f"Selenium environment setup failed: {e}")

    def tearDown(self):
        # Cleanup code executed at the end of testing
        if self.driver:
            self.driver.quit()

    def test_env_setup(self):
        # Directly check if the self.driver has been successfully created to determine if the Selenium environment has been successfully set up
        if self.driver is None:
            raise Exception("Selenium environment setup failed.")

    def test_page_load(self, test_url=TEST_URL):
        if self.driver is None:
            raise Exception("Selenium environment setup failed.")
        # Perform actual testing, such as accessing web pages
        self.driver.get(test_url)
        if "Example" not in self.driver.title:
            raise Exception("Website title does not contain 'Example'.")


if __name__ == '__main__':
    unittest.main()
