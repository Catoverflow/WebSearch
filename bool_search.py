import logging
import re
from utils.data_process import Data
from re import L, sub
class Bool_Search(object):
    def __init__(self, inverted_index, look_up_dict):
        self.ii = inverted_index
        self.lookup = {look_up_dict[wordid]:wordid for wordid in range(len(look_up_dict))}

    def _get_ii_(self, word):
        # query word not found in documentss
        if word not in self.lookup:
            return None
        return self.ii[self.lookup[word]]

    def search(self, query):
        l_bracket_stack = []
        query = Bool_Search._preprocess_(query)
        index = 0
        # resolve priority provided by brackets
        # and pass plain expression to self._process_
        while index < len(query):
            if query[index] == '(':
                l_bracket_stack.append(index)
                index += 1
            elif query[index] == ')':
                # match last left bracket
                l_bracket_index = l_bracket_stack.pop()
                # pop left bracket
                query.pop(l_bracket_index)
                # pop expression in between
                # replace right bracket with procssed single inverted index
                to_process = [query.pop(l_bracket_index) for i in range(0, index-l_bracket_index-1)]
                query[l_bracket_index] = Bool_Search.process(to_process)
                index = l_bracket_index + 1
            # pass bool keyword to process to handle, ignore
            elif query[index] == 'and' or query[index] == 'not' or query[index] == 'or':
                index += 1
            # replace word with corresponding inverted index
            else:
                query[index] = self._get_ii_(query[index])
                index += 1
            
        if index > 1:
            query[0] = Bool_Search.process(query)
        return query[0]

    @staticmethod
    def intersection(iia, iib):
        # handle circumstances in which one or more word is not found
        if iia == None or iib == None:
            return None
        i = 0
        j = 0
        res = []
        while i < len(iia) and j < len(iib):
            if iia[i] > iib[j]:
                j += 1
            elif iia[i] < iib[j]:
                i += 1
            else:
                res.append(iia[i])
                i += 1
                j += 1
        return res

    @staticmethod
    def strip(iia, iib):
        # handle circumstances in which one or more word is not found
        if iia == None:
            return None
        elif iib == None:
            return iia
        i = 0
        j = 0
        res = iia
        while i < len(res) and j < len(iib):
            if res[i] > iib[j]:
                j += 1
            elif res[i] < iib[j]:
                i += 1
            else:
                res.pop(i)
                j += 1
        return res
    
    @staticmethod
    def complement(iia, iib):
        # handle circumstances in which one or more word is not found
        if iia == None and iib == None:
            return None
        elif iia == None:
            return iib
        elif iib == None:
            return iia
        i = 0
        j = 0
        res = []
        while i < len(iia) and j < len(iib):
            if iia[i] > iib[j]:
                res.append(iib[j])
                j += 1
            elif iia[i] < iib[j]:
                res.append(iia[i])
                i += 1
            else:
                res.append(iia[i])
                i += 1
                j += 1
        if i < len(iia):
            res.extend(iia[i:])
        if j < len(iib):
            res.extend(iib[j:])
        return res

    # generate key word list from query string
    def _preprocess_(query):
        # add space before & after bracket for split
        query = sub('\(', ' ( ',query)
        query = sub('\)', ' ) ',query)
        # remove continuous spaces
        query = sub(' {2,}', ' ',query)
        query = query.lower()
        query = query.split()
        data = Data()
        data.lemma_word(query)
        return data.data[0]

    # calculate target inverted index by operator
    @staticmethod
    def process(ii_list):
        while len(ii_list) > 1:
            iia, op, iib = ii_list.pop(0), ii_list.pop(0), ii_list[0]
            if op == 'and':
                ii_list[0] = Bool_Search.intersection(iia, iib)
            elif op == 'or':
                ii_list[0] = Bool_Search.complement(iia, iib)
            elif op == 'not':
                ii_list[0] = Bool_Search.strip(iia, iib)
        return ii_list[0]

def load():
    import zstd
    import pickle
    with open('output/inverted_index.zstd','rb') as f:
        ii = zstd.decompress(f.read())
        ii = pickle.loads(ii)
        f.close()
    with open('output/dictionary.zstd','rb') as f:
        dictionary = zstd.decompress(f.read())
        dictionary = pickle.loads(dictionary)
        f.close()
    with open('output/metadata.zstd','rb') as f:
        metadata = zstd.decompress(f.read())
        metadata = pickle.loads(metadata)
        f.close()
    return ii, dictionary, metadata


if __name__ == '__main__':
    # Beware that python API limit data size to 2GB
    # Coz all source files' size = 1.9GB so we can ignore it safely
    logging.info("Loading data from file")
    ii, dictionary, metadata = load()
    bs = Bool_Search(ii, dictionary)
    print("Ctrl + C to exit")
    while True:
        query = input("Enter expression for bool search: ")
        res = bs.search(query)
        if res!= None:
            for docid in range(len(res)):
                print('{}\t{}'.format(docid+1,metadata[res[docid]]['title']))
        else:
            print('Not found')