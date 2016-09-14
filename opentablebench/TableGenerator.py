# -*- coding: utf-8 -*-
"""TableGenerator -- generate the tables out of RDF from a SPARQL endpoint."""

import os
import random
import uuid

from .config import CLASSES_FOLDER, PROPERTIES_FOLDER, \
    SUBJECT_COLUMN_FOLDER, TABLE_FOLDER
from .CsvWriter import CsvWriter
from .QueryExecutor import execute_query
from .RDFGenerator import fetch_triples_for_entity


class TableGenerator(object):
    """
    TableGenerator.

    Generate the tables out of RDF from a SPARQL endpoint.
    """

    def generate_table_of_length(self, _class, entities, table_length_rows):
        """Generate entities/table_length_rows number of tables for _class."""
        number_of_entities = len(entities)
        for i in range(0, number_of_entities, table_length_rows):
            # i gives a lower limit
            self.generate_table(_class, entities[i:table_length_rows + i])

    def generate_table(self, _class, entities):
        """Generate a table for _class from entities."""
        print("Getting rows for %s" % (_class,))
        rows = self._get_rows(entities)
        print("Getting header for %s" % (_class,))
        header = self.generate_header(rows[0])
        table_id = self._generate_random_table_id()
        csv_filename = str(table_id) + ".csv"
        csv_filepath = os.path.join(TABLE_FOLDER, csv_filename)

        print("Generating property annotation for %s" % (_class,))
        self.generate_property_annotation(csv_filename, rows[0])
        print("Generating subject column annotation for %s" % (_class,))
        self.generate_subj_col_annotation(csv_filename, rows[0])
        print("Generating class annotation for %s" % (_class,))
        self.generate_class_annotation(csv_filename, _class)

        csv_writer = CsvWriter(csv_filepath)
        csv_writer.write_header(header)

        for row_entity_tuple in rows:
            (_, row) = row_entity_tuple
            row = self._unpack_row(row)
            aligned_row = self._align_row_with_header(row, header)
            csv_writer.write_row(aligned_row)

        csv_writer.close()

    @staticmethod
    def _unpack_row(row):
        unpacked_row = {}
        for cell in row:
            unpacked_row[cell['label']] = cell['value']

        return unpacked_row

    @staticmethod
    def _align_row_with_header(unpacked_row, header):
        aligned_row = []
        for item in header:
            aligned_row.append(unpacked_row.get(item, ""))
        return aligned_row

    @staticmethod
    def generate_table_id(_class):
        """Create a unique deterministic ID from a class URI."""
        return uuid.uuid5(uuid.NAMESPACE_URL, _class)

    @staticmethod
    def _generate_random_table_id():
        return uuid.uuid4()

    @staticmethod
    def generate_header(row_entity_tuple):
        """Generate CSV header."""
        (_, cells) = row_entity_tuple
        header = []
        for cell in cells:
            header.append(cell['label'])
        return header

    @staticmethod
    def generate_property_annotation(csv_filename, row_entity_tuple):
        """
        Generate the property annotation as csv file.

        Example:
        "http://dbpedia.org/ontology/genre","","False","1"
        "http://dbpedia.org/ontology/computingPlatform","","False","2"
        "http://www.w3.org/2000/01/rdf-schema#label","","True","3"
        """
        (_, cells) = row_entity_tuple
        properties = []
        for cell in cells:
            properties.append(cell['property'])

        property_annotation_filepath = os.path.join(
            PROPERTIES_FOLDER,
            csv_filename
        )
        csv_writer = CsvWriter(property_annotation_filepath)
        for num, _property in enumerate(properties):
            if _property == u"http://www.w3.org/2000/01/rdf-schema#label":
                row = [_property, "", "True", str(num + 1)]
            else:
                row = [_property, "", "False", str(num + 1)]
            csv_writer.write_row(row)

        csv_writer.close()

    @staticmethod
    def generate_subj_col_annotation(csv_filename, row_entity_tuple):
        """
        Generate the subject column annotation as csv file.

        Example:
        id_of_table_csv_file.csv, 5
        id_of_table_csv_file2.csv, 0

            in our case subject column is always 0
            for proper testing, column shuffling is necessary
        """
        (_, cells) = row_entity_tuple
        subject_column_index = 0

        properties = []
        for cell in cells:
            properties.append(cell['property'])

        subject_column_index = properties.index(
            "http://www.w3.org/2000/01/rdf-schema#label"
        )

        subj_col_annotation_filepath = os.path.join(
            SUBJECT_COLUMN_FOLDER,
            csv_filename
        )
        csv_writer = CsvWriter(subj_col_annotation_filepath)
        row = [csv_filename, str(subject_column_index + 1)]
        csv_writer.write_row(row)
        csv_writer.close()

    def generate_class_annotation(self, csv_filename, _class):
        """
        Generate class annotation in csv format.

        Header is:
        id_of_table_csv_file.csv, dbpediaClassLabel,
        dbpediaClassUri, headerRowIndex (always 1)
        """
        class_annotation_filepath = os.path.join(CLASSES_FOLDER, csv_filename)
        csv_writer = CsvWriter(class_annotation_filepath)
        row = [csv_filename, self._get_label(_class), _class, 1]
        csv_writer.write_row(row)
        csv_writer.close()

    def _get_rows(self, entities):
        rows = []
        for num, entity in enumerate(entities):
            print("Getting row %s out of %s" % (num, len(entities),))
            row_entity_tuple = self._get_row(entity)
            # permutate first row to have a random header sequence
            if num == 0:
                (entity, row) = row_entity_tuple
                permutated_row = self._permutate_row(row)
                row_entity_tuple = (entity, permutated_row)
            rows.append(row_entity_tuple)
        return rows

    def _get_row(self, entity):
        triples = fetch_triples_for_entity(entity)

        row = []
        # append entity label as the first item
        row.append({
            "property": "http://www.w3.org/2000/01/rdf-schema#label",
            "label": "label",
            "value": self._get_label(entity)
        })

        properties = []
        for _triple in triples:
            _property = _triple["p"]["value"]
            _object = _triple["o"]["value"]
            _property_label = self._get_label(_property)
            if _property_label != "" and (_property not in properties):
                row.append({
                    "property": _property,
                    "label": _property_label,
                    "value": _object
                })
                properties.append(_property)

        return (entity, row)

    @staticmethod
    def _permutate_row(row):
        number_of_cols = len(row)
        if number_of_cols == 1:
            return row

        for _ in range(0, 1000):
            col_a = random.randint(0, number_of_cols - 1)
            col_b = col_a
            while col_b == col_a:
                col_b = random.randint(0, number_of_cols - 1)
            temp = row[col_a]
            row[col_a] = row[col_b]
            row[col_b] = temp
        return row

    @staticmethod
    def _get_label(subject_string):
        results = execute_query(u"""
            SELECT DISTINCT ?label
            WHERE {<%s> rdfs:label ?label}
            LIMIT 1
        """ % (subject_string,))
        results = results["results"]["bindings"]
        if len(results) == 0:
            return ""
        else:
            return results[0]["label"]["value"]
