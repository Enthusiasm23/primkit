from ..utils import get_chrome_driver
from ..config import TEST_URL, DEFAULT_HEADLESS

import unittest


import logging
logger = logging.getLogger(__name__)


class TestSeleniumEnvironment(unittest.TestCase):
    def setUp(self):
        try:
            # 尝试获取 Chrome driver
            self.driver = get_chrome_driver(headless=DEFAULT_HEADLESS)
        except Exception as e:
            self.driver = None
            logger.error(f"Selenium environment setup failed: {e}")

    def tearDown(self):
        # 在测试结束时执行的清理代码
        if self.driver:
            self.driver.quit()

    def test_env_setup(self):
        # 直接检查 self.driver 是否成功创建，来判断 Selenium 环境是否设置成功
        if self.driver is None:
            raise Exception("Selenium environment setup failed.")

    def test_page_load(self, test_url=TEST_URL):
        if self.driver is None:
            raise Exception("Selenium environment setup failed.")
        # 执行实际的测试，例如访问网页
        self.driver.get(test_url)
        if "Example" not in self.driver.title:
            raise Exception("Website title does not contain 'Example'.")


if __name__ == '__main__':
    unittest.main()
