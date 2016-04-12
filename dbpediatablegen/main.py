from dbpediatablegen.ClassSelector import ClassSelector
from dbpediatablegen.EntitySelector import EntitySelector

if __name__ == "__main__":
    classSelector = ClassSelector()
    classCount = classSelector.getClassCount()
    classes = classSelector.getClasses()
    randomSelection = classSelector.generateRandomSelection(100)
    randomClasses = classSelector.getRandomClasses()

    entitySelector = EntitySelector()
    entitySelector.countEntities(randomClasses[0])

    import ipdb; ipdb.set_trace()
