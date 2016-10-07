"""Test verbalization for the header items."""

import os
from opentablebench.config import LOG_FOLDER
from opentablebench.FileWriter import FileWriter
import opentablebench.NLTKInterface as nltk
import pytest


@pytest.fixture
def test_data():
    """Load test data fixture."""
    return nltk.load_test_data()


def test_verbalize(test_data, capsys):
    """Test verbalization from NLTKInterface."""
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
