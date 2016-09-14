"""RDFGenerator fetches and permutate RDF."""

from .QueryExecutor import execute_query, execute_query_ntriples

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


def fetch_triples_for_entity_nt(entity):
    """
    Retrieve ?p ?o for entity ?s.

    Returns Ntriples.
    """
    query = _gen_query_for_entity(
        entity,
        NUMBER_OF_TRIPLES_FOR_ENTITY
    )
    results = execute_query_ntriples(query)
    results = results["results"]["bindings"]
    return results


def _gen_query_for_entity(entity, number_of_triples):
    """Generate query to fetch triples for an entity."""
    query = u"""
        SELECT DISTINCT ?p ?o
        WHERE {<%s> ?p ?o}
        LIMIT %s
    """ % (entity, number_of_triples,)
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


def fetch_triples_for_entities_nt(entities):
    """
    Retrieve RDF for all entities.

    Returns Ntriples
    """
    triple_tuples = []
    for entity in entities:
        triples = fetch_triples_for_entity_nt(entity)
        triple_tuples.append(
            (entity, triples)
        )
    return triple_tuples
