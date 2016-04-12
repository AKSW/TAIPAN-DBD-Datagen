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
    entities = entitySelector.getEntities(randomClasses[0])

    tableGenerator = TableGenerator()
    #5 columns
    tableGenerator.generateTable(randomClasses[0], entities[:5])



    import ipdb; ipdb.set_trace()
