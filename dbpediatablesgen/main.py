from dbpediatablesgen.ClassSelector import ClassSelector

if __name__ == "__main__":
    classSelector = ClassSelector()
    classCount = classSelector.getClassCount()
    classes = classSelector.getClasses()
    randomSelection = classSelector.generateRandomSelection(100)
    randomClasses = classSelector.getRandomClasses()
    import ipdb; ipdb.set_trace()
