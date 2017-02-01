"""RDFQuery queries the SPARQL endpoint."""

import os
import pickle
import uuid

from lovlabelfetcherpy.lovlabelfetcher import LOVLabelFetcher
from yagolabelfetcherpy.yagolabelfetcher import YAGOLabelFetcher

from .config import CACHE_FOLDER_LABELS, CACHE_FOLDER_LABELS_WIKIDATA
from .QueryExecutor import execute_query, execute_query_wikidata


def get_label_endpoint(subject_string):
    """Get label for subject_string from endpoint."""
    if not subject_string.startswith("http"):
        return subject_string
    subject_string_hash = uuid.uuid5(
        uuid.NAMESPACE_URL,
        subject_string
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
            label_uri = None
        else:
            label_uri = results[0]["label"]["value"]
        pickle.dump(
            label_uri,
            open(cached_label_file, "wb")
        )
        return label_uri


def get_label_wikidata(subject_string):
    """
    Retrieve URI label from wikidata.

    Use wikidata endpoint
    """
    if not subject_string.startswith("http"):
        return subject_string
    subject_string_hash = uuid.uuid5(
        uuid.NAMESPACE_URL,
        subject_string
    )
    cached_label_file = os.path.join(
        CACHE_FOLDER_LABELS_WIKIDATA,
        str(subject_string_hash)
    )
    if os.path.exists(cached_label_file):
        return pickle.load(open(cached_label_file, "rb"))
    else:
        results = execute_query_wikidata(u"""
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
            label_uri = None
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
    label = lov_label_fetcher.get_label(subject_string)
    return label


def get_label_yago(subject_string):
    """
    Retrieve URI label from YAGO.

    Use yagolabelfetcher library.
    """
    yago_label_fetcher = YAGOLabelFetcher()
    label = yago_label_fetcher.get_label(subject_string)
    return label


def get_label(subject_string):
    """
    Retrieve rdfs:label for a URI.

    Default interface for getting URI rdfs:label.
    """
    # get the label from LOV by default
    label = get_label_lov(subject_string)

    if label is None:
        # get the label from YAGO
        label = get_label_yago(subject_string)

    if label is None:
        # dbpedia SPARQL endpoint
        label = get_label_endpoint(subject_string)

    if label is None:
        # wikidata SPARQL endpoint
        label = get_label_wikidata(subject_string)

    if label is None:
        # empty value for everything what is left
        label = ""
        # raise Exception

    return label


def generate_label_for_uri(uri):
    """Generate label for uri."""
    label = uri.split("/")[-1]
    if "#" in label:
        return label.split("#")[-1]
    return label
