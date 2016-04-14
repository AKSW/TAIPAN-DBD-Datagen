import os

from dbpediatablegen.config import TABLE_FOLDER

from dbpediatablegen.ClassSelector import ClassSelector
from dbpediatablegen.EntitySelector import EntitySelector
from dbpediatablegen.TableGenerator import TableGenerator

if __name__ == "__main__":
    classSelector = ClassSelector()
    classCount = classSelector.getClassCount()
    classes = classSelector.getClasses()
    randomSelection = classSelector.generateRandomSelection(200)
    randomClasses = classSelector.getRandomClasses()

    entitySelector = EntitySelector()
    tableGenerator = TableGenerator()

    path, dirs, files = os.walk(TABLE_FOLDER).next()
    generatedTablesCount = len(files)
    classesToSkip = int(float(generatedTablesCount) / 5)

    for num, _class in enumerate(randomClasses):
        if num < classesToSkip:
            continue
        print "Processing: %s" %(_class,)
        #We get 100 entities because of LIMIT in the SPARQL query
        entities = entitySelector.getEntities(_class)
        #20 entities per table --> 20 rows
        tableGenerator.generateTableOfLengthN(_class, entities, 20)
