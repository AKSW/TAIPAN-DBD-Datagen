from SPARQLWrapper import SPARQLWrapper, JSON

from .config import DBPEDIA_SPARQL_ENDPOINT, DBPEDIA_DEFAULT_GRAPH

class QueryExecutor(object):
    def __init__(self):
        self.dbpediaEndpoint = SPARQLWrapper(DBPEDIA_SPARQL_ENDPOINT)
        self.dbpediaEndpoint.setReturnFormat(JSON)
        self.dbpediaEndpoint.addDefaultGraph(DBPEDIA_DEFAULT_GRAPH)

    def executeQuery(self, query):
        self.dbpediaEndpoint.setQuery(query)
        results = self.dbpediaEndpoint.query().convert()
        return results
