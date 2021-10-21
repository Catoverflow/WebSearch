# auto load raw files and generate corresponding lemmatized data
# usage: Data.load() load first, get raw files and lemmatizing them
#                    duplicate loading is auto-prevented
#        file_id: unique id for each file, ascending from 1
#        Data.data() get lemmatized data list
#                    data format: data = [[file1 word lis],[file2 word list],...]
#        Data.metadata() get metadata of file
#                    data format: metadata = [{file1 metadata dict},{file2 metadatadoct},...]
#        Data.dict() get word bag of all files
#                    data format: dict = {word1,word2,...}
from json import load
from os import walk
from re import sub
import logging

#use global variable to prevent duplicate loading
data = []
metadata = []
dict = set()

class Data(object):
    def __init__(self, path="./data", maxfile=-1,lemma_engine="nltk"):
        self.path = path
        self.poplist = set({})
        self.maxfile = maxfile
        self.lemma_engine = lemma_engine
        logging.info(f"maxfile is set to {self.maxfile}")

    def _dump_(self):
        file_id = 0
        logging.info('Loading all files, this may take a long time...')
        for (root, dirs, files) in walk(self.path):
            for file in files:
                with open(f'{root}/{file}', 'r') as f:
                    file_id += 1
                    rawdata = load(f)
                    data.append(rawdata["text"])
                    metadata.append({
                        "id": rawdata["uuid"],
                        "time": rawdata["published"],
                        "title": rawdata["title"],
                        "author": rawdata["author"],
                        "url": rawdata["url"]})
                    if file_id % 1000 == 0:
                        logging.info(f'{file_id} file loaded')
                    if file_id == self.maxfile:
                        logging.info(f'Maxfile reached, {file_id} file loaded')
                        return
        logging.info(f'All {file_id} file loaded')

    def _pre_process_(self):
        logging.info('Pre-processing files')
        for file_id in range(len(data)):
            data[file_id] = data[file_id].lower()
            # match most of valid email addresses
            data[file_id] =sub('\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b','',data[file_id])
            # match url
            data[file_id] =sub(r'((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*','',data[file_id])
            # match time
            data[file_id] =sub('[0-9]{1,}:[0-9]{1,}(:[0-9]{2})?(am|pm)?','',data[file_id])
            # match punctuation
            data[file_id] =sub(r'[^\w\s]','',data[file_id])
            # remove digit
            data[file_id] =sub('[0-9]+', '',data[file_id])
            # remove \n when crawled
            data[file_id] =sub('\\n', '',data[file_id])
            # remove multiple space
            data[file_id] =sub(' {2,}', ' ',data[file_id])
            data[file_id] = data[file_id].strip()

    def _spacy_lemma_(self):
        #deprecated due to low efficiency, stop words not implemented
        import spacy
        for file_id in range(len(data)):
            nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
            data[file_id] = [token.lemma_ for token in nlp(data[file_id])]
            if self.debug and file_id % 100 == 0:
                logging.info(f'{file_id} file lemmatized')
        logging.info(f'All {file_id} file lemmatized')

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
        for file_id in range(len(data)):
            lemmatizer = WordNetLemmatizer()
            wordlist = []
            for word in data[file_id].split(' '):
                if word not in stopword:
                    wordlist.append(word)
            data[file_id] = [lemmatizer.lemmatize(word, get_wordnet_pos(word))
                for word in wordlist]
            if file_id % 100 == 0:
                logging.info(f'{file_id} file lemmatized')
        logging.info(f'All {file_id} file lemmatized')
    
    def _lemma_(self):
        logging.info('Lemmatizing all files, this may take a longer time...')
        if self.lemma_engine == "nltk":
            logging.info("Lemmatization engine: NLTK")
            self._nltk_lemma_()
        elif self.lemma_engine == "spacy":
            logging.info("Lemmatization engine: SpaCy")
            self._spacy_lemma_()

    def _gen_dict_(self):
        if len(data) == 0:
            logging.error("data not loaded")
            return
        for file_id in range(len(data)):
            for word in data[file_id]:
                if word not in dict:
                    dict.add(word)
        
    def load(self):
        if len(data) == 0:
            self._dump_()
            self._pre_process_()
            self._lemma_()
            self.loaded = True
    
    @staticmethod
    def data(self):
        if len(data) == 0:
            self.load()
        return data

    @staticmethod
    def metadata(self):
        if len(metadata) == 0:
            self.load()
        return metadata

    @staticmethod
    def dict(self):
        if len(dict) == 0:
            self._gen_dict_()
            return dict