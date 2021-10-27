from utils.data_process import Data
from utils.tf_idf import TF_IDF
from utils.inverted_index import Inverted_Index
import logging
import zstd
import pickle

save_dir = "output"
logging.basicConfig(level=logging.DEBUG)
logging.info("Loading data from files")
data = Data()
data.load("data",maxfile = 1000)
data.process()
wordcount = None
logging.info("Writing data to output")
with open(f'{save_dir}/inverted_index.zstd','wb') as f:
    ii = Inverted_Index(data.data,data.dict)
    ii.procecss()
    wordcount = ii.word_count
    logging.info("Compressing and saving inverted index")
    ii_data = pickle.dumps(ii.inverted_index)
    f.write(zstd.compress(ii_data))
    f.close()
with open(f'{save_dir}/tf_idf_matrix.zstd','wb') as f:
    tf_idf = TF_IDF(data.data,data.dict,wordcount)
    tf_idf.process()
    logging.info("Compressing and saving tf-idf matrix")
    tf_idf_data = pickle.dumps(tf_idf.tf_idf)
    f.write(zstd.compress(tf_idf_data))
    f.close()
with open(f'{save_dir}/dictionary.zstd','wb') as f:
    logging.info("Compressing and saving dictionary")  
    dict_data = pickle.dumps(data.dict)
    f.write(zstd.compress(dict_data))
    f.close()
with open(f'{save_dir}/metadata.zstd','wb') as f:
    logging.info("Compressing and saving metadata")  
    meta_data = pickle.dumps(data.metadata)
    f.write(zstd.compress(meta_data))
    f.close()