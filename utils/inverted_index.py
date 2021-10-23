import logging

# usage: Inverted_Index.process()
# output:
#        word_count = wordid: count of docs in which word occurs
#        inverted_index = wordid: [doc1, doc2,...]
class Inverted_Index(object):
    def __init__(self, data, dictionary):
        self.data = data
        self.dict = dictionary
        self.inverted_index = {wordid:[] for wordid in range(len(self.dict))}
        self.word_count = []
        # lookup table for word and id

    def procecss(self):
        logging.info("Start generating inverted-index")
        for docid in range(len(self.data)):
            for wordid in self.data[docid]:
                if docid not in self.inverted_index[wordid]:
                    self.inverted_index[wordid].append(docid)
        self.word_count = [len(self.inverted_index[wordid]) for wordid in range(len(self.dict))]