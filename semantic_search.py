from nltk.corpus.reader.panlex_swadesh import PanlexSwadeshCorpusReader
from math import sqrt
from utils.data_process import Data
from utils.tf_idf import TF_IDF

ths = 0.5
res = 10
class Semantic_Search(object):
    # threshold is used to filter out documents which only include less than threshold * words in query
    def __init__(self, tf_idf_table, look_up_dict, threshold = 0.5, return_results = 10):
        self.tf_idf = tf_idf_table
        # dict constructed from database
        self.lookup = {}
        for wordid in range(len(look_up_dict)):
            self.lookup[look_up_dict[wordid]] = wordid
        # dict constructed from query
        self.dict = []
        ths = threshold
        res = return_results

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
            #ignore those words which are not in database
            if self._convert_(wordid) >= 0:
                query_tf[self._convert_(wordid)]=tf.tf[0][wordid]
        self.dict = data.dict
        return query_tf

    def search(self, query):
        query_tf = self._gen_tf_(query)
        best_rank = [0 for i in range(res)]
        for doc_tf_idf in self.tf_idf:
            vcos = Semantic_Search.cos(query_tf,doc_tf_idf)
            if vcos > best_rank[-1]:
                best_rank[-1] = vcos
                best_rank.sort(reverse=True)
        return best_rank

    @staticmethod
    def cos(query_tf, doc_tf_idf):
        if len(query_tf) == 0:
            return 0
        hit = 0
        for wordid in query_tf.keys():
            if wordid in doc_tf_idf:
                hit+=1
        if hit < ths*len(query_tf):
            return 0
        dotsum = 0
        len_q = 0
        len_d = 0
        for wordid, tf in query_tf.items():
            len_q += tf*tf
            if wordid in doc_tf_idf:
                dotsum += tf*doc_tf_idf[wordid]
                len_d += doc_tf_idf[wordid]*doc_tf_idf[wordid]
        return dotsum/sqrt(len_q*len_d)
        # try numpy's dot