import csv
import uuid
import os

from .QueryExecutor import QueryExecutor
from .CsvWriter import CsvWriter
from .config import TABLE_FOLDER, PROPERTIES_FOLDER, SUBJECT_COLUMN_FOLDER

class TableGenerator(object):
    def __init__(self):
        self.queryExecutor = QueryExecutor()

    def generateTable(self, _class, entities):
        rows = self.getRows(entities)
        header = self.generateHeader(rows[0])
        tableId = self.generateTableId(_class)
        csvFilename = str(tableId) + ".csv"
        csvFilepath = os.path.join(TABLE_FOLDER, csvFilename)
        csvWriter = CsvWriter(csvFilepath)
        csvWriter.writeheader(header)

        for rowEntityTuple in rows:
            (entity, row) = rowEntityTuple
            row = self.unpackRow(row)
            import ipdb; ipdb.set_trace()
            csvWriter.writerow(row)

        csvFile.close()
        import ipdb; ipdb.set_trace()

    def unpackRow(self, row):
        unpackedRow = {}
        for cell in row:
            unpackedRow[cell['label']] = cell['value'].decode("utf-8")
        return unpackedRow

    def generateTableId(self, _class):
        """
            Create a unique deterministic ID from a class URI
        """
        return uuid.uuid5(uuid.NAMESPACE_URL, _class)

    def generateHeader(self, rowEntityTuple):
        """
            Generate CSV header
        """
        (entity, cells) = rowEntityTuple
        header = []
        for cell in cells:
            header.append(cell['label'])
        return header

    def generatePropertyAnnotation(self, rows):
        """
            "http://dbpedia.org/ontology/genre","","False","1"
            "http://dbpedia.org/ontology/computingPlatform","","False","2"
        """
        pass

    def generateSubjectColumnAnnotation(self, rows):
        """
            id_of_table_csv_file.csv, 5
            id_of_table_csv_file2.csv, 0
        """
        pass

    def getRows(self, entities):
        rows = []
        for entity in entities:
            entityRowTuple = self.getRow(entity)
            rows.append(entityRowTuple)
        return rows

    def getRow(self, entity):
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT ?p ?o
            WHERE {<%s> ?p ?o}
        """ %(entity,))
        results = results["results"]["bindings"]
        row = []
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
