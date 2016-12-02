"""Test methods from NLTKInterface package."""

import os

from opentablebench.config import LOG_FOLDER
from opentablebench.FileWriter import FileWriter
import opentablebench.NLTKInterface as nltk

import pytest


@pytest.fixture
def header():
    """Load header fixture."""
    return ['label', 'type', 'subject', 'homepage', 'foundation']


def test_get_header_synsets(header):
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


def test_pick_first_subgraph(synset_graph):
    edges_length_list = list(map(lambda x: len(x), synset_graph))
    (subgraph, state) = nltk.pick_next_subgraph(
        synset_graph,
        [],
        edges_length_list
    )
    assert len(subgraph) == len(edges_length_list)


@pytest.fixture
def subgraph_does_not_converge():
    """Load synset subgraph fixture."""
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
    """Load synset subgraph fixture."""
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
    is_converge = nltk.is_graph_converge(subgraph_does_not_converge, 5)
    assert is_converge is False


def test_is_graph_converge_pass(subgraph_converge):
    is_converge = nltk.is_graph_converge(subgraph_converge, 5)
    assert is_converge is True


def test_build_permutation_tree():
    _list = [1, 2, 4]
    permutations = nltk.build_permutation_tree(_list)
    assert len(permutations) == 29


def test_sort_permutation_tree():
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


def test_pick_subgraph(synset_graph, capsys):
    log_file = os.path.join(LOG_FOLDER, "graph.log")
    log = FileWriter(log_file)

    edges_length_list = list(map(lambda x: len(x) - 1, synset_graph))
    (subgraph, state) = nltk.pick_next_subgraph(
        synset_graph,
        [],
        edges_length_list
    )
    while True:
        if nltk.is_graph_converge(subgraph, 5):
            break
        (subgraph, state) = nltk.pick_next_subgraph(
            synset_graph,
            state,
            edges_length_list
        )
        log.write(repr(subgraph))
        log.write("\n")
        log.write(repr(state))
        log.write("\n")
        log.write("\n")
        if state == edges_length_list:
            break
