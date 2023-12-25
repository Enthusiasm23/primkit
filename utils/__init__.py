"""
This is the `utils` module of the project.

This module provides utility functions and classes that are used across the project.
This includes functions for configuring and managing WebDriver instances for Selenium testing,
and a utility class for fetching cookies and tokens from websites using WebDriver.

See the `WebdriverInitializer.py` for more detailed information on configuring WebDriver instances.
"""

from .SysProfiler import get_system_type, get_headers, is_url, get_user_agent
from .WebdriverInitializer import get_chrome_driver, get_default_chrome_options
from .SiteSeleniumer import WebDriverUtility
from .SiteRequester import get_site_data
from .DataFetcher import fetch_web_data
from .ResultDownloader import download
from .FileReader import FileReader
from .DatabaseHandler import DatabaseHandler
from .EmailManager import EmailManager
