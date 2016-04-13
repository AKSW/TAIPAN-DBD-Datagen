import codecs


class CsvWriter(object):
    def __init__(self, csvFilepath):
        self.csvFile = codecs.open(csvFilepath, "w", "utf-8")

    def writeheader(self, header):
        self.writerow(header)

    def writerow(self, row):
        quotedRow = []
        for item in row:
            quotedRow.append(u'"%s"'%(item,))

        rowToWrite = ",".join(quotedRow)
        try:
            self.csvFile.write(u"%s\n"%(rowToWrite,))
        except IOError as e:
            print "Failed to write to file: %s" % (str(e),)

    def close(self):
        self.csvFile.close()
