# -*- coding: utf-8 -*-
"""QueryExecutor -- firing the queries against a SPARQL endpoint."""

from SPARQLWrapper import JSON, N3, SPARQLWrapper

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
    )


def execute_query_ntriples(query):
    """
    Execute a query against endpoint configured in config.py.

    Returns Ntriples.
    """
    return _execute_query(
        DBPEDIA_SPARQL_ENDPOINT,
        N3,
        DBPEDIA_DEFAULT_GRAPH,
        query
    )


def _execute_query(endpoint, return_format, default_graph, query):
    dbpedia_endpoint = SPARQLWrapper(endpoint)
    dbpedia_endpoint.setReturnFormat(return_format)
    dbpedia_endpoint.addDefaultGraph(default_graph)
    dbpedia_endpoint.setQuery(query)
    results = dbpedia_endpoint.query().convert()
    return results
