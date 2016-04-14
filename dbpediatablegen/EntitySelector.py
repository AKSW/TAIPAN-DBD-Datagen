from .QueryExecutor import QueryExecutor

class EntitySelector(object):
    def __init__(self):
        self.queryExecutor = QueryExecutor()

    def getEntities(self, _class):
        """
            Request 100 entities for a given _class
        """
        print "Getting entities for %s" %(_class,)
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT ?entity
            WHERE {
                ?entity rdf:type <%s>
            } LIMIT 100
        """ %(_class, ))
        results = results["results"]["bindings"]
        entities = []
        for _result in results:
            entities.append(_result["entity"]["value"])
        return entities

    def countEntities(self, _class):
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT COUNT(?entity)
            WHERE {
                ?entity rdf:type <%s>
            }
        """ %(_class, ))
        return int(results['results']['bindings'][0]['callret-0']['value'])
