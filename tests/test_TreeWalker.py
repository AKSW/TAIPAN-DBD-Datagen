"""Test methods from TreeWalker package."""

import opentablebench.TreeWalker as tw

import pytest


@pytest.fixture
def example_list():
    """Load example list to permutate."""
    return [1, 2, 4]


@pytest.fixture
def example_list_big():
    """Load example list to permutate."""
    return [10, 20, 40, 15, 64, 21, 33, 84, 10, 65]


def test_build_permutation_tree(example_list):
    """Test build_permutation_tree method."""
    permutations = tw.build_permutation_tree(example_list)
    assert len(permutations) == 29


@pytest.mark.skip(reason="Overflows RAM")
def test_build_permutation_tree_big(example_list_big):
    """Test build_permutation_tree method."""
    permutations = tw.build_permutation_tree(example_list_big)
    # does not matter as this will never execute
    assert len(permutations) > 0


def test_sort_permutation_tree():
    """Test sort_permutation_tree method."""
    _list = [1, 2, 1]
    permutations = tw.build_permutation_tree(_list)
    sorted_permutations = tw.sort_permutation_tree(permutations)
    result = [[0, 0, 1],
              [0, 1, 0],
              [1, 0, 0],
              [0, 1, 1],
              [0, 2, 0],
              [1, 0, 1],
              [1, 1, 0],
              [0, 2, 1],
              [1, 1, 1],
              [1, 2, 0],
              [1, 2, 1]]
    assert result == sorted_permutations
