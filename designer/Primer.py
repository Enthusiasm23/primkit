from ..config import MFE_PRIMER, PRIMER_URL, RETRY_INTERVAL, \
    MAX_RETRIES, CHECK_INTERVAL, PRIMER_PARAMS, PARAMS_CONSTRAINTS, \
    PRIMER_SET_COUNT, WAITING_TIMEOUT
from ..utils.SiteSeleniumer import WebDriverUtility

import re
import time
import requests
from bs4 import BeautifulSoup
import logging
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def validate_parameter(parameter, value, constraints):
    """
    Validates if a single parameter value is within its constraint range.

    :param parameter: The name of the parameter to validate.
    :param value: The value of the parameter to validate.
    :param constraints: A list or tuple containing the allowed range or set of values for the parameter.
    :return: Boolean indicating whether the parameter value is valid.
    """
    logger.info(f"Validating parameter {parameter} with value {value}.")
    if parameter in ['DB', 'SnpFilter']:
        if value not in constraints:
            logger.error(f"Value for {parameter} is not within the allowed constraints.")
        return value in constraints
    elif parameter in ['PrimerMinSize', 'PrimerOptSize', 'PrimerMaxSize',
                       'PrimerMinTm', 'PrimerOptTm', 'PrimerMaxTm',
                       'ProdMinSize', 'ProdMaxSize',
                       'DimerScore', 'HairpinScore', 'Tm',
                       'SpecMinSize', 'SpecMaxSize']:
        if not (constraints[0] <= int(value) <= constraints[1]):
            logger.error(f"Value for {parameter} is not within the allowed range of {constraints}.")
        return constraints[0] <= int(value) <= constraints[1]
    else:
        return True


def validate_bed_input(bed_input, max_count=PRIMER_SET_COUNT):
    """
    Validates the format of the BedInput parameter and ensures the number of entries does not exceed the maximum count.
    The BedInput should be a string containing lines with specific chromosomes (chr1 to chr22, chrX, chrY),
    start, and end positions, separated by tabs or spaces and ending with a newline character.
    Regular expression matches lines with "chr[specific chromosome][spaces/tabs][number][spaces/tabs][number][newline]"

    :param bed_input: The input string in BED format to validate.
    :param max_count: The maximum number of entries allowed.
    :return: A tuple containing a boolean indicating if the BedInput format is correct and the processed BedInput.
    """
    logger.info("Validating the BedInput format.")

    bed_lines = bed_input.splitlines()
    if len(bed_lines) > max_count:
        logger.warning(
            f"BedInput contains more than {max_count} entries. Only the first {max_count} will be processed.")
        bed_lines = bed_lines[:max_count]  # Keep only the first 20 entries

    bed_input_pattern = re.compile(r'chr(?:[1-9]|1\d|2[0-2]|X|Y)\s+(\d+)\s+(\d+)(\r?\n|$)')

    for line in bed_lines:
        match = bed_input_pattern.match(line)
        if not match:
            logger.error(
                f"Line does not match the expected format: {line}. (Expected format: 'chr[specific chromosome][spaces/tabs][number][spaces/tabs][number][newline]').")
            return False, bed_input  # Return original bed_input for further reference

        start, end = map(int, match.groups()[:2])
        if start >= end:
            logger.error(
                f"Starting position is greater than or equal to the ending position in the line: {line}. (The ending position must be greater than the starting position by at least 1 base pair (bp).)")
            return False, bed_input

    processed_bed_input = "\n".join(bed_lines)  # Reconstruct the BedInput with potentially fewer lines
    return True, processed_bed_input


def build_data_dict(token, bed_input, custom_params=None, default_params=None):
    """
    Builds a data dictionary using default and custom parameters.

    :param token: The authentication token required for the POST request.
    :param bed_input: The BED format input containing chromosome, start, and end positions.
    :param custom_params: A dictionary of parameters provided by the user to override defaults.
    :param default_params: A dictionary of default parameters for the POST request.
    :return: A dictionary containing the combined default and custom parameters.
    """
    logger.info("Building data dictionary with parameters.")
    data = default_params.copy() if default_params else {}
    data.update(custom_params if custom_params else {})
    data['_xsrf'] = token
    data['BedInput'] = bed_input
    return data


def prepare_post_data(token, bed_input, custom_params=None, default_params=PRIMER_PARAMS,
                      constraints=PARAMS_CONSTRAINTS):
    """
    Prepares the data for a POST request by validating parameters and constructing a data dictionary.

    :param token: The authentication token required for the POST request.
    :param bed_input: The BED format input containing chromosome, start, and end positions.
    :param custom_params: Optional; A dictionary of parameters provided by the user to override defaults.
    :param default_params: Optional; A dictionary of default parameters for the POST request.
    :param constraints: Optional; A dictionary of constraints for parameter validation.
    :return: A dictionary ready to be sent in a POST request if all validations pass.
    :raises ValueError: If token is empty, BedInput format is incorrect, custom_params is not a dictionary,
                         or if any parameter is out of its constraint range.
    """
    logger.info("Preparing post data.")

    if not token:
        logger.error("Token parameter cannot be empty.")
        raise ValueError("Token parameter cannot be empty.")

    valid, processed_bed_input = validate_bed_input(bed_input)
    if not valid:
        logger.error("BedInput format is incorrect.")
        raise ValueError("BedInput format is incorrect.")

    if custom_params is not None and not isinstance(custom_params, dict):
        logger.error("Custom_params must be a dictionary.")
        raise ValueError("Custom_params must be a dictionary.")

    valid_keys = constraints.keys()
    for key in custom_params or {}:
        if key not in valid_keys:
            valid_keys_str = ', '.join(valid_keys)
            logger.error(f"Invalid parameter: {key}. Valid keys are: {valid_keys_str}")
            raise ValueError(f"Invalid parameter: {key}. Valid keys are: {valid_keys_str}")

    data = build_data_dict(token, processed_bed_input, custom_params, default_params)
    for key, value in data.items():
        if not validate_parameter(key, value, constraints.get(key, [])):
            logger.error(f"Parameter {key} with value {value} is out of constraint range.")
            raise ValueError(f"Parameter {key} with value {value} is out of constraint range.")

    logger.info("Data prepared successfully.")
    return data


def submit_and_track(data, headers, cookies, url=PRIMER_URL, root_url=MFE_PRIMER, max_retries=MAX_RETRIES,
                     retry_interval=RETRY_INTERVAL):
    """
    Sends a POST request and retrieves the task link.

    :param data: Data to be sent in the POST request.
    :param headers: Headers to be used for the request.
    :param cookies: Cookies to be used for the request.
    :param root_url: Root URL.
    :param url: URL to send the POST request.
    :param max_retries: Maximum number of retries if the task link is not found (default is RETRY_TIME).
    :param retry_interval: Time in seconds to wait before retrying.
    :return: Task link if found.
    :raises: Exception if the task link is not found after retries.
    """
    logger.info("Attempting to submit data and track task link.")
    attempts = 0
    while attempts < max_retries:
        try:
            response = requests.post(url, cookies=cookies, headers=headers, data=data)
            if response.status_code == 200:
                logger.info("POST request successful. Processing response.")
                soup = BeautifulSoup(response.text, 'html.parser')
                task_link_element = soup.find('a', href=re.compile(r'/muld/'))

                if task_link_element:
                    task_href = task_link_element.get('href')
                    task_link = f"{root_url}{task_href}"
                    logger.info(f"Task link found: {task_link}")
                    return task_link
                else:
                    logger.warning("Task link not found in response. Retrying...")
            else:
                logger.error(f"POST request failed with status code: {response.status_code}")
                break
        except requests.RequestException as e:
            logger.error(f"An error occurred while making a POST request: {e}")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break

        attempts += 1
        time.sleep(retry_interval)

    error_message = "Failed to retrieve task link after maximum retries."
    logger.error(error_message)
    raise Exception(error_message)


def check_task_status(task_url, headers, cookies, root_url=MFE_PRIMER, check_interval=CHECK_INTERVAL, max_retries=MAX_RETRIES, verify=False):
    """
    Checks the status of a specific task and retrieves the download URL upon completion.

    :param root_url: Root URL.
    :param task_url: URL to check the task status.
    :param headers: Headers to be used for the request.
    :param cookies: Cookies to be used for the request.
    :param check_interval: Interval in seconds between checks.
    :param max_retries: Maximum number of retries for checking the task status.
    :param verify: (optional) Whether to verify the server's TLS certificate. Defaults to False.
    :return: Download URL if the task is completed.
    :raises: Exception if the task link is not found or another error occurs.
    """
    logger.info(f"Checking task status for URL: {task_url}")
    retries = 0

    while True:
        try:
            response = requests.get(task_url, cookies=cookies, headers=headers, verify=verify)
            if response.status_code == 200:
                check_soup = BeautifulSoup(response.text, 'html.parser')
                status_span = check_soup.find('span', id='shuaxin')

                if status_span and status_span.text.strip() == 'Done':
                    download_link_element = check_soup.find('a', href=re.compile(r'/muld/.*?/download'))
                    if download_link_element:
                        download_url = f"{root_url}{download_link_element.get('href')}"
                        logger.info(f"File available for download: {download_url}")
                        return download_url
                elif check_soup.find('span', class_='badge badge-danger', string='Running...'):
                    logger.info('Task is still running...')
                else:
                    logger.warning('Task status is unknown. Waiting to retry...')

            else:
                logger.error(f"Failed to check task status. HTTP status code: {response.status_code}")
                raise Exception("Failed to check task status due to HTTP error.")

            time.sleep(check_interval)

        except requests.RequestException as e:
            logger.error(f"Request exception occurred: {e}")
            retries += 1
            if retries > max_retries:
                raise Exception("Max retries reached. Failed to check task status due to a request exception.") from e
            logger.info(f"Retrying... Attempt {retries}/{max_retries}")
            time.sleep(check_interval)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            retries += 1
            if retries > max_retries:
                raise Exception("Max retries reached. An unexpected error occurred while checking task status.") from e
            logger.info(f"Retrying... Attempt {retries}/{max_retries}")
            time.sleep(check_interval)

        # If the retry count exceeds the set maximum retry count, exit the loop
        if retries > max_retries:
            logger.error("Failed to complete the task status check after maximum retries.")
            break

    # If the loop exits without returning, raise an exception
    raise Exception("Failed to complete the task status check after maximum retries.")


def input_bed_data(utility, input_element, bed_data):
    """
    Inputs BED formatted data into the given input element line by line.

    :param utility: An instance of WebDriverUtility for Selenium operations.
    :param input_element: The web element where the BED data will be input.
    :param bed_data: The BED data to be entered into the input element.
    """
    for line in bed_data.splitlines():
        for value in line.split():
            utility.input_element(input_element, value)
            time.sleep(0.1)
            utility.input_element(input_element, Keys.SHIFT, Keys.SPACE)
        utility.input_element(input_element, Keys.RETURN)


def get_download_link(utility, check_interval=CHECK_INTERVAL, timeout=WAITING_TIMEOUT):
    """
    Retrieves the URL of the download link for primer results, waiting until it's available or the timeout is reached.

    :param utility: An instance of WebDriverUtility for Selenium operations.
    :param check_interval: Interval in seconds between checks.
    :param timeout: Total time in seconds to wait before timing out.
    :return: Download URL if the task is completed.
    :raises: Exception if the task does not complete within the specified timeout.
    """
    logger.info("Waiting for the primer design task to complete...")
    start_time = time.time()
    while True:
        try:
            # Check for the 'Done' indicator
            utility.find_element(by=By.XPATH,
                                 value='//span[contains(@class, "badge badge-success") and contains(text(), "Done")]')

            # Once 'Done' is detected, get the download link URL
            download_url = utility.get_element_attribute('span[class="badge badge-success"]+a', 'href')
            logger.info(f"Primer design completed. Download link: {download_url}")
            return download_url
        except NoSuchElementException:
            logger.info('Task is still running...')
            # Check if the timeout has been reached
            if time.time() - start_time > timeout:
                error_info = f"Timeout reached: Primer design did not complete within {timeout} seconds."
                logger.error(error_info)
                raise Exception(error_info)

            # Wait before checking again
            time.sleep(check_interval)


def simulate_primer_fetch(data, url=PRIMER_URL, max_retries=MAX_RETRIES, retry_interval=RETRY_INTERVAL):
    """
    Designs primers using Selenium by interacting with the specified website.

    :param url: URL of the primer design web page.
    :param data: Data to be inputted for primer design.
    :param max_retries: Maximum number of retries.
    :param retry_interval: Time in seconds to wait before retrying.
    :return: Download URL if the task is completed.
    """
    retries = 0
    while retries <= max_retries:
        try:
            # Initialize WebDriverUtility and navigate to the URL
            utility = WebDriverUtility(url)
            utility.load_url()

            # Input BED data
            if utility.ensure_element('#BedInput'):
                input_element = utility.find_element(by=By.CSS_SELECTOR, value='#BedInput')
                utility.click_element(input_element)
                input_bed_data(utility, input_element, data['BedInput'])
            else:
                raise Exception("The BedInput element was not found on the page.")

            # Select options from dropdowns
            utility.select_dropdown_option('select[name="DB"]', data['DB'])
            utility.select_dropdown_option('select[name="SnpFilter"]', data['SnpFilter'])

            # Input values for various primer and product properties
            field_mapping = {
                '#PrimerMinSize': 'PrimerMinSize',
                '#PrimerOptSize': 'PrimerOptSize',
                '#PrimerMaxSize': 'PrimerMaxSize',
                '#PrimerMinTm': 'PrimerMinTm',
                '#PrimerOptTm': 'PrimerOptTm',
                '#PrimerMaxTm': 'PrimerMaxTm',
                '#ProdMinSize': 'ProdMinSize',
                '#ProdMaxSize': 'ProdMaxSize',
                '#DimerScoreID': 'DimerScore',
                '#HairpinScoreID': 'HairpinScore',
                '#TmID': 'Tm',
                '#SpecMinSize': 'SpecMinSize',
                '#SpecMaxSize': 'SpecMaxSize'
            }
            input_fields = list(field_mapping.keys())
            for field in input_fields:
                utility.input_values((By.CSS_SELECTOR, field), data[field_mapping[field]])

            # Submit the form
            if utility.ensure_element('button[type="submit"]'):
                submit_button = utility.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]')
                utility.click_element(submit_button)
            else:
                raise Exception("Submit button not found on the page.")

            # Wait for page to load and then refresh
            utility.ensure_loaded()
            utility.refresh_page()

            # Check for completion and get the result URL
            if utility.ensure_element(
                    '//span[contains(@class, "badge badge-danger") and contains(text(), "Running...")]', by=By.XPATH):
                # Submit successfully, then obtain the download link
                download_url = get_download_link(utility)
                return download_url
            else:
                raise Exception("Submission did not start successfully or 'Running...' status was not found.")

        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise Exception(f"Max retries reached. Last error: {e}")
            time.sleep(retry_interval)
            # Optionally, log the retry attempt
            logging.info(f"Retrying... Attempt {retries}/{max_retries}")

    raise Exception("Failed to complete the primer fetch process after maximum retries.")


def design_primers(data, method='requests', headers=None, cookies=None):
    """
    Main function to design primers and retrieve the download URL for the results.

    :param data: Data to be sent in the POST request.
    :param method: The method to perform the operations ('requests' or 'selenium').
    :param headers: Headers to be used for the request. Required if method is 'requests'.
    :param cookies: Cookies to be used for the request. Required if method is 'requests'.
    :return: The URL to download the primer design results.
    """
    if method == 'requests':
        if headers is None or cookies is None:
            raise ValueError("Headers and cookies are required for requests method.")
        task_url = submit_and_track(data, headers, cookies)
        return check_task_status(task_url, headers, cookies)
    elif method == 'selenium':
        return simulate_primer_fetch(data)
    else:
        raise ValueError("Invalid method specified. Choose 'requests' or 'selenium'.")
