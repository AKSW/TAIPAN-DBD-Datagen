import codecs


class CsvWriter(object):
    def __init__(self, csvFilepath):
        self.csvFile = codecs.open(csvFilepath, "w", "utf-8")

    def writeheader(self, header):
        quotedHeader = []
        for item in header:
            quotedHeader.append(u'"%s"'%(item,))

        rowToWrite = ",".join()
        self.csvFile.write()
        import ipdb; ipdb.set_trace()

    def writerow(self, row):
        pass
