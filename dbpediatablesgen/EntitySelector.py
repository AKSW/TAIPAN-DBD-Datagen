from .QueryExecutor import QueryExecutor

class EntitySelector(object):
    def __init__(self):
        self.queryExecutor = QueryExecutor()

    def getEntities(self, _class):
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT ?entity
            WHERE {
                ?entity rdf:type <%s>
            }
        """ %(_class, ))

    def countEntities(self, _class):
        results = self.queryExecutor.executeQuery(u"""
            SELECT DISTINCT ?entity
            WHERE {
                ?entity rdf:type <%s>
            }
        """ %(_class, ))
        import ipdb; ipdb.set_trace()
