# auto load raw files and generate corresponding lemmatized data
# usage: Data.load() load first, get raw files and lemmatizing them
#                    duplicate loading is auto-prevented
#        file_id: unique id for each file, ascending from 1
#        Data.data() get lemmatized data list
#                    data format: data = [[file1 word lis],[file2 word list],...]
#        Data.metadata() get metadata of file
#                    data format: metadata = [{file1 metadata dict},{file2 metadatadoct},...]
#        Data.dict() get word bag of all files
#                    data format: dict = [word1,word2,...]
#                    use list instead of set is to keep words in order
from json import load
from os import walk
from re import sub
import logging

class Data(object):
    def __init__(self):
        self.data = []
        self.metadata = []
        self.dict = []

    def load(self, path="./data", maxfile=-1):
        logging.info(f"maxfile is set to {maxfile}")
        file_id = 0
        logging.info('Loading all files, this may take a long time...')
        for (root, dirs, files) in walk(path):
            for file in files:
                with open(f'{root}/{file}', 'r') as f:
                    file_id += 1
                    rawdata = load(f)
                    self.data.append(rawdata["text"])
                    self.metadata.append({
                        "id": rawdata["uuid"],
                        "time": rawdata["published"],
                        "title": rawdata["title"],
                        "author": rawdata["author"],
                        "url": rawdata["url"]})
                    if file_id == maxfile:
                        logging.info(f'Maxfile reached, {file_id} file loaded')
                        return
        logging.info(f'All {file_id} file loaded')

    def dump(self, sentence):
        logging.info("Dumping input")
        self.data[0] = sentence

    def lemma_word(self, word_list):
        self.data[0] = word_list
        self._lemma_()

    def _pre_process_(self):
        logging.info('Pre-processing files')
        for file_id in range(len(self.data)):
            self.data[file_id] = self.data[file_id].lower()
            # match most of valid email addresses
            self.data[file_id] =sub('\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b','',self.data[file_id])
            # match url
            self.data[file_id] =sub(r'((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*','',self.data[file_id])
            # match time
            self.data[file_id] =sub('[0-9]{1,}:[0-9]{1,}(:[0-9]{2})?(am|pm)?','',self.data[file_id])
            # match punctuation
            self.data[file_id] =sub(r'[^\w\s]','',self.data[file_id])
            # remove digit
            self.data[file_id] =sub('[0-9]+', '',self.data[file_id])
            # remove \n when crawled
            self.data[file_id] =sub('\\n', '',self.data[file_id])
            # remove multiple space
            self.data[file_id] =sub(' {2,}', ' ',self.data[file_id])
            self.data[file_id] = self.data[file_id].strip()
            self.data[file_id] = self.data[file_id].split()

    def _lemma_(self):
        logging.info("Lemmatizing words")
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
        for file_id in range(len(self.data)):
            lemmatizer = WordNetLemmatizer()
            wordlist = []
            for word in self.data[file_id]:
                if word not in stopword:
                    wordlist.append(word)
            self.data[file_id] = [lemmatizer.lemmatize(word, get_wordnet_pos(word))
                for word in wordlist]
            if file_id % 200 == 0:
                logging.debug(f'{file_id} instance(s) lemmatized')
        logging.info(f'All {file_id+1} instance(s) lemmatized')

    def _gen_dict_(self):
        logging.info("Generating dictionary")
        if len(self.data) == 0:
            logging.error("data not loaded")
            return
        for file_id in range(len(self.data)):
            for word in self.data[file_id]:
                if word not in self.dict:
                    self.dict.append(word)
        
    def process(self):
        self._pre_process_()
        self._lemma_()
        self._gen_dict_()