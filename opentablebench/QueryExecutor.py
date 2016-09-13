# -*- coding: utf-8 -*-
"""QueryExecutor -- firing the queries against a SPARQL endpoint."""

from SPARQLWrapper import JSON, SPARQLWrapper

from .config import DBPEDIA_DEFAULT_GRAPH, DBPEDIA_SPARQL_ENDPOINT


class QueryExecutor(object):
    """QueryExecutor -- firing the queries against a SPARQL endpoint."""

    @staticmethod
    def execute_query(query):
        """Execute a query against endpoint configured in config.py."""
        dbpedia_endpoint = SPARQLWrapper(DBPEDIA_SPARQL_ENDPOINT)
        dbpedia_endpoint.setReturnFormat(JSON)
        dbpedia_endpoint.addDefaultGraph(DBPEDIA_DEFAULT_GRAPH)
        dbpedia_endpoint.setQuery(query)
        results = dbpedia_endpoint.query().convert()
        return results
