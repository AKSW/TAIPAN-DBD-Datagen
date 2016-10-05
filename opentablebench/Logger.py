"""Logger is for application wide logging."""

import logging

from .config import LOG_FILE

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename=LOG_FILE,
    filemode='w'
)


def get_logger(name):
    """Get a logger with a name."""
    return logging.getLogger(name)
