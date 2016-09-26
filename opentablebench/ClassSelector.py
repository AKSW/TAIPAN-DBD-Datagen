# -*- coding: utf-8 -*-
"""ClassSelector -- selecting classes out of SPARQL endpoint."""
import os
import random

from .config import CLASSES_ENTITIES_FILE, RANDOM_CLASS_SELECTION
from .FileWriter import FileWriter
from .QueryExecutor import execute_query


class ClassSelector(object):
    """ClassSelector selects owl:Class from SPARQL endpoint."""

    @staticmethod
    def get_classes():
        """Get all classes from SPARQL endpoint."""
        results = execute_query(u"""
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

    @staticmethod
    def get_class_count():
        """Get number of classes in a SPARQL endpoint."""
        results = execute_query(u"""
            SELECT DISTINCT COUNT(?class)
            WHERE {?class rdf:type owl:Class}
        """)
        import ipdb; ipdb.set_trace()
        return int(results["results"]["bindings"][0]["callret-0"]["value"])

    @staticmethod
    def get_empty_classes():
        """
        Get classes with 0 entities from a SPARQL endpoint.

        Fetches the data from ClassesEntitiesCount.csv file.
        """
        empty_classes = []
        _file = open(CLASSES_ENTITIES_FILE)
        for line in _file.readlines():
            (_class, count) = line.split(",")
            if int(count) == 0:
                empty_classes.append(_class)
        return empty_classes

    @staticmethod
    def get_classes_with_entities(number_of_entities=100):
        """
        Get classes with >20 entities from a SPARQL endpoint.

        Fetches the data from ClassesEntitiesCount.csv file.
        """
        if not os.path.exists(CLASSES_ENTITIES_FILE):
            ClassSelector.fetch_classes_entities()

        classes = []
        _file = open(CLASSES_ENTITIES_FILE)
        for line in _file.readlines():
            (_class, count) = line.split(",")
            if int(count) > number_of_entities:
                classes.append(_class)
        return classes

    @staticmethod
    def fetch_classes_entities():
        """Update ClassesEntitiesCount.csv file."""
        if os.path.exists(CLASSES_ENTITIES_FILE):
            return

        _file = FileWriter(CLASSES_ENTITIES_FILE)
        classes = ClassSelector.get_classes()
        for _class in classes:
            if not _class.startswith("http"):
                continue
            results = execute_query(u"""
                SELECT DISTINCT COUNT(?s)
                WHERE {
                    ?s ?p ?o .
                    ?s ?p <%s> .
                }
            """ % (_class))
            count = results["results"]["bindings"][0]["callret-0"]["value"]
            csv_string = "%s, %s\n" % (_class, count)
            _file.write(csv_string)
        _file.close()
