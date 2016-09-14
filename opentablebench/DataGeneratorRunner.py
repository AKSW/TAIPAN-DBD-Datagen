# -*- coding: utf-8 -*-
"""DataGeneratorRunner.py -- entrypoint for the benchmark data generator."""

import os

from .ClassSelector import ClassSelector
from .config import TABLE_FOLDER
from .EntitySelector import EntitySelector
from .RDFGenerator import convert_json_to_rdf, fetch_triples_for_entities
from .TableGenerator import TableGenerator


class DataGeneratorRunner(object):
    """Executor for application."""

    def __init__(self):
        """
        Initialize DataGeneratorRunner.

        With ClassSelector, EntitySelector and TableGenerator.
        """
        self.class_selector = ClassSelector()
        self.entity_selector = EntitySelector()
        self.table_generator = TableGenerator()

    @staticmethod
    def get_classes_to_skip(tables_per_class):
        """Get amount of classes to skip."""
        _, _, files = next(os.walk(TABLE_FOLDER))
        generated_tables_count = len(files)
        classes_to_skip = int(float(generated_tables_count) / tables_per_class)
        return classes_to_skip

    def run(self):
        """Run the data generator."""
        classes = self.class_selector.get_classes()

        tables_per_class = 20
        classes_to_skip = self.get_classes_to_skip(tables_per_class)
        print("Skipping first %s classes" % (classes_to_skip,))

        for num, _class in enumerate(classes):
            print(
                "Processing (%s out of %s): %s"
                % (num, len(classes), _class,)
            )
            # We get 100 entities because of LIMIT in the SPARQL query
            number_of_entities = 5
            entities = self.entity_selector.get_entities(
                _class,
                number_of_entities
            )

            triples_tuples_json = fetch_triples_for_entities(entities)
            triples_tuples_rdf = convert_json_to_rdf(triples_tuples_json)
            print("Triple length is %s" % len(triples_tuples_rdf))

            # 20 entities per table --> 20 rows
            self.table_generator.generate_table_of_length(
                _class,
                triples_tuples_json,
                20
            )
