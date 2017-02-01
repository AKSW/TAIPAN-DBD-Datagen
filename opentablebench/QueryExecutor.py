# -*- coding: utf-8 -*-
"""QueryExecutor -- firing the queries against a SPARQL endpoint."""

import requests

from SPARQLWrapper import JSON, SPARQLWrapper

from .config import DBPEDIA_DEFAULT_GRAPH, DBPEDIA_SPARQL_ENDPOINT, \
        WIKIDATA_SPARQL_ENDPOINT


def execute_query(query):
    """
    Execute a query against endpoint configured in config.py.

    Returns JSON.
    """
    return _execute_query(
        query,
        DBPEDIA_SPARQL_ENDPOINT,
        JSON,
        DBPEDIA_DEFAULT_GRAPH
    ).convert()


def execute_query_wikidata(query):
    """
    Execute a query against wikidata endpoint.

    Returns JSON.
    """
    return _execute_query(
        query,
        WIKIDATA_SPARQL_ENDPOINT,
        JSON
    ).convert()


def _execute_query(query, endpoint, return_format=JSON, default_graph=None):
    dbpedia_endpoint = SPARQLWrapper(endpoint)
    dbpedia_endpoint.setReturnFormat(return_format)
    if default_graph is not None:
        dbpedia_endpoint.addDefaultGraph(default_graph)
    dbpedia_endpoint.setQuery(query)
    results = dbpedia_endpoint.query()
    return results


def execute_query_rdf(query):
    """
    Execute a query against endpoint configured in config.py.

    SPARQLWrapper does not work well with returning ntriples.
    Or any triples. Just throwing errors on wrong format.
    Returns Ntriples.
    """
    url = DBPEDIA_SPARQL_ENDPOINT
    data = {
        "format": "text/ntriples",
        "default-graph-uri": DBPEDIA_DEFAULT_GRAPH,
        "query": query
    }
    req = requests.post(url, data=data)
    return req.text
