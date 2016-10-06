"""NLTKInterface for NLP related tasks."""

from nltk.corpus import wordnet as wn  # pylint: disable=import-error
from nltk.corpus import wordnet_ic

from .config import TABLE_HEADERS_FILE
from .FileReader import FileReader
from .Logger import get_logger

LOGGER = get_logger(__name__)


def verbalize_header(header):
    """Verbalize header items."""
    verbalized_header = []

    synsets_pack = []
    for item in header:
        synsets_pack.append((item, wn.synsets(item)))

    # calculate closest pair for first two columns
    (_, col_0) = synsets_pack[0]
    (_, col_1) = synsets_pack[1]
    (col_0_item, col_1_item) = find_closest_synsets(col_0, col_1)
    verbalized_header.extend([col_0_item, col_1_item])

    # calculate other columns
    # some elements might have no synsets!
    i = 2
    closest_to_previous = col_1_item
    while i < len(synsets_pack):
        (_, next_header_item) = synsets_pack[i]
        next_closest = None
        max_similarity = 0
        for synset in next_header_item:
            similarity = calculate_similarity(closest_to_previous, synset)
            if similarity > max_similarity:
                max_similarity = similarity
                next_closest = synset
        closest_to_previous = next_closest
        verbalized_header.append(closest_to_previous)
        i = i + 1

    return verbalized_header


def find_closest_synsets(synsets_1, synsets_2):
    closest_pair = ()
    max_similarity = 0
    for _synset_1 in synsets_1:
        for _synset_2 in synsets_2:
            similarity = calculate_similarity(_synset_1, _synset_2)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_pair = (_synset_1, _synset_2)
    return closest_pair


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
