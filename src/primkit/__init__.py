__doc__ = """
The `primkit` package is a comprehensive toolkit for primer design and molecular biology applications. It includes utilities for logging setup, system profiling, web driver initialization, web data fetching, and results downloading, among others.

This package facilitates various tasks such as automated browser interactions with Selenium, fetching and processing web data, handling files, managing databases, and sending emails. Additionally, it provides a designer module to create and manage primer design workflows.

Importing `primkit` will set up logging, execute tests, and provide access to a suite of tools for efficient molecular biology research.
"""
__version__ = "0.1.3"
__author__ = 'LiBao Feng',
__email__ = 'lbfeng23@gmail.com',
__license__ = 'MIT'
__description__ = 'A comprehensive toolkit for primer design and molecular biology.'
__url__ = 'https://github.com/Enthusiasm23/primkit'

from .utils.LoggerSetup import setup_logging
from .tests.SeleniumTests import ExecuteTests
from .utils.SysProfiler import get_system_type, get_headers, is_url, get_user_agent
from .utils.WebdriverInitializer import get_chrome_driver, get_default_chrome_options
from .utils.SiteSeleniumer import WebDriverUtility
from .utils.SiteRequester import get_site_data
from .utils.DataFetcher import fetch_web_data
from .utils.ResultDownloader import download
from .utils.FileReader import FileReader
from .utils.DatabaseHandler import DatabaseHandler
from .utils.EmailManager import EmailManager
from .designer.Primer import prepare_post_data, submit_and_track, check_task_status, design_primers

# Setup logging on module import
setup_logging()

__all__ = [
    'ExecuteTests', 'get_system_type', 'get_headers', 'is_url', 'get_user_agent',
    'get_chrome_driver', 'get_default_chrome_options', 'WebDriverUtility',
    'get_site_data', 'fetch_web_data', 'download', 'FileReader',
    'DatabaseHandler', 'EmailManager', 'prepare_post_data', 'submit_and_track',
    'check_task_status', 'design_primers'
]
