# -*- coding: utf-8 -*-
"""CsvWriter for writing csv to files in utf-8."""

import codecs


class CsvWriter(object):
    """CsvWriter for writing csv to files in utf-8."""

    def __init__(self, csvFilepath):
        """
        Initialize CsvWriter with csvFilepath.

        Will write to the file located at csvFilepath.
        """
        self.csv_file = codecs.open(csvFilepath, "w", "utf-8")

    def write_header(self, header):
        """Write header to the file."""
        self.write_row(header)

    def write_row(self, row):
        """Write row to the file."""
        quoted_row = []
        for item in row:
            quoted_row.append(u'"%s"' % (item,))

        row_to_write = ",".join(quoted_row)
        try:
            self.csv_file.write(u"%s\n" % (row_to_write,))
        except IOError as exception:
            print(u"Failed to write to file: %s" % (str(exception),))

    def close(self):
        """Close the csv file."""
        self.csv_file.close()
