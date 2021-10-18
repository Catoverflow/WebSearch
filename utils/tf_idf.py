from data_process import Data
from math import log2 as log
from inverted_index import InvertedIndex

class TF_IDF(object):
    def __init__(self,path='../data',maxfile=20):
        data = Data(path,maxfile).load()
        self.path = path
        self.maxfile = maxfile
        self.data = data.data()
        self.dict = data.dict()
        self.tf = {}
        self.idf = {}
        self.tf_idf = {}

    def _gen_tf_(self):
        for word in self.dict:
            freq = 0
            self.tf[word] = []
            for file_id in self.data:
                for oword in self.data[file_id]:
                    if word == oword:
                        freq += 1
                self.tf[word].append(freq/len(self.data[file_id]))
    
    def _gen_idf_(self):
        invert = InvertedIndex(self.path,self.maxfile)
        invert.process()
        for word in self.dict:
            self.idf[word] = []
            for file_id in self.data:
                self.idf[word]= log(len(self.data[file_id])/len(invert.docdic))

    def _gen_tf_idf_(self):
        for word in self.dict:
            self.tf_idf[word] = self.tf[word]*self.idf[word]