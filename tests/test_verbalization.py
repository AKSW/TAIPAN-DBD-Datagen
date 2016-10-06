"""Test verbalization for the header items."""

import pytest
import sys

import opentablebench.NLTKInterface as nltk

@pytest.fixture
def test_data():
    return nltk.load_test_data()

def test_verbalize(test_data, capsys):
    max_complexity = 1
    for header in test_data:
        print("Original header")
        print(header)

        verbalized_header = nltk.verbalize_header(header)
        print("Verbalized header")
        print(verbalized_header)
        pytest.set_trace()
