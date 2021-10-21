from data_process import Data
from math import log10
import logging
class TF_IDF(object):
    def __init__(self,data,dictionary,word_occur_count):
        self.data = data
        self.dict = dictionary
        self.count = word_occur_count
        self.tf = {}
        self.idf = {}
        self.tf_idf = {}

    def _gen_tf_(self):
        logging.info("Generating tf table")
        for word in self.dict:
            freq = 0
            self.tf[word] = []
            for docid in range(len(self.data)):
                for oword in self.data[docid]:
                    if word == oword:
                        freq += 1
                self.tf[word].append(1+log10(freq/len(self.data[docid])))
                if docid % 1000 == 0:
                    logging.debug(f'{docid} file processed')
        pass # switch to count word only in doc
    
    def _gen_idf_(self):
        logging.info("Generating idf table")
        for word in self.dict:
            self.idf[word] = []
            for docid in range(len(self.data)):
                self.idf[word].append(log10(len(self.data[docid])/len(self.count[word])+1))
                if docid % 1000 == 0:
                    logging.debug(f'{docid} file processed')
            pass

    def _gen_tf_idf_(self):
        logging.info("Generating tf-idf table")
        for word in self.dict:
            self.tf_idf[word] = self.tf[word]*self.idf[word]

    @property
    def tf_idf(self):
        return self.td_idf