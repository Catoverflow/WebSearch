import logging
from os import stat
from utils.data_process import Data
from re import L, sub
class Bool_Search(object):
    def __init__(self, inverted_index, look_up_dict):
        self.ii = inverted_index
        self.lookup = look_up_dict

    def get_ii(self, word):
        return self.ii[self.lookup[word]]

    def search(self, query):
        bracket_stack = []
        query = self._preprocess_(query)
        index = 0
        # resolve priority provided by brackets
        # and pass plain expression to self._process_
        while index < len(query):
            if query[index] == '(':
                bracket_stack.append({'(':index})
            elif query[index] == ')':
                # match last left bracket
                l_bracket_index = bracket_stack.pop()['(']
                # pop left bracket
                query.pop(l_bracket_index)
                # pop expression in between
                # replace right bracket with procssed single inverted index
                to_process = [query.pop(l_bracket_index) for i in range(0, index-l_bracket_index-1)]
                query[l_bracket_index] = self._process_(to_process)
                index = l_bracket_index + 1
                pass
            elif query[index] != 'and' and query[index] != 'not' and query[index] != 'or':
                # replace word with corresponding inverted index
                query[index] = self.get_ii()
        if index > 1:
            query = self._process_(query)

    @staticmethod
    def intercetion(iia, iib):
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
        return res

    # generate key word list from query string
    def _preprocess_(query):
        # add space before & after bracket for split
        query = sub('(', ' ( ',query)
        query = sub(')', ' ) ',query)
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
                ii_list[0] = Bool_Search.complement(iia, iib)
            elif op == 'or':
                ii_list[0] = Bool_Search.union(iia, iib)
            elif op == 'not':
                ii_list[0] = Bool_Search.strip(iia, iib)
        return ii_list