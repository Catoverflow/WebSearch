from math import log10
import logging
class TF_IDF(object):
    def __init__(self,data,dictionary,word_occur_count):
        self.data = data
        self.dict = dictionary
        self.count = word_occur_count
        self.tf = []
        self.idf =[]
        self.tf_idf = []
        # each doc's tf-idf vector is set to follow the word order in dict

    def _gen_tf_(self):
        logging.info("Generating tf table")

        for docid in range(len(self.data)):
            freq = {}
            for word in self.data[docid]:
                if word not in freq:
                    freq[word] = 1
                else:
                    freq[word] += 1
            doctf = []
            for word in self.dict:
                if word in freq.keys():
                    doctf.append(log10(1+freq[word]/len(self.data[docid])))
                else:
                    doctf.append(0)
            self.tf.append(doctf)

    #idf_smooth
    def _gen_idf_(self):
        logging.info("Generating idf table")
        self.idf = [log10(len(self.data)/(1+self.count[wordid]))+1 for wordid in range(len(self.dict))]

    def _gen_tf_idf_(self):
        logging.info("Generating tf-idf table")
        for docid in range(len(self.data)):
            self.tf_idf.append([self.idf[wordid]*self.tf[docid][wordid] for wordid in range(len(self.dict))])

    def process(self):
        self._gen_tf_()
        self._gen_idf_()
        self._gen_tf_idf_()