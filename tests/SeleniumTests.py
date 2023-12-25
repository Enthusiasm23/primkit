from ..tests.PytestTrigger import TestSeleniumEnvironment

import logging

logger = logging.getLogger(__name__)


def ExecuteTests():
    """
    Executes predefined Selenium environment tests.

    This function creates an instance of TestSeleniumEnvironment, sets up the test environment,
    runs the tests, and then tears down the environment. It logs the outcome of the tests and
    returns a boolean indicating success or failure.

    Returns:
        bool: True if tests passed, False otherwise.
    """
    test_instance = TestSeleniumEnvironment()
    try:
        test_instance.setUp()
        test_instance.test_env_setup()  # 检查环境
        test_instance.test_page_load()  # 检查网页
        test_instance.tearDown()
        logger.info("Test passed")
        return True
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False


if __name__ == '__main__':
    ExecuteTests()
