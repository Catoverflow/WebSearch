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
            self.data.append(data[docid] + headerdata[docid])
        self.dict = dictionary
        self.maxid = max([self.dict[word] for word in self.dict]) + 1
        self.inverted_index = [[] for i in range(self.maxid)]
        self.word_count = []
        # lookup table for word and id

    def procecss(self):
        logging.info("Generating inverted-index")
        for docid in range(len(self.data)):
            if docid %1000 == 0:
                logging.debug(f"Inverted index generated for {docid} document")
            for wordid in self.data[docid]:
                if len(self.inverted_index[wordid]) == 0 or self.inverted_index[wordid][-1] != docid:
                    self.inverted_index[wordid].append(docid)
        self.word_count = [len(self.inverted_index[wordid]) for wordid in range(self.maxid)]