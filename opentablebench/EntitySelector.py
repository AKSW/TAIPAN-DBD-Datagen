# -*- coding: utf-8 -*-
"""EntitySelector -- getting entities from a SPARQL endpoint."""

from .QueryExecutor import QueryExecutor


class EntitySelector(object):
    """EntitySelector -- getting entities from a SPARQL endpoint."""

    def __init__(self):
        """Initialize EntitySelector with QueryExecutor."""
        self.query_executor = QueryExecutor()

    def get_entities(self, _class):
        """Request 100 entities for a given _class."""
        print("Getting entities for %s" % (_class,))
        results = self.query_executor.execute_query(u"""
            SELECT DISTINCT ?entity
            WHERE {
                ?entity rdf:type <%s>
            } LIMIT 100
        """ % (_class, ))
        results = results["results"]["bindings"]
        entities = []
        for _result in results:
            entity = _result["entity"]["value"]
            entities.append(entity)
        return entities

    def count_entities(self, _class):
        """Request number of entities for a given _class."""
        results = self.query_executor.execute_query(u"""
            SELECT DISTINCT COUNT(?entity)
            WHERE {
                ?entity rdf:type <%s>
            }
        """ % (_class, ))
        return int(results['results']['bindings'][0]['callret-0']['value'])
