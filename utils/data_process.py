from json import load
from os import popen, walk
from re import sub

#use global variable to prevent duplicate loading
data = {}
metadata = {}
class Data(object):
    def __init__(self, path="./data", maxfile=-1,debug=False,lemma_engine="nltk"):
        self.path = path
        self.poplist = set({})
        self.maxfile = maxfile
        self.debug = debug
        self.lemma_engine = lemma_engine
        print(f"DEBUG: maxfile is set to {self.maxfile}")

    def _dump_(self):
        file_id = 0
        if self.debug: print('DEBUG: Loading all files, this may take a long time...')
        for (root, dirs, files) in walk(self.path):
            for file in files:
                with open(f'{root}/{file}', 'r') as f:
                    file_id += 1
                    rawdata = load(f)
                    data[file_id] = rawdata["text"]
                    metadata[file_id] = {
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
        if self.debug: print('DEBUG: Pre-processing files')
        for file_id in data:
            data[file_id] = data[file_id].lower()
            # match most of valid email addresses
            data[file_id] =sub('\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b','',data[file_id])
            # match url
            data[file_id] =sub('((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*','',data[file_id])
            # match punctuation
            data[file_id] =sub(r'[^\w\s]','',data[file_id])
            # match time
            data[file_id] =sub('[0-9]{1,}:[0-9]{1,}(:[0-9]{2})?(am|pm)?','',data[file_id])
            data[file_id] =sub(' {2,}|\\n', ' ',data[file_id])
            data[file_id] = data[file_id].strip()

    def _spacy_lemma_(self):
        #deprecated due to low efficiency, stop words not implemented
        import spacy
        for file_id in data:
            nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
            data[file_id] = [token.lemma_ for token in nlp(data[file_id])]
            if self.debug and file_id % 100 == 0:
                print(f'DEBUG: {file_id} file lemmatized')
        if self.debug: print(f'DEBUG: All {file_id} file lemmatized')

    def _nltk_lemma_(self):
        import nltk
        from nltk.stem import WordNetLemmatizer 
        from nltk.corpus import wordnet, stopwords
        #this method owe to https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
        def get_wordnet_pos(word):
            tag = nltk.pos_tag([word])[0][1][0].upper()
            tag_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)
        stopword = set(stopwords.words('english'))            
        for file_id in data:
            lemmatizer = WordNetLemmatizer()
            wordlist = []
            for word in data[file_id].split(' '):
                if word not in stopword:
                    wordlist.append(word)
            data[file_id] = [lemmatizer.lemmatize(word, get_wordnet_pos(word))
                for word in wordlist]
            if self.debug and file_id % 100 == 0:
                print(f'DEBUG: {file_id} file lemmatized')
        if self.debug: print(f'DEBUG: All {file_id} file lemmatized')
    
    def _lemma_(self):
        if self.debug: print('DEBUG: Lemmatizing all files, this may take a longer time...')
        if self.lemma_engine == "nltk":
            if self.debug: print("DEBUG: Lemmatization engine: NLTK")
            self._nltk_lemma_()
        elif self.lemma_engine == "spacy":
            if self.debug: print("DEBUG: Lemmatization engine: SpaCy")
            self._spacy_lemma_()
        
    def load(self):
        if len(data) == 0:
            self._dump_()
            self._pre_process_()
            self._lemma_()
            self.loaded = True
        if self.debug:
            while True:
                file_id = int(input("DEBUG: choose a config to show(number): "))
                print(data[file_id])
                print('-------metadata-------')
                print(metadata[file_id])
    
    @staticmethod
    def data():
        return data

    @staticmethod
    def metadata():
        return metadata