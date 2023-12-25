from ..config import LOG_LEVEL, LOG_FILE, LOG_FORMAT, LOG_FILE_MODE, MAX_LOG_SIZE, BACKUP_COUNT, LOG_STREAM

import logging
import logging.handlers


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
        设置日志记录。

        :param level: 日志级别，例如 'DEBUG', 'INFO', 'WARNING'。默认从 config.py 获取，可被用户输入覆盖。
        :param log_file: 日志文件的路径。如果指定，日志将被写入文件。默认从 config.py 获取，可被用户输入覆盖。
        :param format: 日志格式。默认从 config.py 获取，可被用户输入覆盖。
        :param log_file_mode: 写入日志文件的模式，例如 'a' 为追加模式。默认从 config.py 获取，可被用户输入覆盖。
        :param max_log_size: 日志文件的最大大小（以字节为单位）。超过此大小，日志将被轮换。默认从 config.py 获取，可被用户输入覆盖。
        :param backup_count: 保留的日志文件个数。默认从 config.py 获取，可被用户输入覆盖。
        :param stream: 是否在控制台输出日志。默认从 config.py 获取，可被用户输入覆盖。
    """

    # 使用默认配置或用户提供的配置
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

    # 配置日志格式
    log_formatter = logging.Formatter(format)

    # 获取根日志记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.handlers = []  # 清除现有的处理程序

    # 文件处理程序，使用RotatingFileHandler
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, mode=log_file_mode, maxBytes=max_log_size, backupCount=backup_count
        )
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    # 控制台（流）处理程序
    if stream or not log_file:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        logger.addHandler(stream_handler)

    return logging.getLogger(__name__)
