"""RDFGenerator fetches and permutate RDF."""

import pickle
import os
import uuid

from .config import CACHE_FOLDER_TRIPLES, CACHE_FOLDER_TRIPLES_RDF, RDF_FOLDER
from .FileWriter import FileWriter
from .QueryExecutor import execute_query, execute_query_rdf
from .RDFQuery import get_label

NUMBER_OF_TRIPLES_FOR_ENTITY = 15


def fetch_triples_for_entity(entity):
    """
    Retrieve ?p ?o for entity ?s.

    Returns JSON.
    """
    _entity_hash = uuid.uuid5(
        uuid.NAMESPACE_URL,
        entity
    )
    cached_triples_file = os.path.join(
        CACHE_FOLDER_TRIPLES,
        str(_entity_hash)
    )
    if os.path.exists(cached_triples_file):
        return pickle.load(open(cached_triples_file, "rb"))
    else:
        query = _gen_query_for_entity(
            entity,
            NUMBER_OF_TRIPLES_FOR_ENTITY
        )
        results = execute_query(query)
        results = results["results"]["bindings"]
        pickle.dump(
            results,
            open(cached_triples_file, "wb")
        )
        return results


def fetch_triples_for_entity_rdf(entity):
    """
    Retrieve ?p ?o for entity ?s.

    Returns Ntriples.
    """
    _entity_hash = uuid.uuid5(
        uuid.NAMESPACE_URL,
        entity
    )
    cached_triples_rdf_file = os.path.join(
        CACHE_FOLDER_TRIPLES_RDF,
        str(_entity_hash)
    )
    if os.path.exists(cached_triples_rdf_file):
        return pickle.load(open(cached_triples_rdf_file, "rb"))
    else:
        query = _gen_query_for_entity_rdf(
            entity,
            NUMBER_OF_TRIPLES_FOR_ENTITY
        )
        results = execute_query_rdf(query)
        pickle.dump(
            results,
            open(cached_triples_rdf_file, "wb")
        )
        return results


def _gen_query_for_entity(entity, number_of_triples):
    """
    Generate query to fetch triples for an entity.

    Return format which can be parsed to JSON.
    """
    query = u"""
        SELECT DISTINCT ?p ?o
        WHERE {<%s> ?p ?o}
        LIMIT %s
    """ % (entity, number_of_triples,)
    return query


def _gen_query_for_entity_rdf(entity, number_of_triples):
    """
    Generate query to fetch triples for an entity.

    Return RDF triples.
    """
    query = u"""
        CONSTRUCT {<%s> ?p ?o}
        WHERE {<%s> ?p ?o}
        LIMIT %s
    """ % (entity, entity, number_of_triples,)
    return query


def fetch_triples_for_entities(entities):
    """
    Retrieve RDF for all entities.

    Returns JSON.
    """
    triple_tuples = []
    for entity in entities:
        triples = fetch_triples_for_entity(entity)
        triple_tuples.append(
            (entity, triples)
        )
    return triple_tuples


def fetch_triples_for_entities_rdf(entities):
    """
    Retrieve RDF for all entities.

    Returns Ntriples
    """
    triple_tuples = []
    for entity in entities:
        triples = fetch_triples_for_entity_rdf(entity)
        triple_tuples.append(
            (entity, triples)
        )
    return triple_tuples


def convert_json_to_rdf(triple_tuples_json):
    """Convert triples in JSON to Ntriples."""
    triples = []
    for triple_tuple in triple_tuples_json:
        _subject = triple_tuple[0]
        for _triple in triple_tuple[1]:
            # property is always uri, no need to check
            _property = "<%s>" % (_triple["p"]["value"],)

            _object = _triple["o"]["value"]
            _object_type = _triple["o"]["type"]
            if _object_type == "uri":
                _object = "<%s>" % (_object,)
            elif _object_type == "literal":
                _object = '"%s"' % (_object,)
            elif _object_type == "typed-literal":
                _object_datatype = _triple["o"]["datatype"]
                _object = '"%s"^^<%s>' % (_object, _object_datatype,)

            triples.append(
                "%s %s %s ." % (_subject, _property, _object)
            )
    return "\n".join(triples)


def convert_dict_to_rdf(triple_tuples):
    """Convert triples in JSON to Ntriples."""
    triples = []
    for triple_tuple in triple_tuples:
        _subject = "<%s>" % (triple_tuple[0],)
        for _triple in triple_tuple[1]:
            # property is always uri, no need to check
            _property = "<%s>" % (_triple,)

            _object = triple_tuple[1][_triple]
            if _object.startswith("http"):
                _object = "<%s>" % (_object,)
            else:
                _object = '"%s"' % (_object,)

            triples.append(
                "%s %s %s ." % (_subject, _property, _object)
            )
        label_triple = '%s <http://www.w3.org/2000/01/rdf-schema#label>\
"%s" .' % (_subject, get_label(triple_tuple[0]),)
        triples.append(label_triple)
    return "\n".join(triples)


def save_rdf(ntriples_string, filename):
    """Write triples to the generated/rdf/ folder."""
    rdf_filepath = os.path.join(RDF_FOLDER, filename)
    file_writer = FileWriter(rdf_filepath)
    file_writer.write(ntriples_string)
    file_writer.close()
