# -*- coding: utf-8 -*-
"""QueryExecutor -- firing the queries against a SPARQL endpoint."""

import requests

from SPARQLWrapper import JSON, SPARQLWrapper

from .config import DBPEDIA_DEFAULT_GRAPH, DBPEDIA_SPARQL_ENDPOINT


def execute_query(query):
    """
    Execute a query against endpoint configured in config.py.

    Returns JSON.
    """
    return _execute_query(
        DBPEDIA_SPARQL_ENDPOINT,
        JSON,
        DBPEDIA_DEFAULT_GRAPH,
        query
    ).convert()


def _execute_query(endpoint, return_format, default_graph, query):
    dbpedia_endpoint = SPARQLWrapper(endpoint)
    dbpedia_endpoint.setReturnFormat(return_format)
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
