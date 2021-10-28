import logging

# usage: Inverted_Index.process()
# output:
#        word_count = wordid: count of docs in which word occurs
#        inverted_index = [doc1, doc2,...], [doc, ...], ...
#                           ↑ index = wordid
class Inverted_Index(object):
    def __init__(self, data, headerdata, dictionary):
        self.data = []
        for docid in range(len(data)):
            self.data[docid] = data[docid] + headerdata[docid]
        self.dict = dictionary
        self.inverted_index = [[] for wordid in range(len(self.dict))]
        self.word_count = []
        # lookup table for word and id

    def procecss(self):
        logging.info("Start generating inverted-index")
        for docid in range(len(self.data)):
            for wordid in self.data[docid]:
                if docid not in self.inverted_index[wordid]:
                    self.inverted_index[wordid].append(docid)
        self.word_count = [len(self.inverted_index[wordid]) for wordid in range(len(self.dict))]