"""RDFQuery queries the SPARQL endpoint."""

import os
import pickle
import uuid

from lovlabelfetcherpy.lovlabelfetcher import LOVLabelFetcher

from .config import CACHE_FOLDER_LABELS
from .QueryExecutor import execute_query

# TODO: get label for yago categories,
# i.e. http://dbpedia.org/class/yago/Abstraction100002137
# Need to look into http://www.w3.org/2002/07/owl#equivalentClass
# and then lookup
# http://yago-knowledge.org/resource/wordnet_abstraction_100002137
# make an index for this (yagolabelfetcherpy)


def get_label_endpoint(subject_string):
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


def get_label_lov(subject_string):
    """
    Retrieve URI label from LOV.

    Use lovlabelfetcher library.
    """
    lov_label_fetcher = LOVLabelFetcher()
    return lov_label_fetcher.get_label(subject_string)


def get_label(subject_string):
    """
    Retrieve rdfs:label for a URI.

    Default interface for getting URI rdfs:label.
    """
    # TODO: test
    # get the label from LOV by default
    label = get_label_lov(subject_string)
    if label is None:
        # fall back to dbpedia SPARQL endpoint if does not exist
        return get_label_endpoint(subject_string)
    else:
        return label


def generate_label_for_uri(uri):
    """Generate label for uri."""
    label = uri.split("/")[-1]
    if "#" in label:
        return label.split("#")[-1]
    return label
