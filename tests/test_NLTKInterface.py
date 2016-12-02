"""Test methods from NLTKInterface package."""

import opentablebench.NLTKInterface as nltk

import pytest


@pytest.fixture
def header():
    """Load header fixture."""
    return ['label', 'type', 'subject', 'homepage', 'foundation']


def test_get_header_synsets(header):
    """Test get_header_synsets method."""
    synset_packs = nltk.get_header_synsets(header)
    for index, synset_pack in enumerate(synset_packs):
        (label, synsets) = synset_pack
        assert header[index] == label
        assert isinstance(synsets, list)


@pytest.fixture
def synset_packs():
    """Load header fixture."""
    header = ['label', 'type', 'subject', 'homepage', 'foundation']
    return nltk.get_header_synsets(header)


def test_build_weighted_graph(synset_packs):
    """Test build_weigthed_graph method."""
    synset_graph = nltk.build_weighted_graph(synset_packs)
    number_of_nodes = len(synset_packs)
    number_of_edges = number_of_nodes * (number_of_nodes - 1) / 2
    assert len(synset_graph) == number_of_edges
    for edge in synset_graph:
        assert len(edge) != 0


@pytest.fixture
def synset_graph():
    """Load synset graph fixture."""
    header = ['label', 'type', 'subject', 'homepage', 'foundation']
    synset_packs = nltk.get_header_synsets(header)
    return nltk.build_weighted_graph(synset_packs)


@pytest.fixture
def subgraph_does_not_converge():
    """
    Load synset subgraph fixture.

    This subgraph is not complete.
    """
    return [('label', 'type'),
            ('label', 'topic'),
            ('label', 'homepage'),
            ('label', 'basis'),
            ('type', 'subject'),
            ('type', 'homepage'),
            ('type', 'initiation'),
            ('topic', 'homepage'),
            ('discipline', 'initiation'),
            ('homepage', 'foundation')]


@pytest.fixture
def subgraph_converge():
    """
    Load synset subgraph fixture.

    This subgraph is complete.
    """
    return [('label', 'type'),
            ('label', 'subject'),
            ('label', 'homepage'),
            ('label', 'foundation'),
            ('type', 'subject'),
            ('type', 'homepage'),
            ('type', 'foundation'),
            ('subject', 'homepage'),
            ('subject', 'foundation'),
            ('homepage', 'foundation')]


def test_is_graph_converge_fail(subgraph_does_not_converge):
    """
    Test is_graph_converge method.

    Subgraph should not converge.
    """
    is_converge = nltk.is_graph_converge(subgraph_does_not_converge, 5)
    assert is_converge is False


def test_is_graph_converge_pass(subgraph_converge):
    """
    Test is_graph_converge method.

    Subgraph should converge.
    """
    is_converge = nltk.is_graph_converge(subgraph_converge, 5)
    assert is_converge is True


def test_build_permutation_tree():
    """Test build_permutation_tree method."""
    _list = [1, 2, 4]
    permutations = nltk.build_permutation_tree(_list)
    assert len(permutations) == 29


def test_sort_permutation_tree():
    """Test sort_permutation_tree method."""
    _list = [1, 2, 1]
    permutations = nltk.build_permutation_tree(_list)
    sorted_permutations = nltk.sort_permutation_tree(permutations)
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
