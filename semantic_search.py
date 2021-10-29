from os import stat
from nltk.corpus.reader.panlex_swadesh import PanlexSwadeshCorpusReader
from math import sqrt
from bool_search import Bool_Search
from utils.data_process import Data
from utils.tf_idf import TF_IDF
import logging


class Semantic_Search(object):
    # threshold is used to filter out documents which only include less than threshold * words in query
    def __init__(self, tf_idf_table, header_tf_idf_table, dictionary):
        self.ths = 0.5
        self.res = 10
        self.tf_idf = tf_idf_table
        self.header_tf_idf = header_tf_idf_table
        # dict constructed from database
        self.dict = dictionary

    def _gen_tf_(self, query):
        query = Data.dump(query)
        query_list = []
        for word in query:
            if word in self.dict:
                query_list.append(self.dict[word])
        tf = TF_IDF([query_list], None, None, None)
        tf.gen_tf()
        return tf.tf[0]

    # add tf-idf length into calculation
    def search(self, query, threshold=0.5, return_results=10, len_weight=0.5, header_weight=0.3):
        self.ths = threshold
        self.res = return_results
        query_tf = self._gen_tf_(query)
        best_rank = [(0, 0) for i in range(self.res)]
        for docid in range(len(self.tf_idf)):
            rescos, reslen = self.calcu(query_tf, self.tf_idf[docid])
            headercos, headerlen = self.calcu(
                query_tf, self.header_tf_idf[docid])
            res = header_weight*(len_weight*headerlen+(1-len_weight)*headercos) + \
                (1-header_weight)*(len_weight*reslen+(1-len_weight)*rescos)
            if res > best_rank[-1][0]:
                # calculate relavance
                best_rank[-1] = (res, docid)
                best_rank.sort(reverse=True)
        return best_rank

    # calculate cos value and length of vectors
    def calcu(self, query_tf, doc_tf_idf):
        if len(query_tf) == 0:
            return 0, 0
        hit = 0
        for wordid in query_tf.keys():
            if wordid in doc_tf_idf:
                hit += 1
        if hit < self.ths*len(query_tf):
            return 0, 0
        dotsum = 0
        len_q = 0
        len_d = 0
        for wordid, tf in query_tf.items():
            len_q += tf*tf
            if wordid in doc_tf_idf:
                dotsum += tf*doc_tf_idf[wordid]
                len_d += doc_tf_idf[wordid]*doc_tf_idf[wordid]
        if len_q == 0 or len_d == 0:
            return 0, 0
        return dotsum/sqrt(len_q*len_d), sqrt(len_d)
        # try numpy's dot


def load():
    import zstd
    import pickle
    with open('output/tf_idf_matrix.zstd', 'rb') as f:
        tf_idf = zstd.decompress(f.read())
        tf_idf = pickle.loads(tf_idf)
        f.close()
    with open('output/header_tf_idf_matrix.zstd', 'rb') as f:
        header_tf_idf = zstd.decompress(f.read())
        header_tf_idf = pickle.loads(header_tf_idf)
        f.close()
    with open('output/dictionary.zstd', 'rb') as f:
        dictionary = zstd.decompress(f.read())
        dictionary = pickle.loads(dictionary)
        f.close()
    with open('output/metadata.zstd', 'rb') as f:
        metadata = zstd.decompress(f.read())
        metadata = pickle.loads(metadata)
        f.close()
    return tf_idf, header_tf_idf, dictionary, metadata


if __name__ == '__main__':
    # Beware that python API limit data size to 2GB
    # Coz all source files' size = 1.9GB so we can ignore it safely
    logging.info("Loading data from file")
    tf_idf, header_tf_idf, dictionary, metadata = load()
    ss = Semantic_Search(tf_idf, header_tf_idf, dictionary)
    print("Ctrl + C to exit")
    while True:
        query = input("Enter words for semantic search: ")
        res = ss.search(query, 0.5, 10, 0.6)
        if res[0][0] == 0:
            print('Not found')
        else:
            for docid in range(len(res)):
                if(res[docid][0] > 0):
                    print('{}:\t{}'.format(res[docid][0],
                                           metadata[res[docid][1]]['title']))
