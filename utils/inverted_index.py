import logging

# usage:InvertedIndex(x).process()
# output:x.docdic={word1:{doc1,doc2,doc3},word2:{doc1,doc2,doc3}}
# index of doc starts with 0
class Inverted_Index(object):
    def __init__(self, data, dictionary):
        self.data = data
        self.dict = dictionary
        self.inverted_index = {word:[] for word in self.dict}
        self.word_count = []

    def procecss(self):
        logging.info("Start generating inverted-index")
        for docid in range(len(self.data)):
            for word in self.data[docid]:
                self.inverted_index[word].append(docid)
            if docid % 1000 == 0:
                logging.debug(f'{docid} file processed')
        self.word_count = [len(self.inverted_index[word]) for word in self.dict]