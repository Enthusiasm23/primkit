from ..utils.SiteSeleniumer import WebDriverUtility
from ..utils.SiteRequester import get_site_data
from ..config import PRIMER_URL

import logging
import requests
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger(__name__)


def fetch_web_data(url=PRIMER_URL, method='requests'):
    """
    Fetches headers, cookies, and a token from a given URL using either requests or selenium.

    Parameters:
    - url (str): URL to fetch data from.
    - method (str): Method to use for fetching data ('requests' or 'selenium').

    Returns:
    - tuple: (headers, cookies, token) if successful, otherwise raises an error.
    """
    logger.info(f"Fetching web data from {url} using {method}")

    headers = {}
    cookies = {}
    token = None

    if method == 'requests':
        # requests fetching logic
        try:
            # (requests fetching implementation)
            headers, cookies, token = get_site_data(url)
            logger.info("Data fetched using requests.")
        except requests.RequestException:
            pass  # Log error or handle exception

    elif method == 'selenium':
        # selenium fetching logic
        try:
            # (selenium fetching implementation)
            utility = WebDriverUtility(url)
            utility.load_url()
            headers = utility.get_headers() or {}
            cookies = utility.get_cookies() or {}
            token = utility.get_token()
            utility.close()
            logger.info("Data fetched using Selenium.")
        except WebDriverException as e:
            raise e

    else:
        raise ValueError("Invalid method. Choose 'requests' or 'selenium'.")

    # Check if data is valid and return
    if token is not None:
        logger.info(f"Fetched headers, cookies, and token successfully.")
        return headers, cookies, token
    else:
        raise ValueError("Failed to fetch data.")
