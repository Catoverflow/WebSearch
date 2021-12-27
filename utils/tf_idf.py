# try tf-idf provided by sklearn
# tf-idf table cantains tremendous amount of zero, thus use triple tuple to store
# tf_idf format: [[doc1],[doc2],[doc3],...,doc[n]]
#          doc1: {wordid1:tf_idf}, {wordid2:tf_idf}, ... , {wordidn:tf_idf}
from math import log10
import logging
from numpy import var, sqrt, mean


class TF_IDF(object):
    def __init__(self, data, headerdata, dictionary, word_occur_count):
        self.data = data
        self.headerdata = headerdata
        self.dict = dictionary
        self.count = word_occur_count
        self.tf = []
        self.header_tf = []
        self.idf = []
        self.header_idf = []
        self.tf_idf = []
        self.header_tf_idf = []
        # each doc's tf-idf vector is set to follow the word order in dict

    def gen_tf(self):
        logging.info("Generating tf table")

        for docid in range(len(self.data)):
            if docid % 1000 == 0:
                logging.debug(f"TF for {docid} document generated")
            freq = {}
            for wordid in self.data[docid]:
                if wordid not in freq:
                    freq[wordid] = 1
                else:
                    freq[wordid] += 1
            for wordid in freq.keys():
                freq[wordid] = log10(1+freq[wordid])
            self.tf.append(freq)
        if self.headerdata == None:
            return
        for docid in range(len(self.headerdata)):
            freq = {}
            for wordid in self.headerdata[docid]:
                if wordid not in freq:
                    freq[wordid] = 1
                else:
                    freq[wordid] += 1
            for wordid in freq.keys():
                freq[wordid] = log10(1+freq[wordid])
            self.header_tf.append(freq)

    # idf_smooth
    def gen_idf(self):
        maxid = max([self.dict[word] for word in self.dict]) + 1
        logging.info("Generating idf table")
        self.idf = []
        self.header_idf = []
        for wordid in range(maxid):
            if wordid % 1000 == 0:
                logging.debug(f"IDF for {wordid} word generated")
            self.idf.append(log10(len(self.data)/(1+self.count[wordid]))+1)
            self.header_idf.append(
                log10(len(self.headerdata)/(1+self.count[wordid])) + 1)

    def gen_tf_idf(self):
        logging.info("Generating tf-idf table")
        for docid in range(len(self.data)):
            if docid % 1000 == 0:
                logging.debug(f"TF-IDF for {docid} document generated")
            dic = {}
            header_dic = {}
            for wordid in self.tf[docid].keys():
                dic.update({wordid: self.idf[wordid]*self.tf[docid][wordid]})
            for wordid in self.header_tf[docid].keys():
                header_dic.update(
                    {wordid: self.header_idf[wordid]*self.header_tf[docid][wordid]})
            self.tf_idf.append(dic)
            self.header_tf_idf.append(header_dic)

    def normalization(self):
        logging.info("Normanizing tf-idf")
        tf_idf_list = []
        header_tf_idf_list = []
        for docid in range(len(self.tf_idf)):
            tf_idf_list.extend(list(self.tf_idf[docid].values()))
            header_tf_idf_list.extend(list(self.header_tf_idf[docid].values()))
        # Studentized residual
        std_deviation = sqrt(var(tf_idf_list))
        header_std_deviation = sqrt(var(header_tf_idf_list))
        mean_value = mean(tf_idf_list)
        header_mean_value = mean(header_tf_idf_list)
        for docid in range(len(self.tf_idf)):
            for wordid in self.tf[docid].keys():
                self.tf_idf[docid][wordid] = (
                    self.tf_idf[docid][wordid] - mean_value)/std_deviation
            for wordid in self.header_tf[docid].keys():
                self.header_tf_idf[docid][wordid] = (
                    self.header_tf_idf[docid][wordid] - header_mean_value)/header_std_deviation

        # min_max scaling
        # max_value = max(tf_idf_list)
        # for docid in range(len(self.tf_idf)):
        #     for wordid in self.tf[docid].keys():
        #         self.tf_idf[docid][wordid] / max_value

    def process(self):
        self.gen_tf()
        self.gen_idf()
        self.gen_tf_idf()
        self.normalization()
        # linear normalization's factor will not effect the cos value of query string
        # thus omitted
