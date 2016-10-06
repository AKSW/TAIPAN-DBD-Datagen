# -*- coding: utf-8 -*-
"""FileWriter for writing strings to files in utf-8."""

import codecs

from .Logger import get_logger

LOGGER = get_logger(__name__)


class FileWriter(object):
    """FileWriter for writing strings to files in utf-8."""

    def __init__(self, filepath):
        """
        Initialize FileWriter with filepath.

        Will write to the file located at filepath.
        """
        self.file = codecs.open(filepath, "w", "utf-8")

    def write(self, string):
        """Write string to the file."""
        try:
            self.file.write(string)
        except IOError as exception:
            LOGGER.error(u"Failed to write to file: %s", str(exception))

    def close(self):
        """Close the csv file."""
        self.file.close()
