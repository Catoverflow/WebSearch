from utils.data_process import Data
import logging

logging.basicConfig(level=logging.DEBUG)
data = Data()
data.load("data",1000)
data.process()