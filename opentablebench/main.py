# -*- coding: utf-8 -*-
"""main.py -- the entrypoint for the benchmark data generator."""

import os

from .ClassSelector import ClassSelector
from .config import TABLE_FOLDER
from .EntitySelector import EntitySelector
from .TableGenerator import TableGenerator


if __name__ == "__main__":
    class_selector = ClassSelector()
    classes = class_selector.getClasses()

    entity_selector = EntitySelector()
    table_generator = TableGenerator()

    path, dirs, files = os.walk(TABLE_FOLDER).next()
    generated_tables_count = len(files)
    # Can have more than 5 tables per class!
    classes_to_skip = int(float(generated_tables_count) / 5)

    for num, _class in enumerate(classes):
        print("Processing (%s out of %s): %s" % (num, len(classes), _class,))
        # We get 100 entities because of LIMIT in the SPARQL query
        entities = entity_selector.get_entities(_class)

        # 20 entities per table --> 20 rows
        table_generator.generate_table_of_length(_class, entities, 20)
