"""Logger is for application wide logging."""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M'
)


def get_logger(name):
    """Get a logger with a name."""
    return logging.getLogger(name)
