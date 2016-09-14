"""RDFGenerator fetches and permutate RDF."""

from .QueryExecutor import execute_query, execute_query_rdf

NUMBER_OF_TRIPLES_FOR_ENTITY = 15


def fetch_triples_for_entity(entity):
    """
    Retrieve ?p ?o for entity ?s.

    Returns JSON.
    """
    query = _gen_query_for_entity(
        entity,
        NUMBER_OF_TRIPLES_FOR_ENTITY
    )
    results = execute_query(query)
    results = results["results"]["bindings"]
    return results


def fetch_triples_for_entity_rdf(entity):
    """
    Retrieve ?p ?o for entity ?s.

    Returns Ntriples.
    """
    query = _gen_query_for_entity_rdf(
        entity,
        NUMBER_OF_TRIPLES_FOR_ENTITY
    )
    results = execute_query_rdf(query)
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
