from numpy import byte
from utils.data_process import Data
from utils.tf_idf import TF_IDF
from utils.inverted_index import Inverted_Index
import logging
import zstd
import time

logging.basicConfig(level=logging.DEBUG)
data = Data()
data.load("data",1000)
data.process()
ii = Inverted_Index(data.data,data.dict)
ii.procecss()
tf_idf = TF_IDF(data.data,data.dict,ii.word_count)
tf_idf.process()

dat = str(ii.inverted_index)
print("Compressing inverted index table")
start = time.time()
cdat = zstd.compress(dat.encode("ascii"))
print(f"Compressed, ratio = {len(cdat)/len(dat)} in {time.time()-start}")
start = time.time()
logging.info("Decompressing...")
rdat = zstd.decompress(cdat)
print(f"Decompressed in {time.time()-start}")