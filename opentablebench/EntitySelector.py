# -*- coding: utf-8 -*-
"""EntitySelector -- getting entities from a SPARQL endpoint."""

from .QueryExecutor import execute_query


class EntitySelector(object):
    """EntitySelector -- getting entities from a SPARQL endpoint."""

    @staticmethod
    def get_entities(_class, number_of_entities):
        """Request number_of_entities entities for a given _class."""
        print("Getting entities for %s" % (_class,))
        results = execute_query(u"""
            SELECT DISTINCT ?entity
            WHERE {
                ?entity rdf:type <%s>
            } LIMIT %s
        """ % (_class, number_of_entities,))
        results = results["results"]["bindings"]
        entities = []
        for _result in results:
            entity = _result["entity"]["value"]
            entities.append(entity)
        return entities

    @staticmethod
    def count_entities(_class):
        """Request number of entities for a given _class."""
        results = execute_query(u"""
            SELECT DISTINCT COUNT(?entity)
            WHERE {
                ?entity rdf:type <%s>
            }
        """ % (_class, ))
        return int(results['results']['bindings'][0]['callret-0']['value'])
