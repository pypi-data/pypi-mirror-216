import logging
from functools import wraps
import time

loggers = {}


def setup_logger(name, log_level=logging.ERROR, log_file=None):
    """
    Set up and configure a logger with the given name.

    Args:
        name (str): Name of the logger.
        log_level (int): Log level for the logger (default: logging.ERROR).
        log_file (str): Path to the log file (optional).

    Returns:
        logging.Logger: Configured logger instance.
    """
    global loggers

    # Check if the logger already exists
    if loggers.get(name):
        return loggers.get(name)
    else:
        # Create a new logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Configure log message format
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "file_name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
        )
        console_handler.setFormatter(formatter)

        # Add console handler to the logger
        logger.addHandler(console_handler)

        # Store the logger in the dictionary for future use
        loggers[name] = logger

        return logger


def timeit(logging):
    """
    Decorator for measuring the execution time of a function.

    Args:
        logging (logging.Logger): Logger instance to log the execution time.

    Returns:
        function: Decorated function.
    """
    def operate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            logging.info(f'{func.__name__} finished in {(end - start):.2f}s')
            return result

        return wrapper

    return operate
