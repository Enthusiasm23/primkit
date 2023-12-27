import requests
from bs4 import BeautifulSoup
from ..utils.SysProfiler import get_headers, is_url
from ..config import XSRF_NAME


def get_site_data(url):
    """
    Fetch headers, cookies, and the CSRF token from a given URL.
    If the URL is not valid, raises a ValueError.

    Parameters:
    - url (str): The URL to fetch the data from.

    Returns:
    - dict: The headers obtained from the `get_headers` function.
    - dict: The cookies obtained from the response, formatted as a dictionary.
    - str or None: The value of the CSRF token, if found; otherwise, None.

    Raises:
    - requests.RequestException: If there is an error making the GET request.
    - ValueError: If the status code is not 200 or the CSRF token is not found.
    """
    if not is_url(url):
        raise ValueError(f"Invalid URL: {url}")

    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Error fetching data from {url}: Status code {response.status_code}")

        headers = get_headers()
        cookies = {cookie.name: cookie.value for cookie in response.cookies}

        soup = BeautifulSoup(response.content, 'html.parser')
        token_element = soup.find('input', {'name': XSRF_NAME})
        token = token_element['value'] if token_element else None

        if token is None:
            raise ValueError(f"CSRF token not found at {url}")

        return headers, cookies, token

    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching data from {url}: {e}")

    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
