# -*- coding: utf-8 -*-
"""TableGenerator -- generate the tables out of RDF from a SPARQL endpoint."""

import math
import os
import random
import re
import string
import uuid

from .config import CLASSES_FOLDER, PROPERTIES_FOLDER, \
    SUBJECT_COLUMN_FOLDER, TABLE_FOLDER
from .CsvWriter import CsvWriter
from .NLTKInterface import verbalize_header_random
from .RDFFilter import get_labels_for_all_objects
from .RDFGenerator import convert_dict_to_rdf, save_rdf
from .RDFQuery import get_label


class TableGenerator(object):
    """
    TableGenerator.

    Generate the tables out of RDF from a SPARQL endpoint.
    """

    CHAR_REGEX = re.compile("[a-z]|[A-Z]")
    NUM_REGEX = re.compile("[0-9]")

    CELL_IS_TEXT = 0
    CELL_IS_NUM = 1

    def generate_tables_of_length(
            self,
            _class,
            triples_tuples,
            table_length_rows
    ):
        """Generate entities/table_length_rows number of tables for _class."""
        number_of_entities = len(triples_tuples)
        for i in range(0, number_of_entities, table_length_rows):
            # i gives a lower limit
            self.generate_table(
                _class,
                triples_tuples[i:table_length_rows + i]
            )

    def generate_table(self, _class, triples_tuples):
        """Generate a table for _class from entities."""
        table_id = self._generate_random_table_id()

        ntriples = convert_dict_to_rdf(triples_tuples)
        ntriples_filename = str(table_id) + ".nt"
        save_rdf(ntriples, ntriples_filename)

        rows = self._get_rows(triples_tuples, permutate_columns=False)
        header = self.generate_header(rows[0])
        verbalized_header = verbalize_header_random(header)
        csv_filename = str(table_id) + ".csv"
        csv_filepath = os.path.join(TABLE_FOLDER, csv_filename)

        self.generate_property_annotation(csv_filename, rows[0])
        self.generate_subj_col_annotation(csv_filename, rows[0])
        self.generate_class_annotation(csv_filename, _class)

        csv_writer = CsvWriter(csv_filepath)
        csv_writer.write_header(verbalized_header)

        for row_entity_tuple in rows:
            (_, row) = row_entity_tuple
            row = self._unpack_row(row)
            row = self.introduce_errors_row(row)
            aligned_row = self._align_row_with_header(row, header)
            csv_writer.write_row(aligned_row)

        csv_writer.close()


    def introduce_errors_row(self, row):
        """Introduce errors to a row with 10% probability."""
        #if random.randint(0,100) > 10:
        #    return row

        for header_label in row:
            cell = row[header_label]
            if len(cell) <= 0:
                continue
            cell_type = self.classify_cell(cell)
            if cell_type is self.CELL_IS_TEXT:
                row[header_label] = self.introduce_errors_text(cell)
            elif cell_type is self.CELL_IS_NUM:
                row[header_label] = self.introduce_errors_num(cell)

        return row


    def classify_cell(self, cell):
        """Classify cell as a text or number."""
        char_count = len(re.findall(self.CHAR_REGEX, cell))
        char_percentage = char_count / len(cell)
        if char_percentage > 0.75:
            return self.CELL_IS_TEXT

        num_count = len(re.findall(self.NUM_REGEX, cell))
        num_percentage = num_count / len(cell)
        if num_percentage > 0.6:
            return self.CELL_IS_NUM

        return None

    @staticmethod
    def introduce_errors_text(_string):
        """
        Add errors to the text.

        Add error every 20 characters
        """
        if len(_string) <= 2:
            # ignore short strings
            return _string
        errors_per_char = 20
        errors_count = math.ceil(len(_string) / errors_per_char)
        for _ in range(0, errors_count):
            #Remove character
            position = random.randint(1, len(_string) - 1)
            _string = _string[:position] + _string[(position+1):]
            #Insert random character
            _char = random.choice(string.ascii_letters)
            position = random.randint(1, len(_string) - 1)
            _string = _string[:position] + _char + _string[position:]
        return _string


    @staticmethod
    def introduce_errors_num(_string):
        if len(_string) <= 1:
            # ignore one digit numbers
            return _string
        #Insert random character
        _char = random.choice(string.digits)
        position = random.randint(1, len(_string) - 1)
        _string = _string[:position] + _char + _string[(position - 1):]
        return _string


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

    @staticmethod
    def generate_class_annotation(csv_filename, _class):
        """
        Generate class annotation in csv format.

        Header is:
        id_of_table_csv_file.csv, dbpediaClassLabel,
        dbpediaClassUri, headerRowIndex (always 1)
        """
        class_annotation_filepath = os.path.join(CLASSES_FOLDER, csv_filename)
        csv_writer = CsvWriter(class_annotation_filepath)
        row = [csv_filename, get_label(_class), _class, 1]
        csv_writer.write_row(row)
        csv_writer.close()

    def _get_rows(self, triples_tuples, permutate_columns=True):
        labeled_tuples = get_labels_for_all_objects(triples_tuples)

        rows = []
        for num, triples_tuple in enumerate(labeled_tuples):
            (entity, triples) = triples_tuple
            row_entity_tuple = self._get_row(entity, triples)
            # permutate first row to have a random header sequence
            if num == 0 and permutate_columns:
                (entity, row) = row_entity_tuple
                permutated_row = self._permutate_row(row)
                row_entity_tuple = (entity, permutated_row)
            rows.append(row_entity_tuple)
        return rows

    @staticmethod
    def _get_row(entity, triples):
        row = []
        # append entity label as the first item
        row.append({
            "property": "http://www.w3.org/2000/01/rdf-schema#label",
            "label": "label",
            "value": get_label(entity)
        })

        properties = []
        for _triple in triples:
            _property = _triple
            _object = triples[_triple]
            _property_label = get_label(_property)
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
