# try tf-idf provided by sklearn
# tf-idf table cantains tremendous amount of zero, thus use triple tuple to store
# tf_idf format: [[doc1],[doc2],[doc3],...,doc[n]]
#          doc1: {wordid1:tf_idf}, {wordid2:tf_idf}, ... , {wordidn:tf_idf}
from math import log10
import logging
from numpy import var, sqrt


class TF_IDF(object):
    def __init__(self, data, dictionary, word_occur_count, header_weight=0.5):
        self.data = data
        self.dict = dictionary
        self.count = word_occur_count
        self.tf = []
        self.idf = []
        self.tf_idf = []
        self.header_weight = header_weight
        # each doc's tf-idf vector is set to follow the word order in dict

    def gen_tf(self):
        logging.info("Generating tf table")

        for docid in range(len(self.data)):
            freq = {}
            for wordid in self.data[docid]:
                if wordid not in freq:
                    freq[wordid] = 1
                else:
                    freq[wordid] += 1
            for wordid in freq.keys():
                freq[wordid] = log10(1+freq[wordid]/len(self.data[docid]))
            self.tf.append(freq)

    # idf_smooth
    def _gen_idf_(self):
        logging.info("Generating idf table")
        self.idf = [log10(len(self.data)/(1+self.count[wordid])) +
                    1 for wordid in range(len(self.dict))]

    def _gen_tf_idf_(self):
        logging.info("Generating tf-idf table")
        for docid in range(len(self.data)):
            dic = {}
            for wordid in self.tf[docid].keys():
                dic.update({wordid: self.idf[wordid]*self.tf[docid][wordid]})
            self.tf_idf.append(dic)

    def _normalization_(self):
        logging.info("Normanizing tf-idf")
        tf_idf_list = []
        for docid in range(len(self.tf_idf)):
            tf_idf_list.extend(
                [tf_idf for tf_idf in self.tf_idf[docid].values()])
        std_deviation = sqrt(var(tf_idf_list))
        for docid in range(len(self.tf_idf)):
            for wordid in self.tf[docid].keys():
                self.tf_idf[docid][wordid] /= std_deviation

    def process(self):
        self.gen_tf()
        self._gen_idf_()
        self._gen_tf_idf_()
        # self._normalization_()
        # linear normalization's factor will not effect the cos value of query string
        # thus omitted
