#abandoned, due to inefficiency of synonym picking via word2vec
#you can try other models like BART
#pretrained data: https://github.com/RaRe-Technologies/gensim-data
#export GENSIM_DATA_DIR=$(pwd)/dataset/gensim-data
import gensim.downloader as api

model = api.load('word2vec-google-news-300')