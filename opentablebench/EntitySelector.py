# -*- coding: utf-8 -*-
"""EntitySelector -- getting entities from a SPARQL endpoint."""

import pickle
import os
import uuid

from .config import CACHE_FOLDER_ENTITIES
from .QueryExecutor import execute_query


class EntitySelector(object):
    """EntitySelector -- getting entities from a SPARQL endpoint."""

    @staticmethod
    def get_entities(_class, number_of_entities):
        """Request number_of_entities entities for a given _class."""
        _class_hash = uuid.uuid5(
            uuid.NAMESPACE_URL,
            _class
        )
        cached_entities_file = os.path.join(
            CACHE_FOLDER_ENTITIES,
            str(_class_hash)
        )
        if os.path.exists(cached_entities_file):
            return pickle.load(open(cached_entities_file, "rb"))
        else:
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
            pickle.dump(
                entities,
                open(cached_entities_file, "wb")
            )
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
