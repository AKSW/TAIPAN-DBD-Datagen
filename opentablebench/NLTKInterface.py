"""NLTKInterface for NLP related tasks."""

from nltk.corpus import wordnet as wn  # pylint: disable=import-error
from nltk.corpus import wordnet_ic
import operator
import re

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
        #if item is several words -- get synsets for all of those
        synsets = []
        for subitem in _split_header_item(item):
            synsets.extend(wn.synsets(subitem))
        synsets_header_pack.append((item, synsets))
    return synsets_header_pack

def _split_header_item(string):
    """Clean and split header into an array of strings."""
    split_by_space = re.compile('[\s]+')
    header_items = split_by_space.split(string)
    return map(
        _filter_non_printable_characters,
        header_items
    )

def _filter_non_printable_characters(string):
    pattern = re.compile('[\W_]+')
    return pattern.sub('', string)

def cluster_header(synsets_header_pack):
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

def cluster_header_naive(header):
    """
    Cluster synsets by maximum similarity.

    The problem is that it might get stuck in a local maximum.
    To overcome the problem it is necessary to employ more sophisticated
    clustering methods.
    """
    synsets_pack = get_header_synsets(header)
    # Pick the column with minimum synsets
    minimal_column = 0
    minimum_synsets = 1000
    for index, synset_pack in enumerate(synsets_pack):
        (item, synsets) = synset_pack
        if len(synsets) > 0\
            and len(synsets) < minimum_synsets:
            minimum_synsets = len(synsets)
            minimal_column = index

    #Fix the minimum column
    verbalized_headers = []
    for minimal_column_item in range(0, minimum_synsets):
        (_item, _synsets) = synsets_pack[minimal_column]
        _synset = _synsets[minimal_column_item]

        #Find the shortest path to each column
        shortest_path = []
        shortest_path.append(
            (_convert_synset_to_header_item(_synset), minimal_column)
        )
        evaluated_columns = []
        evaluated_columns.append(minimal_column)
        next_synset = _synset
        total_similarity = 0
        while True:
            similarity_pairs = []
            for index, synset_pack in enumerate(synsets_pack):
                # skip evaluated columns
                if index in evaluated_columns:
                    continue
                (item, synsets) = synset_pack
                closest_pair = find_closest_synsets(
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
                    if not index in evaluated_columns:
                        shortest_path.append((header[index], index))
                break

            next_synset = closest_pair[1]
            shortest_path.append(
                (_convert_synset_to_header_item(next_synset), index)
            )

            evaluated_columns.append(index)
            if len(evaluated_columns) == len(synsets_pack):
                break

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


def _convert_synset_to_header_item(synset):
    return " ".join(synset.name().split(".")[0].split("_"))


def verbalize_header(header):
    """Verbalize header items."""
    verbalized_header = []

    verbalized_headers = cluster_header_naive(header)
    top_header = sorted(verbalized_headers, key=operator.itemgetter(1, 2))[0][0]

    return top_header


def find_closest_synsets(synsets_1, synsets_2, index):
    closest_pair = ()
    max_similarity = 0
    if synsets_1 == [] or synsets_2 == []:
        return (closest_pair, 0, index)
    for _synset_1 in synsets_1:
        for _synset_2 in synsets_2:
            similarity = calculate_similarity(_synset_1, _synset_2)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_pair = (_synset_1, _synset_2)
    return (closest_pair, similarity, index)


def calculate_similarity(synset_1, synset_2):
    similarity = synset_1.path_similarity(synset_2)
    if similarity is None:
        return 0
    else:
        return similarity


def load_test_data():
    table_headers_file = FileReader(TABLE_HEADERS_FILE)
    table_headers = table_headers_file.readlines()
    table_headers = map(lambda x: x.strip(), table_headers)
    table_headers = map(lambda x: eval(x), table_headers)
    return table_headers
