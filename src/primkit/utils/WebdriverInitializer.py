from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from ..utils.SysProfiler import get_system_type
from ..config import DEFAULT_LINUX_USER_DATA_DIR, DEFAULT_WINDOWS_USER_DATA_DIR, \
    DEFAULT_HEADLESS, REMOTE_DEBUGGING_PORT, CHROME_DRIVER_PATH


def get_default_chrome_options(user_data_dir=None, headless=False, remote_debugging_port=None):
    """
    Configure and return an instance of ChromeOptions.

    :param user_data_dir: Path to the Chrome user data directory. If specified, Chrome will use the configurations and data from this directory.
    :param headless: Whether to enable headless mode. In headless mode, Chrome runs without a visible interface.
    :param remote_debugging_port: Port for Chrome's remote debugging.
    :return: Configured instance of ChromeOptions.
    """
    options = webdriver.ChromeOptions()

    # Basic configuration
    options.add_argument('--no-sandbox')  # Run in no sandbox mode
    options.add_argument('--disable-infobars')  # Disable infobars
    options.add_argument('--incognito')  # Incognito mode
    options.add_argument("--disable-site-isolation-trials")  # Disable site isolation
    options.add_argument('--ignore-certificate-errors')  # Ignore certificate errors
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--disable-dev-shm-usage')  # Reduce /dev/shm usage
    options.add_argument("--disable-notifications")  # Disable notifications
    options.add_argument('--disable-software-rasterizer')  # Disable software rasterizer
    options.add_argument('--disable-extensions')  # Disable extensions
    options.add_argument('--disable-popup-blocking')  # Disable pop-up blocking
    options.add_argument('--profile-directory=Default')  # Use the default profile directory
    options.add_argument("--disable-plugins-discovery")  # Disable plugin discovery
    options.add_argument('--window-size=1920,1080')  # Set window size
    options.add_argument("--start-maximized")  # Start maximized
    options.add_argument('--enable-logging')  # Enable detailed logging
    options.add_argument('--v=1')  # Set logging verbosity level to 1
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Exclude logging switches
    options.add_experimental_option('useAutomationExtension', False)  # Disable Chrome's automation extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Hide automation control prompts

    # Set according to the parameters
    if user_data_dir:
        options.add_argument(f'--user-data-dir={user_data_dir}')
    if headless:
        options.add_argument('--headless')
    if remote_debugging_port:
        options.add_argument(f'--remote-debugging-port={remote_debugging_port}')

    return options


def get_chrome_driver(driver_path=None, user_data_dir=None, headless=None, remote_debugging_port=None):
    """
    Create and return an instance of the Chrome WebDriver.

    :param driver_path: Path to the ChromeDriver. If specified, the ChromeDriver at this path will be used.
    :param user_data_dir: Path to the Chrome user data directory. If specified, Chrome will use the configurations and data from this directory.
    :param headless: Whether to enable headless mode. Defaults to True for Linux systems and False for other systems.
    :param remote_debugging_port: Port for Chrome's remote debugging.
    :return: Configured instance of the Chrome WebDriver.
    """
    # Determine the operating system
    system = get_system_type()

    # Set the headless default
    if system == 'linux':
        headless = True   # Linux systems have headless mode enabled by default
    elif headless is None:
        headless = DEFAULT_HEADLESS

    # Set the default user data directory
    if user_data_dir is None:
        if system == 'Linux':
            user_data_dir = DEFAULT_LINUX_USER_DATA_DIR
        elif system == 'Windows':
            user_data_dir = DEFAULT_WINDOWS_USER_DATA_DIR

    # Set up remote_debugging_port
    remote_debugging_port = remote_debugging_port if remote_debugging_port else REMOTE_DEBUGGING_PORT

    # Set Chrome options
    options = get_default_chrome_options(user_data_dir, headless, remote_debugging_port)

    # Set up executable_path
    executable_path = driver_path if driver_path else CHROME_DRIVER_PATH

    # If neither driver_path nor CHROME_DRIVER_PATH are provided, use ChromeDriverManager to download or get the path
    if not executable_path:
        executable_path = ChromeDriverManager().install()

    # Create a WebDriver instance
    service = ChromeService(executable_path=executable_path)
    return webdriver.Chrome(service=service, options=options)
