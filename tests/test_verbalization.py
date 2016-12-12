"""Test verbalization for the header items."""

import os
import time

from opentablebench.config import LOG_FOLDER
from opentablebench.FileWriter import FileWriter
import opentablebench.NLTKInterface as nltk

import pytest


@pytest.fixture
def test_data():
    """Load test data fixture."""
    return nltk.load_test_data()


@pytest.mark.skip(reason="done, see logs")
def test_verbalize_header_naive(test_data, capsys):
    """Test naive verbalization from NLTKInterface."""
    verbalization_log_file = os.path.join(
        LOG_FOLDER,
        "verbalization_naive.logs"
    )
    verbalization_log = FileWriter(verbalization_log_file)
    verbalization_log_time_file = os.path.join(
        LOG_FOLDER,
        "verbalization_naive_time.logs"
    )
    verbalization_log_time = FileWriter(verbalization_log_time_file)

    start_time = time.time()
    empty_line = "\n"
    for header in test_data:
        verbalization_log.write(repr(header))
        verbalization_log.write(empty_line)
        verbalized_header = nltk.verbalize_header_naive(header)
        verbalization_log.write(repr(verbalized_header))
        verbalization_log.write(empty_line)
        verbalization_log.write(empty_line)
    end_time = time.time()
    verbalization_log_time.write("%s" % (end_time - start_time))

    verbalization_log.close()
    verbalization_log_time.close()


@pytest.mark.skip(reason="done, see logs")
def test_verbalize_header_random(test_data, capsys):
    """Test verbalization from NLTKInterface."""
    verbalization_log_file = os.path.join(
        LOG_FOLDER,
        "verbalization_random_1.logs"
    )
    verbalization_log = FileWriter(verbalization_log_file)
    verbalization_log_time_file = os.path.join(
        LOG_FOLDER,
        "verbalization_random_time_1.logs"
    )
    verbalization_log_time = FileWriter(verbalization_log_time_file)
    error_log_file = os.path.join(
        LOG_FOLDER,
        "verbalization_random_error.logs"
    )
    error_log = FileWriter(error_log_file)

    start_time = time.time()
    empty_line = "\n"
    for index, header in enumerate(test_data):
        verbalization_log.write(repr(header))
        verbalization_log.write(empty_line)
        try:
            verbalized_header = nltk.verbalize_header_random(header)
            verbalization_log.write(repr(verbalized_header))
            verbalization_log.write(empty_line)
            verbalization_log.write(empty_line)
        except:
            error_log.write(repr(header))
            continue
    end_time = time.time()
    verbalization_log_time.write("%s" % (end_time - start_time))

    verbalization_log.close()
    verbalization_log_time.close()


def test_verbalize_header_palmetto(test_data, capsys):
    """Test verbalization from NLTKInterface."""
    verbalization_log_file = os.path.join(
        LOG_FOLDER,
        "verbalization_palmetto.logs"
    )
    verbalization_log = FileWriter(verbalization_log_file)
    verbalization_log_time_file = os.path.join(
        LOG_FOLDER,
        "verbalization_palmetto_time.logs"
    )
    verbalization_log_time = FileWriter(verbalization_log_time_file)

    start_time = time.time()
    empty_line = "\n"
    for header in test_data:
        verbalization_log.write(repr(header))
        verbalization_log.write(empty_line)
        verbalized_header = nltk.verbalize_header_palmetto(header)
        verbalization_log.write(repr(verbalized_header))
        verbalization_log.write(empty_line)
        verbalization_log.write(empty_line)
    end_time = time.time()
    verbalization_log_time.write("%s" % (end_time - start_time))

    verbalization_log.close()
    verbalization_log_time.close()
