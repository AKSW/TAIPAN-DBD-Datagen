"""NLTKInterface for NLP related tasks."""

from nltk.corpus import wordnet as wn  # pylint: disable=import-error

from .config import TABLE_HEADERS_FILE
from .FileReader import FileReader
from .Logger import get_logger

LOGGER = get_logger(__name__)


def verbalize_header(header):
    """Verbalize header items."""
    wn.synsets("dog")
    return header


def load_test_data():
    table_headers_file = FileReader(TABLE_HEADERS_FILE)
    table_headers = table_headers_file.readlines()
    table_headers = map(lambda x: x.strip(), table_headers)
    table_headers = map(lambda x: eval(x), table_headers)
    return table_headers
