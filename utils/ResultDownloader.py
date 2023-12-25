from ..config import CONNECT_TIMEOUT, READ_TIMEOUT, CHUNK_SIZE
from ..utils.SysProfiler import get_user_agent

import os
import time
from tqdm import tqdm
import logging
import requests
import urllib3

logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download(down_url, save_path, headers=None, cookies=None, stream=True, verify=False, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT), chunk_size=CHUNK_SIZE):
    """
    Downloads the file from the given URL and saves it to the specified location.

    :param down_url: The URL from which to download the file.
    :param save_path: The local file path to save the downloaded file.
    :param headers: (optional) Dictionary of HTTP headers to send with the request.
    :param cookies: (optional) Dict or CookieJar object to send with the request.
    :param stream: (optional) If True, the download is streamed. Defaults to True.
    :param verify: (optional) Whether to verify the server's TLS certificate. Defaults to False.
    :param timeout: (optional) A tuple (connect_timeout, read_timeout) in seconds.
    :param chunk_size: (optional) The chunk size of the file to download. Defaults to 1024 bytes.
    """
    if headers is None:
        headers = get_user_agent()

    request_kwargs = {
        'stream': stream,
        'timeout': timeout,
        'verify': verify,
        'headers': headers
    }
    if cookies:
        request_kwargs['cookies'] = cookies

    try:
        response = requests.get(down_url, **request_kwargs)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to start download from {down_url}. The cause of the error is {e}")
        raise

    # Check if the file exists or can be opened
    if os.path.exists(save_path):
        try:
            test = open(save_path, "wb")
            test.close()
        except IOError as e:
            error_info = f"Cannot write to the file {save_path}. Error: {e}"
            logger.error(error_info)
            raise IOError(error_info)

    data_size = int(response.headers.get('Content-Length', 0)) / 1024
    if data_size == 0:
        logger.warning("Unable to determine file size, progress bar may be inaccurate.")

    with open(save_path, mode='wb') as f:
        pbar = tqdm(
            total=data_size,        # Ensure the correct byte size
            unit='KB',              # Base unit is bytes
            unit_scale=True,        # Enable scaling
            unit_divisor=1024,      # Set divisor to 1024 for KB/MG/GB etc.
            desc='Downloading',     # Progress bar title
            ncols=100,              # Width of the progress bar
            colour='BLUE',          # Set the progress bar color to blue
        )
        for data in response.iter_content(chunk_size=chunk_size):
            size = f.write(data)
            # If the download speed is too fast, increase the delay to display the progress bar speed
            time.sleep(0.01)
            pbar.update(size / 1024)
        pbar.close()

    logger.info(f"{save_path} download complete.")
    response.close()
