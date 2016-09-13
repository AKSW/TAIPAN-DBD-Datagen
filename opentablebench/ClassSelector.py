# -*- coding: utf-8 -*-
"""ClassSelector -- selecting classes out of SPARQL endpoint."""
import os
import random

from .config import DATA_FOLDER, RANDOM_CLASS_SELECTION
from .QueryExecutor import QueryExecutor


class ClassSelector(object):
    """ClassSelector selects owl:Class from SPARQL endpoint."""

    def __init__(self):
        """Initialize ClassSelector with QueryExecutor."""
        self.query_executor = QueryExecutor()

    def get_classes(self):
        """Get all classes from SPARQL endpoint."""
        results = self.query_executor.execute_query(u"""
            SELECT DISTINCT ?class
            WHERE {?class rdf:type owl:Class}
        """)
        results = results["results"]["bindings"]
        classes = []
        for _result in results:
            _class = _result["class"]["value"]
            if _class.startswith("http://"):
                classes.append(_class)
        return classes

    def generate_random_selection(self, number_of_classes):
        """Generate random sequence of classes (returns indexes)."""
        classes = self.get_classes_with_entities()
        random_sample = random.sample(classes, number_of_classes)
        indexes = []
        for item in random_sample:
            indexes.append(classes.index(item))
        return indexes

    def get_random_classes(self):
        """Get random classes from config.py."""
        classes = self.get_classes_with_entities()
        random_indexes = RANDOM_CLASS_SELECTION
        random_classes = []
        for index in random_indexes:
            random_classes.append(classes[index])
        return random_classes

    def get_class_count(self):
        """Get number of classes in a SPARQL endpoint."""
        results = self.query_executor.execute_query(u"""
            SELECT DISTINCT COUNT(?class)
            WHERE {?class rdf:type owl:Class}
        """)
        return int(results["results"]["bindings"][0]["callret-0"]["value"])

    @staticmethod
    def get_empty_classes():
        """
        Get classes with 0 entities from a SPARQL endpoint.

        Fetches the data from ClassesEntitiesCount.csv file.
        """
        empty_classes = []
        _file = open(os.path.join(DATA_FOLDER, "ClassesEntitiesCount.csv"))
        for line in _file.readlines():
            (_class, count) = line.split(",")
            if int(count) == 0:
                empty_classes.append(_class)
        return empty_classes

    @staticmethod
    def get_classes_with_entities():
        """
        Get classes with >20 entities from a SPARQL endpoint.

        Fetches the data from ClassesEntitiesCount.csv file.
        """
        classes = []
        _file = open(os.path.join(DATA_FOLDER, "ClassesEntitiesCount.csv"))
        for line in _file.readlines():
            (_class, count) = line.split(",")
            if int(count) > 20:
                classes.append(_class)
        return classes
