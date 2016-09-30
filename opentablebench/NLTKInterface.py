"""NLTKInterface for NLP related tasks."""

from nltk.corpus import wordnet as wn  # pylint: disable=import-error

from .Logger import get_logger

LOGGER = get_logger(__name__)


def verbalize_header(header):
    """Verbalize header items."""
    wn.synsets("dog")
    LOGGER.debug(header)
    return header
