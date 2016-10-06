# -*- coding: utf-8 -*-
"""FileReader for reading files in utf-8."""


import codecs

from .Logger import get_logger

LOGGER = get_logger(__name__)


class FileReader(object):
    """FileReader for reading files in utf-8."""

    def __init__(self, filepath):
        """Initialize FileReader with filepath."""
        try:
            self.file = codecs.open(filepath, "r", "utf-8")
        except BaseException as exception:
            LOGGER.error(
                "File read error at %s: %s",
                filepath,
                str(exception)
            )

    def readlines(self):
        """Read the entire file."""
        return self.file.readlines()

    def close(self):
        """Close the csv file."""
        self.file.close()
