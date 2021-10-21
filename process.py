from utils.data_process import Data
from utils.tf_idf import TF_IDF
from utils.inverted_index import Inverted_Index
import logging

logging.basicConfig(level=logging.DEBUG)
data = Data()
data.load("data",10)
data.process()
ii = Inverted_Index(data.data,data.dict)
ii.procecss()
tf_idf = TF_IDF(data.data,data.dict,ii.word_count)
tf_idf.process()