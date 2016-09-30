"""RDFQuery queries the SPARQL endpoint."""

import cPickle as pickle  # pylint: disable=import-error
import os
import uuid

from .config import CACHE_FOLDER_LABELS
from .QueryExecutor import execute_query


def get_label(subject_string):
    """Get label for subject_string from endpoint."""
    if not subject_string.startswith("http"):
        return subject_string
    subject_string_hash = uuid.uuid5(
        uuid.NAMESPACE_URL,
        subject_string.encode("utf-8")
    )
    cached_label_file = os.path.join(
        CACHE_FOLDER_LABELS,
        str(subject_string_hash)
    )
    if os.path.exists(cached_label_file):
        return pickle.load(open(cached_label_file, "rb"))
    else:
        results = execute_query(u"""
            SELECT DISTINCT ?label
            WHERE {
                <%s> rdfs:label ?label .
                FILTER( lang(?label) = "en")
            }
            LIMIT 1
        """ % (subject_string,))
        results = results["results"]["bindings"]
        if len(results) == 0 or\
                results[0]["label"]["value"] is None:
            label_uri = generate_label_for_uri(subject_string)
        else:
            label_uri = results[0]["label"]["value"]
        pickle.dump(
            label_uri,
            open(cached_label_file, "wb")
        )
        return label_uri


def generate_label_for_uri(uri):
    """Generate label for uri."""
    label = uri.split("/")[-1]
    if "#" in label:
        return label.split("#")[-1]
    return label
