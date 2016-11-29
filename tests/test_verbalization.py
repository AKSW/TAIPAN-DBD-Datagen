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


@pytest.mark.skip(reason="Naive approach works fine. Skip for now.")
def test_verbalize_header_naive(test_data, capsys):
    """Test naive verbalization from NLTKInterface."""
    verbalization_log_file = os.path.join(
        LOG_FOLDER,
        "verbalization_naive.logs"
    )
    verbalization_log = FileWriter(verbalization_log_file)

    empty_line = "\n"
    for header in test_data:
        verbalization_log.write(repr(header))
        verbalization_log.write(empty_line)
        verbalized_header = nltk.verbalize_header_naive(header)
        verbalization_log.write(repr(verbalized_header))
        verbalization_log.write(empty_line)
        verbalization_log.write(empty_line)

    verbalization_log.close()


@pytest.mark.skip(reason="Naive approach works fine. Skip for now.")
def test_verbalize_header_palmetto(test_data, capsys):
    """Test verbalization from NLTKInterface."""
    verbalization_log_file = os.path.join(
        LOG_FOLDER,
        "verbalization_palmetto.logs"
    )
    verbalization_log = FileWriter(verbalization_log_file)

    empty_line = "\n"
    for header in test_data:
        verbalization_log.write(repr(header))
        verbalization_log.write(empty_line)
        verbalized_header = nltk.cluster_header_random(header)
        verbalization_log.write(repr(verbalized_header))
        verbalization_log.write(empty_line)
        verbalization_log.write(empty_line)

    verbalization_log.close()
