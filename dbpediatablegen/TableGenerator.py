import csv
import uuid
import os
import random

from .QueryExecutor import QueryExecutor
from .CsvWriter import CsvWriter
from .config import TABLE_FOLDER, PROPERTIES_FOLDER, SUBJECT_COLUMN_FOLDER

class TableGenerator(object):
    def __init__(self):
        self.queryExecutor = QueryExecutor()

    def generateTableOfLengthN(self, _class, entities, n):
        numberOfEntities = len(entities)
        for i in range(0, numberOfEntities, n):
            #i gives a lower limit
            self.generateTable(_class, entities[i:n+i])

    def generateTable(self, _class, entities):
        rows = self.getRows(entities)
        header = self.generateHeader(rows[0])
        tableId = self.generateRandomTableId()
        csvFilename = str(tableId) + ".csv"
        csvFilepath = os.path.join(TABLE_FOLDER, csvFilename)

        self.generatePropertyAnnotation(csvFilename, rows[0])
        self.generateSubjectColumnAnnotation(csvFilename, rows[0])

        csvWriter = CsvWriter(csvFilepath)
        csvWriter.writeheader(header)

        for rowEntityTuple in rows:
            (entity, row) = rowEntityTuple
            row = self.unpackRow(row)
            row = self.alignRowWithHeader(row, header)
            csvWriter.writerow(row)

        csvWriter.close()

    def unpackRow(self, row):
        unpackedRow = {}
        for cell in row:
            unpackedRow[cell['label']] = cell['value']

        return unpackedRow

    def alignRowWithHeader(self, unpackedRow, header):
        alignedRow = []
        for item in header:
            alignedRow.append(unpackedRow.get(item, ""))
        return alignedRow

    def generateTableId(self, _class):
        """
            Create a unique deterministic ID from a class URI
        """
        return uuid.uuid5(uuid.NAMESPACE_URL, _class)

    def generateRandomTableId(self):
        return uuid.uuid4()

    def generateHeader(self, rowEntityTuple):
        """
            Generate CSV header
        """
        (entity, cells) = rowEntityTuple
        header = []
        for cell in cells:
            header.append(cell['label'])
        return header

    def generatePropertyAnnotation(self, csvFilename, entityRowTuple):
        """
            "http://dbpedia.org/ontology/genre","","False","1"
            "http://dbpedia.org/ontology/computingPlatform","","False","2"
            "http://www.w3.org/2000/01/rdf-schema#label","","True","3"
        """
        (entity, cells) = entityRowTuple
        properties = []
        for cell in cells:
            properties.append(cell['property'])

        propertyAnnotationFilepath = os.path.join(PROPERTIES_FOLDER, csvFilename)
        csvWriter = CsvWriter(propertyAnnotationFilepath)
        for num, _property in enumerate(properties):
            if _property == u"http://www.w3.org/2000/01/rdf-schema#label":
                row = [_property, "", "True", str(num+1)]
            else:
                row = [_property, "", "False", str(num+1)]
            csvWriter.writerow(row)

    def generateSubjectColumnAnnotation(self, csvFilename, entityRowTuple):
        """
            id_of_table_csv_file.csv, 5
            id_of_table_csv_file2.csv, 0

            in our case subject column is always 0
            for proper testing, column shuffling is necessary
        """
        (entity, cells) = entityRowTuple
        subjectColumnIndex = 0

        properties = []
        for cell in cells:
            properties.append(cell['property'])

        subjectColumnIndex = properties.index("http://www.w3.org/2000/01/rdf-schema#label")

        subjectColumnAnnotationFilepath = os.path.join(SUBJECT_COLUMN_FOLDER, csvFilename)
        csvWriter = CsvWriter(subjectColumnAnnotationFilepath)
        row = [csvFilename, str(subjectColumnIndex + 1)]
        csvWriter.writerow(row)

    def getRows(self, entities):
        rows = []
        for num, entity in enumerate(entities):
            entityRowTuple = self.getRow(entity)
            #permutate first row to have a random header sequence
            if num == 0:
                (entity, row) = entityRowTuple
                permutatedRow = self.permutateRow(row)
                entityRowTuple = (entity, permutatedRow)
            rows.append(entityRowTuple)
        return rows

    def getRow(self, entity):
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT ?p ?o
            WHERE {<%s> ?p ?o}
        """ %(entity,))
        results = results["results"]["bindings"]
        row = []

        #append entity label as the first item
        row.append({
            "property": "http://www.w3.org/2000/01/rdf-schema#label",
            "label": "label",
            "value": self.getLabel(entity)
        })

        properties = []
        for _result in results:
            _property = _result["p"]["value"]
            object = _result["o"]["value"]
            _propertyLabel = self.getLabel(_property)
            if _propertyLabel != "" and (not _property in properties):
                row.append({
                    "property": _property,
                    "label": _propertyLabel,
                    "value": object
                })
                properties.append(_property)

        return (entity, row)

    def permutateRow(self, row):
        numberOfCols = len(row)
        for i in range(0, 1000):
            colA = random.randint(0, numberOfCols - 1)
            colB = colA
            while colB == colA:
                colB = random.randint(0, numberOfCols - 1)
            temp = row[colA]
            row[colA] = row[colB]
            row[colB] = temp
        return row

    def getLabel(self, s):
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT ?label
            WHERE {<%s> rdfs:label ?label}
        """ %(s,))
        results = results["results"]["bindings"]
        if len(results) == 0:
            return ""
        else:
            return results[0]["label"]["value"]
