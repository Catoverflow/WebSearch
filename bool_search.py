# {A:{b,c,d}}，从倒排表建立的字典
# DIC = {'the': {0, 1, 2, 3, 4, 5}, 'a': {0, 1, 2, 3, 4, 5}, 'one': {1}, 'two': {2}, 'three': {3}}


# userage: BoolSearch(docdic).processAndPrint()
# docdic:example:{'the': {0, 1, 2, 3, 4, 5}, 'a': {0, 1, 2, 3, 4, 5}, 'one': {1}, 'two': {2}, 'three': {3}}
class BoolSearch(object):
    # init class with given inverted_index
    def __init__(self, docdic):
        self._docdic = docdic
        self._reversedchar = {"and", "or", "not", "(", ")"}
        self._inlist = []
        self._most = set()

    # input, preprocess and calcute the universial set
    def _getInputAndMost_(self):
        inputchr = input("BoolSearch***Input:\n")
        self._inlist = [i if i in self._reversedchar else self._docdic[i] for i in
                        inputchr.lower().replace('(', " ( ").replace(')', " ) ").split()]
        for key in self._inlist:
            if isinstance(key, set):
                self._most.union(key)

    # set calculate
    def _calculate_(self, partlist):
        calist = partlist
        while len(calist) > 1:
            if "not" in calist:
                for j in range(len(calist)):
                    if calist[j] == "not":
                        calist[j + 1] = self._most.difference(calist[j + 1])
                        del (calist[j])
                        break
            else:
                for j in range(len(calist)):
                    if calist[j] == "and":
                        calist[j + 1] = calist[j - 1].intersection(calist[j + 1])
                        del (calist[j - 1:j + 1])
                        break
                    if calist[j] == "or":
                        calist[j + 1] = calist[j - 1].union(calist[j + 1])
                        del (calist[j - 1:j + 1])
                        break
        return calist

    # Recursively handle backets
    def _backetProcess_(self):
        if ")" in self._inlist:
            r_index = self._inlist.index(")")
            inputlist_temp = self._inlist[:r_index]
            l_index = 0
            for i in range(len(inputlist_temp)):
                if inputlist_temp[i] == "(":
                    l_index = i
            inputlist_temp = self._inlist[l_index + 1:r_index]
            self._inlist[l_index:r_index + 1] = self._calculate_(inputlist_temp)
            self._backetProcess_()
        return self._calculate_(self._inlist)

    # External interface
    def processAndPrint(self):
        self._getInputAndMost_()
        print(self._backetProcess_())

# aBoolSearchTest = BoolSearch(DIC)
# aBoolSearchTest.processAndPrint()
