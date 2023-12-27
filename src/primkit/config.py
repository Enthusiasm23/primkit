import os
import logging

# Browser driver configuration
BROWSER = os.environ.get('CHROME_DRIVER_PATH', 'chrome').lower()
DEFAULT_TIMEOUT = int(os.environ.get('DEFAULT_TIMEOUT', 30))
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH', None)
DEFAULT_LINUX_USER_DATA_DIR = os.environ.get('DEFAULT_LINUX_USER_DATA_DIR', '~/.config/google-chrome')
DEFAULT_WINDOWS_USER_DATA_DIR = os.environ.get('DEFAULT_WINDOWS_USER_DATA_DIR', None)
DEFAULT_HEADLESS = os.environ.get('DEFAULT_HEADLESS', 'False').lower() in ('true', '1', 't')
REMOTE_DEBUGGING_PORT = os.environ.get('REMOTE_DEBUGGING_PORT', None)

# Test the relevant configurations
TEST_URL = os.environ.get('TEST_URL', "https://example.com")

# Security and authentication configurations
XSRF_NAME = os.environ.get('XSRF_NAME', "_xsrf")

# Log configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')  # 日志级别
LOG_FILE = os.environ.get('LOG_FILE', None)  # 日志文件路径
LOG_FORMAT = os.environ.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 日志格式
LOG_FILE_MODE = os.environ.get('LOG_FILE_MODE', 'a')  # 日志文件模式
MAX_LOG_SIZE = int(os.environ.get('MAX_LOG_SIZE', 10485760))  # 最大日志文件大小（10MB）
BACKUP_COUNT = int(os.environ.get('BACKUP_COUNT', 3))  # 保留的日志文件数量
LOG_STREAM = os.environ.get('LOG_STREAM', 'True').lower() in ('true', '1', 't')  # 是否输出日志到控制台

# Make sure that the log level is valid
if LOG_LEVEL.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    LOG_LEVEL = 'INFO'

# The conversion log level is the corresponding value in the logging module
LOG_LEVEL = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

# Primer design configuration
MFE_PRIMER = os.environ.get('MFE_PRIMER', "https://mfeprimer3.igenetech.com")
PRIMER_URL = os.environ.get('PRIMER_URL', f"{MFE_PRIMER}/muld")
SPEC_URL = os.environ.get('SPEC_URL', f"{MFE_PRIMER}/spec")
DIMER_URL = os.environ.get('DIMER_URL', f"{MFE_PRIMER}/dimer")
HAIRPIN_URL = os.environ.get('HAIRPIN_URL', f"{MFE_PRIMER}/hairpin")
MAX_RETRIES = 3
RETRY_INTERVAL = 2
CHECK_INTERVAL = 3
WAITING_TIMEOUT = 300

# Primer default parameters
PRIMER_PARAMS = {
    'DB': 'hg19.fa',        # hg19.fa/mm10.fa
    'SnpFilter': 'yes',     # yes/no
    'PrimerMinSize': '17',  # 15-35
    'PrimerOptSize': '22',  # 15-35
    'PrimerMaxSize': '25',  # 15-35
    'PrimerMinTm': '58',    # 0-100
    'PrimerOptTm': '60',    # 0-100
    'PrimerMaxTm': '62',    # 0-100
    'ProdMinSize': '80',    # 0-1000000
    'ProdMaxSize': '120',   # 0-1000000
    'DimerScore': '5',      # 3-20
    'HairpinScore': '5',    # 3-20
    'Tm': '47',             # 0-100
    'SpecMinSize': '0',     # 0-1000000
    'SpecMaxSize': '500',   # 0-1000000
}

# Parameter setting range
PARAMS_CONSTRAINTS = {
    'DB': ['hg19.fa', 'mm10.fa'],
    'SnpFilter': ['yes', 'no'],
    'PrimerMinSize': [15, 35],
    'PrimerOptSize': [15, 35],
    'PrimerMaxSize': [15, 35],
    'PrimerMinTm': [0, 100],
    'PrimerOptTm': [0, 100],
    'PrimerMaxTm': [0, 100],
    'ProdMinSize': [0, 1000000],
    'ProdMaxSize': [0, 1000000],
    'DimerScore': [3, 20],
    'HairpinScore': [3, 20],
    'Tm': [0, 100],
    'SpecMinSize': [0, 1000000],
    'SpecMaxSize': [0, 1000000],
}

# Primer number configuration
PRIMER_SET_COUNT = 20

# Download the module configuration
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 30
CHUNK_SIZE = 1024

# Read the primer result configuration
SEP = ','
HEADER = 3
DROP_END_ROWS = 1
