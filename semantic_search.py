from os import stat
from nltk.corpus.reader.panlex_swadesh import PanlexSwadeshCorpusReader
from math import sqrt
from bool_search import Bool_Search
from utils.data_process import Data
from utils.tf_idf import TF_IDF
import logging


class Semantic_Search(object):
    # threshold is used to filter out documents which only include less than threshold * words in query
    def __init__(self, tf_idf_table, look_up_dict):
        self.ths = 0.5
        self.res = 10
        self.tf_idf = tf_idf_table
        # dict constructed from database
        self.lookup = {}
        for wordid in range(len(look_up_dict)):
            self.lookup[look_up_dict[wordid]] = wordid
        # dict constructed from query
        self.dict = []

    # convert wordid in query to id in database
    def _convert_(self, wordid):
        if self.dict[wordid] not in self.lookup.keys():
            return -1
        else:
            return self.lookup[self.dict[wordid]]

    def _gen_tf_(self, query):
        data = Data()
        self.dict = data.dict
        query = data.dump(query)
        data.process()
        tf = TF_IDF(data.data, data.dict, None)
        tf.gen_tf()
        query_tf = {}
        for wordid in tf.tf[0].keys():
            # ignore those words which are not in database
            if self._convert_(wordid) >= 0:
                query_tf[self._convert_(wordid)] = tf.tf[0][wordid]
        self.dict = data.dict
        return query_tf

    # add tf-idf length into calculation
    def search(self, query, threshold=0.5, return_results=10, len_weight = 0.5):
        self.ths = threshold
        self.res = return_results
        query_tf = self._gen_tf_(query)
        best_rank = [(0,0) for i in range(self.res)]
        for docid in range(len(self.tf_idf)):
            rescos, reslen = self.calcu(query_tf, self.tf_idf[docid])
            if rescos > best_rank[-1][0]:
                # calculate relavance
                best_rank[-1] = (rescos*(1-len_weight) + reslen*len_weight, docid)
                best_rank.sort(reverse=True)
        return best_rank

    # calculate cos value and length of vectors
    def calcu(self, query_tf, doc_tf_idf):
        if len(query_tf) == 0:
            return 0,0
        hit = 0
        for wordid in query_tf.keys():
            if wordid in doc_tf_idf:
                hit += 1
        if hit < self.ths*len(query_tf):
            return 0,0
        dotsum = 0
        len_q = 0
        len_d = 0
        for wordid, tf in query_tf.items():
            len_q += tf*tf
            if wordid in doc_tf_idf:
                dotsum += tf*doc_tf_idf[wordid]
                len_d += doc_tf_idf[wordid]*doc_tf_idf[wordid]
        if len_q == 0 or len_d == 0:
            return 0,0
        return dotsum/sqrt(len_q*len_d), sqrt(len_d)
        # try numpy's dot

def load():
    import zstd
    import pickle
    with open('output/tf_idf_matrix.zstd','rb') as f:
        tf_idf = zstd.decompress(f.read())
        tf_idf = pickle.loads(tf_idf)
        f.close()
    with open('output/dictionary.zstd','rb') as f:
        dictionary = zstd.decompress(f.read())
        dictionary = pickle.loads(dictionary)
        f.close()
    with open('output/metadata.zstd','rb') as f:
        metadata = zstd.decompress(f.read())
        metadata = pickle.loads(metadata)
        f.close()
    return tf_idf, dictionary, metadata


if __name__ == '__main__':
    # Beware that python API limit data size to 2GB
    # Coz all source files' size = 1.9GB so we can ignore it safely
    logging.info("Loading data from file")
    tf_idf, dictionary, metadata = load()
    ss = Semantic_Search(tf_idf, dictionary)
    print("Ctrl + C to exit")
    while True:
        query = input("Enter words for semantic search: ")
        res = ss.search(query, 0.5, 10, 0.6)
        for docid in range(len(res)):
            print('{}:\t{}'.format(res[docid][0],metadata[res[docid][1]]['title']))