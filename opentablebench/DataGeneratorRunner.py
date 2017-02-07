# -*- coding: utf-8 -*-
"""DataGeneratorRunner.py -- entrypoint for the benchmark data generator."""

import os

from .ClassSelector import ClassSelector
from .config import TABLE_FOLDER, GENERATED_CLASS_FILE
from .EntitySelector import EntitySelector
from .FileReader import FileReader
from .FileWriter import FileWriter
from .Logger import get_logger
from .RDFFilter import get_distinct_properties_triples
from .RDFGenerator import fetch_triples_for_entities
from .TableGenerator import TableGenerator

LOGGER = get_logger(__name__)


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


    def get_classes_to_skip(self, tables_per_class):
        """Get amount of classes to skip."""
        _classes = self.get_generated_class_list()
        classes_to_skip = len(_classes)
        return classes_to_skip

    @staticmethod
    def get_number_of_tables():
        """Get number of tables from TABLE_FOLDER."""
        _, _, files = next(os.walk(TABLE_FOLDER))
        return len(files)

    @staticmethod
    def get_generated_class_list():
        """Get the list of generated classes."""
        try:
            file_reader = FileReader(GENERATED_CLASS_FILE)
            _classes = file_reader.readlines()
        except:
            _classes = []
        return _classes

    @staticmethod
    def add_class_to_the_list(class_name):
        """Add generated class to the list."""
        file_writer = FileWriter(GENERATED_CLASS_FILE, append=True)
        line = "%s\n" %(class_name,)
        file_writer.write(line)
        file_writer.close()

    def run(self):
        """Run the data generator."""
        number_of_entities = 100
        tables_per_class = 20
        rows_per_table = int(number_of_entities / tables_per_class)

        classes = self.class_selector.get_classes_with_entities(
            number_of_entities=number_of_entities
        )
        classes_to_skip = self.get_classes_to_skip(tables_per_class)
        LOGGER.info("Skipping first %s classes", classes_to_skip)

        for num, _class in enumerate(classes):
            if num < classes_to_skip:
                continue
            LOGGER.info(
                "Processing (%s out of %s): %s",
                num,
                len(classes),
                _class,
            )
            entities = self.entity_selector.get_entities(
                _class,
                number_of_entities
            )
            triples_tuples_json = fetch_triples_for_entities(entities)
            triples_tuples_filtered = get_distinct_properties_triples(
                triples_tuples_json
            )

            # 20 entities per table --> 20 rows
            self.table_generator.generate_tables_of_length(
                _class,
                triples_tuples_filtered,
                rows_per_table
            )
            LOGGER.info(
                "Generated table count: %s",
                DataGeneratorRunner.get_number_of_tables()
            )
            self.add_class_to_the_list(_class)
