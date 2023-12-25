from ..tests.pytest_trigger import TestSeleniumEnvironment

import logging

logger = logging.getLogger(__name__)


def run_tests():
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
    run_tests()
