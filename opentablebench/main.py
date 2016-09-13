import os

from .config import TABLE_FOLDER

from .ClassSelector import ClassSelector
from .EntitySelector import EntitySelector
from .TableGenerator import TableGenerator

if __name__ == "__main__":
    classSelector = ClassSelector()
    classes = classSelector.getClasses()

    entitySelector = EntitySelector()
    tableGenerator = TableGenerator()

    path, dirs, files = os.walk(TABLE_FOLDER).next()
    generatedTablesCount = len(files)
    #Can have more than 5 tables per class!
    classesToSkip = int(float(generatedTablesCount) / 5)

    for num, _class in enumerate(classes):
        print "Processing (%s out of %s): %s" %(num, len(classes), _class,)
        #We get 100 entities because of LIMIT in the SPARQL query
        entities = entitySelector.getEntities(_class)

        #20 entities per table --> 20 rows
        tableGenerator.generateTableOfLengthN(_class, entities, 20)
