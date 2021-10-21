import logging
from data_process import Data

# usage:InvertedIndex(x).process()
# output:x.docdic={word1:{doc1,doc2,doc3},word2:{doc1,doc2,doc3}}
# index of doc starts with 0
class InvertedIndex(object):
    def __init__(self, data, dictionary):
        self.data = data
        self.dict = dictionary
        self.inverted_index = {}
        for word in self.dict:
            self.inverted_index[word] = []

    def procecss(self):
        logging.info("Start generating inverted-index")
        for docid in range(len(self.data)):
            for word in self.data[docid]:
                self.inverted_index[word].append(docid)
            if docid % 1000 == 0:
                logging.debug(f'{docid} file processed')
    
    @property
    def inverted_index(self):
        return self.inverted_index

# aTest = InvertedIndex()
# aTest.process()
# aTest.printDocDic()
