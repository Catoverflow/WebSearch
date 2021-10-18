from logging import debug
from data_process import Data


# usage:InvertedIndex(x).process()
# output:x.docdic={word1:{doc1,doc2,doc3},word2:{doc1,doc2,doc3}}
# index of doc starts with 0
class InvertedIndex(object):
    def __init__(self, path='../data', maxfile=4):
        getdata = Data(path=path, maxfile=maxfile)
        getdata.load()
        data = getdata.data()
        self.data = list(data.values())
        self.docdic = {}

    def process(self):
        for doc in range(len(self.data)):
            for word in self.data[doc]:
                if word not in self.docdic:
                    self.docdic[word] = {doc}
                else:
                    self.docdic[word].add(doc)

    def printDocDic(self):
        print(self.docdic)

# aTest = InvertedIndex()
# aTest.process()
# aTest.printDocDic()
