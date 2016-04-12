import random

from SPARQLWrapper import SPARQLWrapper, JSON

from .config import DBPEDIA_SPARQL_ENDPOINT, DBPEDIA_DEFAULT_GRAPH, RANDOM_CLASS_SELECTION

class ClassSelector(object):
    def __init__(self):
        self.dbpediaEndpoint = SPARQLWrapper(DBPEDIA_SPARQL_ENDPOINT)
        self.dbpediaEndpoint.setReturnFormat(JSON)
        self.dbpediaEndpoint.addDefaultGraph(DBPEDIA_DEFAULT_GRAPH)

    def getClasses(self):
        results = self.executeQuery(u"""
            SELECT DISTINCT ?class
            WHERE {?class rdf:type owl:Class}
        """)
        results = results["results"]["bindings"]
        classes = []
        for _result in results:
            _class = _result["class"]["value"]
            if(_class.startswith("http://")):
                classes.append(_class)
        return classes

    def generateRandomSelection(self, n):
        """
            Random, generates sequence of indexes
        """
        classes = self.getClasses()
        randomSample = random.sample(classes, n)
        indexes = []
        for item in randomSample:
            indexes.append(classes.index(item))
        return indexes

    def getRandomClasses(self):
        """
            Deterministic, depends on config.py
            In experiments we use 100 random classes
            Which is 12.6% of overall classes (out of 791)
            Measured on 12.04.2016
        """
        classes = self.getClasses()
        randomIndexes = eval(RANDOM_CLASS_SELECTION)
        randomClasses = []
        for index in randomIndexes:
            randomClasses.append(classes[index])
        return randomClasses

    def getClassCount(self):
        results = self.executeQuery(u"""
            SELECT DISTINCT COUNT(?class)
            WHERE {?class rdf:type owl:Class}
        """)
        return int(results["results"]["bindings"][0]["callret-0"]["value"])

    def executeQuery(self, query):
        self.dbpediaEndpoint.setQuery(query)
        results = self.dbpediaEndpoint.query().convert()
        return results
