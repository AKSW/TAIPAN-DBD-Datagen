"""NLTKInterface for NLP related tasks."""

import operator
import random
import re

from nltk.corpus import wordnet as wn  # pylint: disable=import-error
from palmettopy.palmetto import Palmetto  # pylint: disable=import-error

from .config import TABLE_HEADERS_FILE
from .FileReader import FileReader
from .Logger import get_logger

LOGGER = get_logger(__name__)


def get_header_synsets(header):
    """
    Return synsets for each header item.

    The format is [("header item1", [synset1, synset2]), ...]
    """
    synsets_header_pack = []
    for item in header:
        # if item is several words -- get synsets for all of those
        synsets = []
        subitems = []
        # split by space first
        subitems = _split_header_item_spaces(item)
        # if empty split by camelcase
        if len(subitems) == 1:
            subitems = _split_header_item_camelcase(item)
        for subitem in subitems:
            synsets.extend(wn.synsets(subitem, pos='n'))
        synsets_header_pack.append((item, synsets))
    return _prune_header_synsets(synsets_header_pack)


def _prune_header_synsets(synsets_header_pack):
    pruned_synsets_header_pack = []
    for (label, synsets) in synsets_header_pack:
        distinct_synsets = set()
        for synset in synsets:
            synset_name = synset.name().split(".")[0]
            distinct_synsets.add(synset_name)
        pruned_synsets = []
        while distinct_synsets:
            for synset in synsets:
                synset_name = synset.name().split(".")[0]
                if synset_name in distinct_synsets:
                    distinct_synsets.remove(synset_name)
                    pruned_synsets.append(synset)
        pruned_synsets_header_pack.append((label, pruned_synsets))

    return pruned_synsets_header_pack


def _split_header_item_camelcase(string):
    _camel_case_regex = re.compile(r"([A-Z])")
    _token_list = _camel_case_regex.split(string)

    _word_list = [_token_list[0]]
    for i, _ in enumerate(_token_list):
        if i % 2 == 1:
            word = "".join([_token_list[i], _token_list[i + 1]])
            _word_list.append(word)

    return _word_list


def _split_header_item_spaces(string):
    """Clean and split header into an array of strings."""
    split_by_space = re.compile(r"[\s]+")
    header_items = split_by_space.split(string)
    return map(
        _filter_non_print_chars,
        header_items
    )


def _filter_non_print_chars(string):
    pattern = re.compile(r"[\W_]+")
    return pattern.sub('', string)


def cluster_header():
    """
    Find clusters for synsets_header_pack.

    Cluster synsets of a header based on the similarity
    between synsets of different columns.
    Number of clusters is equal to the minimum number of synsets
    for a column. That is if column "city" got 2 synsets and all other
    columns have > 2 synsets, there will be exactly 2 clusters.
    In case when column has no synsets, it is not considered in clustering
    and just attached to the resulting cluster at the end of calculation.
    """
    pass


def cluster_header_random(header):
    """
    Cluster synsets using palmetto.

    Randomly select permutation of the header and
    calculate coherence. Repeat until algorithm converges.
    """
    palmetto = Palmetto()
    synsets_pack = get_header_synsets(header)

    window_size = 3
    window = []
    maximum_coherence = 0
    index = 0
    no_change = 0
    best_permutation = []
    while True:
        random_permutation = _pick_random_synset_permutation(synsets_pack)
        coherence = palmetto.get_coherence(random_permutation)
        window.append(
            (
                random_permutation,
                coherence
            )
        )

        if index % window_size == 0:
            (local_best_permutation, local_maximum_coherence) = max(
                window,
                key=lambda x: x[1]
            )
            if local_maximum_coherence > maximum_coherence:
                maximum_coherence = local_maximum_coherence
                best_permutation = local_best_permutation
            else:
                no_change = no_change + 1
            window = []

        if no_change > 2:
            break

        index = index + 1
    return best_permutation


def _pick_random_synset_permutation(synsets_pack):
    permutation = []
    for (_, synsets) in synsets_pack:
        _random_element = random.choice(synsets).name().split(".")[0]
        permutation.append(_random_element)

    return permutation


def cluster_header_naive(header):
    """
    Cluster synsets by maximum similarity.

    The problem is that it might get stuck in a local maximum.
    To overcome the problem it is necessary to employ more sophisticated
    clustering methods.
    """
    synsets_pack = get_header_synsets(header)
    (minimal_column, minimum_synsets) = _pick_minimal_column(synsets_pack)

    # fix the minimum column
    verbalized_headers = []
    for minimal_column_item in range(0, minimum_synsets):
        (_item, _synsets) = synsets_pack[minimal_column]
        _synset = _synsets[minimal_column_item]

        # find the shortest path to each column
        shortest_path = []
        shortest_path.append(
            (_convert_synset_to_header_item(_synset), minimal_column)
        )
        evaluated_columns = []
        evaluated_columns.append(minimal_column)
        next_synset = _synset
        (shortest_path, total_similarity) = _find_shortest_path(
            synsets_pack,
            next_synset,
            evaluated_columns,
            header,
            shortest_path
        )

        shortest_path = sorted(shortest_path, key=lambda x: x[1])
        verbalized_header = map(lambda x: x[0], shortest_path)
        verbalized_headers.append(
            (
                verbalized_header,
                total_similarity,
                len(evaluated_columns)
            )
        )
    return verbalized_headers


def _pick_minimal_column(synsets_pack):
    # Pick the column with minimum synsets
    minimal_column = 0
    minimum_synsets = 1000
    for index, synset_pack in enumerate(synsets_pack):
        (_, synsets) = synset_pack
        if len(synsets) > 0\
                and len(synsets) < minimum_synsets:
            minimum_synsets = len(synsets)
            minimal_column = index
    return (minimal_column, minimum_synsets)


def _find_shortest_path(
        synsets_pack,
        next_synset,
        evaluated_columns,
        header,
        shortest_path):
    total_similarity = 0
    while True:
        similarity_pairs = []
        for index, synset_pack in enumerate(synsets_pack):
            # skip evaluated columns
            if index in evaluated_columns:
                continue
            (_, synsets) = synset_pack
            closest_pair = _find_closest_synsets(
                [next_synset],
                synsets,
                index
            )
            similarity_pairs.append(closest_pair)

        # pick the closest element
        (closest_pair, similarity, index) = sorted(
            similarity_pairs,
            key=lambda x: x[1],
            reverse=True
        )[0]
        total_similarity += similarity

        if closest_pair == ():
            for index in range(0, len(header)):
                if index not in evaluated_columns:
                    shortest_path.append((header[index], index))
            break

        next_synset = closest_pair[1]
        shortest_path.append(
            (_convert_synset_to_header_item(next_synset), index)
        )

        evaluated_columns.append(index)
        if len(evaluated_columns) == len(synsets_pack):
            break
    return (shortest_path, total_similarity)


def _convert_synset_to_header_item(synset):
    return " ".join(synset.name().split(".")[0].split("_"))


def verbalize_header_naive(header):
    """Verbalize header items."""
    verbalized_headers = cluster_header_naive(header)
    top_header = sorted(
        verbalized_headers,
        key=operator.itemgetter(1, 2)
    )[0][0]

    return top_header


def verbalize_header_random(header):
    """Verbalize header using random algorithm."""
    return cluster_header_random(header)


def verbalize_header_palmetto(header):
    """Verbalize header using random algorithm."""
    # TODO: https://goo.gl/d5pFtY
    # TODO: http://palmetto.aksw.org/palmetto-webapp/service/df?words=cat+dog
    return cluster_header_random(header)


def verbalize_header(header):
    """Verbalize header using default algorithm."""
    return verbalize_header_random(header)


def _find_closest_synsets(synsets_1, synsets_2, index):
    closest_pair = ()
    max_similarity = 0
    if synsets_1 == [] or synsets_2 == []:
        return (closest_pair, 0, index)
    for _synset_1 in synsets_1:
        for _synset_2 in synsets_2:
            similarity = _calculate_similarity(_synset_1, _synset_2)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_pair = (_synset_1, _synset_2)
    return (closest_pair, similarity, index)


def _calculate_similarity(synset_1, synset_2):
    similarity = synset_1.path_similarity(synset_2)
    if similarity is None:
        return 0
    else:
        return similarity


def load_test_data():
    """Load test headers from CSV file."""
    table_headers_file = FileReader(TABLE_HEADERS_FILE)
    table_headers = table_headers_file.readlines()
    # pylint: disable=unnecessary-lambda
    table_headers = map(lambda x: x.strip(), table_headers)
    # pylint: disable=eval-used
    table_headers = map(lambda x: eval(x), table_headers)
    return table_headers


def get_max_complexity_naive():
    """
    Calculate amount of combinations for the header permutations.

    i.e. if header is ["country", "city", "population"] and the synsets
    got [5, 6, 10] elements, then the complexity will be 5*6*10
    Max complexity is: 1120863744000
    """
    table_headers = load_test_data()
    maximum_complexity = 0
    for table_header in table_headers:
        complexity = 1
        synset_packs = get_header_synsets(table_header)
        for (_, synsets) in synset_packs:
            complexity = complexity * len(synsets)

        if maximum_complexity < complexity:
            maximum_complexity = complexity

    return maximum_complexity


def get_max_complexity_combinations():
    """
    Calculate amount of combinations for the header permutations.

    i.e. if header is ["country", "city", "population"] and the synsets
    got [5, 6, 10] elements, then the complexity will be
    5*6 + 5*10 + 6*10
    Max complexity is: 8056
    """
    table_headers = load_test_data()
    maximum_complexity = 0
    for table_header in table_headers:
        complexity = 0
        synset_packs = get_header_synsets(table_header)
        for outer_index in range(0, len(synset_packs)):
            outer_synset_pack_len = len(synset_packs[outer_index][1])
            for inner_index in range(outer_index, len(synset_packs)):
                inner_synset_pack_len = len(synset_packs[inner_index][1])
                complexity += outer_synset_pack_len * inner_synset_pack_len

        if maximum_complexity < complexity:
            maximum_complexity = complexity

    return maximum_complexity
