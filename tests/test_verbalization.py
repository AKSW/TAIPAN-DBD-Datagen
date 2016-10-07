"""Test verbalization for the header items."""

import os
import pytest
import sys

import opentablebench.NLTKInterface as nltk
from opentablebench.config import LOG_FOLDER
from opentablebench.FileWriter import FileWriter

@pytest.fixture
def test_data():
    return nltk.load_test_data()

def test_verbalize(test_data, capsys):
    verbalization_log_file = os.path.join(LOG_FOLDER, "verbalization.logs")
    verbalization_log = FileWriter(verbalization_log_file)

    empty_line = "\n"
    for header in test_data:
        verbalization_log.write(repr(header))
        verbalization_log.write(empty_line)
        verbalized_header = nltk.verbalize_header(header)
        verbalization_log.write(repr(verbalized_header))
        verbalization_log.write(empty_line)
        verbalization_log.write(empty_line)

    verbalization_log.close()
