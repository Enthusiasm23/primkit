from ..utils.SysProfiler import get_system_type
from ..config import DEFAULT_LINUX_USER_DATA_DIR, DEFAULT_WINDOWS_USER_DATA_DIR, \
    DEFAULT_HEADLESS, REMOTE_DEBUGGING_PORT, CHROME_DRIVER_PATH

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def get_default_chrome_options(user_data_dir=None, headless=False, remote_debugging_port=None):
    """
        配置并返回一个 ChromeOptions 实例。

        :param user_data_dir: Chrome 用户数据目录的路径。如果指定，Chrome 将使用这个目录的配置和数据。
        :param headless: 是否启用无头模式。在无头模式下，Chrome 不会显示界面。
        :param remote_debugging_port: Chrome 远程调试端口。
        :return: 配置好的 ChromeOptions 实例。
    """
    options = webdriver.ChromeOptions()

    # 基本配置
    options.add_argument('--no-sandbox')  # 在无沙盒模式下运行
    options.add_argument('--disable-infobars')  # 禁用信息栏
    options.add_argument('--incognito')  # 隐身模式
    options.add_argument("--disable-site-isolation-trials")   # 禁用站点隔离功能
    options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    options.add_argument('--disable-gpu')  # 禁用GPU加速
    options.add_argument('--disable-dev-shm-usage')  # 减少/dev/shm使用
    options.add_argument("--disable-notifications")  # 禁用通知
    options.add_argument('--disable-software-rasterizer')  # 禁用软件栅格化器
    options.add_argument('--disable-extensions')  # 禁用扩展
    options.add_argument('--disable-popup-blocking')  # 禁用弹出拦截
    options.add_argument('--profile-directory=Default')  # 使用默认用户文件夹
    options.add_argument("--disable-plugins-discovery")  # 禁用插件发现
    options.add_argument('--window-size=1920,1080')  # 设置窗口大小
    options.add_argument("--start-maximized")  # 启动时最大化
    options.add_argument('--enable-logging')   # 详细日志输出
    options.add_argument('--v=1')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 排除日志开关
    options.add_experimental_option('useAutomationExtension', False)    # 禁用Chrome的自动化扩展
    options.add_experimental_option("excludeSwitches", ["enable-automation"])   # 隐藏控制提示

    # 根据参数设置
    if user_data_dir:
        options.add_argument(f'--user-data-dir={user_data_dir}')
    if headless:
        options.add_argument('--headless')
    if remote_debugging_port:
        options.add_argument(f'--remote-debugging-port={remote_debugging_port}')

    return options


def get_chrome_driver(driver_path=None, user_data_dir=None, headless=None, remote_debugging_port=None):
    """
    创建并返回一个 Chrome WebDriver 实例。

    :param driver_path: ChromeDriver 的路径。如果指定，将使用此路径下的 ChromeDriver。
    :param user_data_dir: Chrome 用户数据目录的路径。如果指定，Chrome 将使用这个目录的配置和数据。
    :param headless: 是否启用无头模式。对于 Linux 系统，默认为 True。对于其他系统，默认为 False。
    :param remote_debugging_port: Chrome 远程调试端口。
    :return: 配置好的 Chrome WebDriver 实例。
    """
    # 判断操作系统
    system = get_system_type()

    # 设置 headless 默认值
    if system == 'linux':
        headless = True   # linux 系统默认启用无头模式
    elif headless is None:
        headless = DEFAULT_HEADLESS

    # 设置默认用户数据目录
    if user_data_dir is None:
        if system == 'Linux':
            user_data_dir = DEFAULT_LINUX_USER_DATA_DIR
        elif system == 'Windows':
            user_data_dir = DEFAULT_WINDOWS_USER_DATA_DIR

    # 设置 remote_debugging_port
    remote_debugging_port = remote_debugging_port if remote_debugging_port else REMOTE_DEBUGGING_PORT

    # 设置 Chrome 选项
    options = get_default_chrome_options(user_data_dir, headless, remote_debugging_port)

    # 设置 executable_path
    executable_path = driver_path if driver_path else CHROME_DRIVER_PATH

    # 如果 driver_path 和 CHROME_DRIVER_PATH 都未提供，使用 ChromeDriverManager 下载或获取路径
    if not executable_path:
        executable_path = ChromeDriverManager().install()

    # 创建 WebDriver 实例
    service = ChromeService(executable_path=executable_path)
    return webdriver.Chrome(service=service, options=options)
