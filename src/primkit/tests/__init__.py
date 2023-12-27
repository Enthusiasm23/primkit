"""
This is the 'tests' module of the project.

This module contains automated tests for the project, using the Selenium WebDriver for browser automation.
It includes:
- 'PytestTrigger.py': Defines test cases using the unittest framework to ensure the Selenium environment is correctly set up and web pages can be loaded successfully.
- 'SeleniumTests.py': Provides a script to run the Selenium tests outside of the standard unittest framework, allowing for custom handling of test setup and teardown, and result reporting.

These scripts are intended to be run as standalone testing procedures and are critical in ensuring the functionality and reliability of the web automation aspects of the project.
"""
from .PytestTrigger import TestSeleniumEnvironment
from .SeleniumTests import ExecuteTests

__all__ = ['TestSeleniumEnvironment', 'ExecuteTests']
