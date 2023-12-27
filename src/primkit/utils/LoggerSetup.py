import logging
import logging.handlers
from ..config import LOG_LEVEL, LOG_FILE, LOG_FORMAT, \
    LOG_FILE_MODE, MAX_LOG_SIZE, BACKUP_COUNT, LOG_STREAM


def setup_logging(
    level=None,
    log_file=None,
    format=None,
    log_file_mode=None,
    max_log_size=None,
    backup_count=None,
    stream=None
):
    """
    Configure logging for the application.

    :param level: The logging level, e.g., 'DEBUG', 'INFO', 'WARNING'. Defaults to value from config.py but can be overridden by user input.
    :param log_file: Path to the log file. If specified, logs will be written to the file. Defaults to value from config.py but can be overridden by user input.
    :param format: The format for the logging messages. Defaults to value from config.py but can be overridden by user input.
    :param log_file_mode: The mode for writing to the log file, e.g., 'a' for append mode. Defaults to value from config.py but can be overridden by user input.
    :param max_log_size: The maximum size of the log file in bytes. When exceeded, the log will rotate. Defaults to value from config.py but can be overridden by user input.
    :param backup_count: The number of backup log files to keep. Defaults to value from config.py but can be overridden by user input.
    :param stream: Whether to output logs to the console. Defaults to value from config.py but can be overridden by user input.

    The function uses the default configuration or configuration provided by the user. Logging can be directed to a file, console, or both based on parameters.
    """

    # Use the default configuration or user-provided configuration
    if level is not None:
        if isinstance(level, int):
            log_level = level
        else:
            log_level = getattr(logging, level.upper(), logging.INFO)
    else:
        if isinstance(LOG_LEVEL, int):
            log_level = LOG_LEVEL
        else:
            log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    log_file = log_file if log_file is not None else LOG_FILE
    format = format if format is not None else LOG_FORMAT
    log_file_mode = log_file_mode if log_file_mode is not None else LOG_FILE_MODE
    max_log_size = max_log_size if max_log_size is not None else MAX_LOG_SIZE
    backup_count = backup_count if backup_count is not None else BACKUP_COUNT
    stream = stream if stream is not None else LOG_STREAM

    # Configure the log format
    log_formatter = logging.Formatter(format)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.handlers = []  # 清除现有的处理程序

    # File handler, using the RotatingFileHandler
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, mode=log_file_mode, maxBytes=max_log_size, backupCount=backup_count
        )
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    # Console (stream) handler
    if stream or not log_file:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        logger.addHandler(stream_handler)

    return logging.getLogger(__name__)
