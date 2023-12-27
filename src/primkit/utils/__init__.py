"""
This is the `utils` module of the `primkit` package.

This module provides utility functions and classes that are used across the project, including:

- `get_system_type`: Determine the operating system type. See `SysProfiler.py` for details.
- `get_headers`: Generate HTTP headers for web requests. See `SysProfiler.py` for usage.
- `is_url`: Validate if a string is a properly formatted URL. See `SysProfiler.py` for implementation.
- `get_user_agent`: Retrieve a user agent string for web requests. See `SysProfiler.py` for more information.
- `get_chrome_driver`: Initialize and retrieve a Chrome WebDriver instance. For configuration, refer to `WebdriverInitializer.py`.
- `get_default_chrome_options`: Get default options for Chrome WebDriver. Details in `WebdriverInitializer.py`.
- `WebDriverUtility`: Provides utilities for managing WebDriver instances. Refer to `SiteSeleniumer.py` for functionality.
- `get_site_data`: Perform HTTP GET requests to retrieve data from websites. Implemented in `SiteRequester.py`.
- `fetch_web_data`: Fetch and process web data using Selenium. See `DataFetcher.py` for the process.
- `download`: Download files or data from the web. Usage described in `ResultDownloader.py`.
- `FileReader`: Handle file reading operations. Refer to `FileReader.py` for more details.
- `DatabaseHandler`: Manage database connections and operations. See `DatabaseHandler.py`.
- `EmailManager`: Manage email sending operations. Implemented in `EmailManager.py`.

Each utility function and class is designed to be modular and reusable. For specific functionality and implementation details, refer to the corresponding script within this module.
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

__all__ = [
    'get_system_type', 'get_headers', 'is_url', 'get_user_agent',
    'get_chrome_driver', 'get_default_chrome_options',
    'WebDriverUtility',
    'get_site_data',
    'fetch_web_data',
    'download',
    'FileReader',
    'DatabaseHandler',
    'EmailManager'
]
