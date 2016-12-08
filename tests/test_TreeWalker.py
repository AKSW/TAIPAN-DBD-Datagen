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


def test_get_distribution_permutations():
    distributions = set([
        (3,0,0,0),
        (2,1,0,0),
        (1,1,1,0)])

    distributions_sorted = sorted(distributions)
    distribution = distributions_sorted.pop()

    permutations = list(tw.get_distribution_permutations(distribution))
    assert (3,0,0,0) in permutations
    assert (0,3,0,0) in permutations
    assert (0,0,3,0) in permutations
    assert (0,0,0,3) in permutations


@pytest.mark.skip(reason="Does not work as I like it")
def test_distribute_weight_recursive():
    assert [[]] == list(tw.distribute_weight_recursive(0, 0))
    assert [[0]] == list(tw.distribute_weight_recursive(0, 1))
    assert [[0,0]] == list(tw.distribute_weight_recursive(0, 2))
    assert [
        [3,0,0,0],
        [2,1,0,0],
        [1,1,1,0]] == list(tw.distribute_weight_recursive(3, 4))
    assert [
        [5,0,0,0],
        [4,1,0,0],
        [3,2,0,0],
        [3,1,1,0],
        [2,2,1,0],
        [2,1,1,1]] == list(tw.distribute_weight_recursive(5, 4))
    assert [
        [8,0,0,0,0],
        [7,1,0,0,0],
        [6,2,0,0,0],
        [6,1,1,0,0],
        [5,3,0,0,0],
        [5,2,1,0,0],
        [5,1,1,1,0],
        [4,4,0,0,0],
        [4,3,1,0,0],
        [4,2,2,0,0],
        [4,2,1,1,0],
        [4,1,1,1,1],
        [3,3,2,0,0],
        [3,3,1,1,0],
        [3,2,1,1,1],
        [3,2,2,1,0],
        [2,2,2,2,0],
        [2,2,2,1,1],
        ] == list(tw.distribute_weight_recursive(8, 5))
    assert [
        [5,0,0],
        [4,1,0],
        [3,2,0],
        [3,1,1],
        [2,2,1],
        ] == list(tw.distribute_weight_recursive(5, 3))
    assert [
        [5,0],
        [4,1],
        [3,2]
        ] == list(tw.distribute_weight_recursive(5, 2))

def test_distribute_weight():
    with pytest.raises(Exception):
        tw.distribute_weight(0, 0)
    assert set([(0)]) == tw.distribute_weight(0, 1)
    assert set([(0,0)]) == tw.distribute_weight(0, 2)
    assert set([
        (3,0,0,0),
        (2,1,0,0),
        (1,1,1,0)]) == tw.distribute_weight(3, 4)
    assert set([
        (5,0,0,0),
        (4,1,0,0),
        (3,2,0,0),
        (3,1,1,0),
        (2,2,1,0),
        (2,1,1,1)]) == tw.distribute_weight(5, 4)
    assert set([
        (8,0,0,0,0),
        (7,1,0,0,0),
        (6,2,0,0,0),
        (6,1,1,0,0),
        (5,3,0,0,0),
        (5,2,1,0,0),
        (5,1,1,1,0),
        (4,4,0,0,0),
        (4,3,1,0,0),
        (4,2,2,0,0),
        (4,2,1,1,0),
        (4,1,1,1,1),
        (3,3,2,0,0),
        (3,3,1,1,0),
        (3,2,1,1,1),
        (3,2,2,1,0),
        (2,2,2,2,0),
        (2,2,2,1,1),
        ]) == tw.distribute_weight(8, 5)
    assert set([
        (5,0,0),
        (4,1,0),
        (3,2,0),
        (3,1,1),
        (2,2,1),
        ]) == tw.distribute_weight(5, 3)
    assert set([
        (5,0),
        (4,1),
        (3,2)
        ]) == tw.distribute_weight(5, 2)
