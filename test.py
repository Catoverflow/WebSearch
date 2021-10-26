from bool_search import Bool_Search
from utils.data_process import Data
from utils.tf_idf import TF_IDF
from utils.inverted_index import Inverted_Index
from semantic_search import Semantic_Search
import logging
import zstd
import pickle
import time

logging.basicConfig(level=logging.DEBUG)
data = Data()
data.load("data",1)
data.process()
print([data.dict[wordid] for wordid in data.data[0][0:20]])
ii = Inverted_Index(data.data,data.dict)
ii.procecss()
tf_idf = TF_IDF(data.data,data.dict,ii.word_count)
tf_idf.process()
ss = Semantic_Search(tf_idf.tf_idf, data.dict, 0.5, 10)
bs = Bool_Search(ii.inverted_index, data.dict)
#logging.info("Serializing inverted index table")
#dat = pickle.dumps(ii.inverted_index)
#logging.info("Compressing inverted index table")
#start = time.time()
#cdat = zstd.compress(dat.encode("ascii"))
#logging.info(f"Compressed, ratio = {len(cdat)/len(dat)} in {time.time()-start}")
#start = time.time()
#logging.info("Decompressing...")
#rdat = zstd.decompress(cdat)
#logging.info(f"Decompressed in {time.time()-start}")
while True:
    query = input("semantic search: ")
    #res = ss.search(query)
    res = bs.search(query)
    if res != None:
        print([data.metadata[docid] for docid in res])
    else:
        print("404")