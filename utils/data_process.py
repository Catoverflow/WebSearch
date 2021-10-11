from json import load
from os import popen, walk
from re import sub
class Data(object):
    def __init__(self, path="./data", maxfile=-1,debug=False,lemma_engine="nltk"):
        self.path = path
        self.poplist = set({})
        self.maxfile = maxfile
        self.data = {}
        self.metadata = {}
        self.debug = debug
        self.lemma_engine = lemma_engine

    def _dump_(self):
        file_id = 0
        print('DEBUG: Loading all files, this may take a long time...')
        for (root, dirs, files) in walk(self.path):
            for file in files:
                with open(f'{root}/{file}', 'r') as f:
                    file_id += 1
                    rawdata = load(f)
                    self.data[file_id] = rawdata["text"]
                    self.metadata[file_id] = {
                        "id": rawdata["uuid"],
                        "time": rawdata["published"],
                        "title": rawdata["title"],
                        "author": rawdata["author"],
                        "url": rawdata["url"]}
                    if self.debug and file_id % 1000 == 0:
                        print(f'DEBUG: {file_id} file loaded')
                    if self.debug and file_id == self.maxfile:
                        print(f'DEBUG: Maxfile reached, {file_id} file loaded')
                        return
        if self.debug: print(f'DEBUG: All {file_id} file loaded')

    def _pre_process_(self):
        for file_id in self.data:
            self.data[file_id] = self.data[file_id].lower()
            # match most of valid email addresses
            self.data[file_id] =sub('\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b','',self.data[file_id])
            # match url
            self.data[file_id] =sub('((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*','',self.data[file_id])
            # match punctuation
            self.data[file_id] =sub(r'[^\w\s]','',self.data[file_id])
            self.data[file_id] =sub(' {2,}', ' ',self.data[file_id])
            self.data[file_id] = self.data[file_id].strip()

    def _spacy_lemma_(self):
        import spacy
        # amazingly slow
        for file_id in self.data:
            nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
            self.data[file_id] = [token.lemma_ for token in nlp(self.data[file_id])]
            if self.debug and file_id % 100 == 0:
                print(f'DEBUG: {file_id} file lemmatized')
        if self.debug: print(f'DEBUG: All {file_id} file lemmatized')

    def _nltk_lemma_(self):
        import nltk
        from nltk.stem import WordNetLemmatizer 
        from nltk.corpus import wordnet
        def get_wordnet_pos(word):
            tag = nltk.pos_tag([word])[0][1][0].upper()
            tag_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}

            return tag_dict.get(tag, wordnet.NOUN)
        for file_id in self.data:
            lemmatizer = WordNetLemmatizer()
            self.data[file_id] = [lemmatizer.lemmatize(w, get_wordnet_pos(w))
                for w in self.data[file_id].split(' ')]
            if self.debug and file_id % 100 == 0:
                print(f'DEBUG: {file_id} file lemmatized')
        if self.debug: print(f'DEBUG: All {file_id} file lemmatized')
    
    def _lemma_(self):
        print('DEBUG: Loading all files, this may take a longer time...')
        if self.lemma_engine == "nltk":
            if self.debug:
                print("DEBUG: Lemmatization engine: NLTK")
            self._nltk_lemma_()
        elif self.lemma_engine == "spacy":
            if self.debug:
                print("DEBUG: Lemmatization engine: SpaCy")
            self._spacy_lemma_()

    def load(self):
        self._dump_()
        self._pre_process_()
        self._lemma_()
        if self.debug:
            file_id = int(input("DEBUG: choose a config to show(number): "))
            print(self.data[file_id])
            print('-------metadata-------')
            print(self.metadata[file_id])