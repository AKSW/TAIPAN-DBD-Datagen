"""RDFFilter filters RDF."""

import random

from .RDFQuery import get_label


def get_distinct_properties_triples(triple_tuples_json):
    """
    Get distinct ?s ?p ?o.

    Sorted by number of predicates (the largest first).
    """
    grouped_by_predicate = []
    for triple_tuple in triple_tuples_json:
        _subject = triple_tuple[0]
        predicates = {}
        for _triple in triple_tuple[1]:
            _predicate = _triple["p"]["value"]
            _object = _triple["o"]["value"]
            if predicates.get(_predicate, None) is None:
                predicates[_predicate] = []
            predicates[_predicate].append(_object)
        for _predicate in predicates:
            predicates[_predicate] = random.choice(predicates[_predicate])
        grouped_by_predicate.append((_subject, predicates))
    return sorted(
        grouped_by_predicate,
        key=lambda tuple: len(tuple[1]),
        reverse=True
    )


def get_labels_for_all_objects(triple_tuples):
    """Get labels for all ?o."""
    labeled_objects = []
    for triple_tuple in triple_tuples:
        _subject = triple_tuple[0]
        predicates = triple_tuple[1]
        for _predicate in predicates:
            _object = triple_tuple[1][_predicate]
            predicates[_predicate] = get_label(_object)
        labeled_objects.append((_subject, predicates))
    return labeled_objects
