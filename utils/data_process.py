# auto load raw files and generate corresponding lemmatized data
# usage: Data.load() load first, get raw files and lemmatizing them
#                    duplicate loading is auto-prevented
#        file_id: unique id for each file, ascending from 1
#        Data.data() get lemmatized data list
#                    data format: data = [[file1 word lis],[file2 word list],...]
#        Data.metadata() get metadata of file
#                    data format: metadata = [{file1 metadata dict},{file2 metadatadoct},...]
#        Data.dict() get word bag of all files
#                    data format: dict = [word1, word2, ...]
#                    use list instead of set is to keep words in order
from json import load
from os import walk
from re import sub
import logging
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk import pos_tag


class Data(object):
    def __init__(self):
        self.data = []
        self.headerdata = []
        self.metadata = []
        self.dict = []
        self.stopword = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(word):
        tag = pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

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
                    self.headerdata.append(rawdata['title'])
                    self.metadata.append({
                        "id": rawdata["uuid"],
                        # "time": rawdata["published"],
                        "title": rawdata["title"]
                        # "author": rawdata["author"],
                        # "url": rawdata["url"]
                    })
                    if file_id == maxfile:
                        logging.info(f'Maxfile reached, {file_id} file loaded')
                        return
        logging.info(f'All {file_id} file loaded')

    def dump(self, sentence):
        logging.info("Dumping input")
        self.data.append(sentence)

    def lemma_word(self, word_list):
        self.data.append(word_list)
        self._lemma_()

    def _pre_process_(self, sentence):
        logging.info('Pre-processing files')
        sentence = sentence.lower()
        # match most of valid email addresses
        sentence = sub(
            '\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b', '', sentence)
        # match url
        sentence = sub(
            r'((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*', '', sentence)
        # match time
        sentence = sub('[0-9]{1,}:[0-9]{1,}(:[0-9]{2})?(am|pm)?', '', sentence)
        # match punctuation
        sentence = sub(r'[^\w\s]', '', sentence)
        # remove digit
        sentence = sub('[0-9]+', '', sentence)
        # remove \n when crawled
        sentence = sub('\\n', '', sentence)
        # remove multiple space
        sentence = sub(' {2,}', ' ', sentence)
        sentence = sentence.strip()
        sentence = sentence.split()
        return sentence

    def _strip_stop_words_(self, wordbag):
        logging.info("Stripping stop words")
        wordlist = []
        for word in wordbag:
            if word not in self.stopword:
                wordlist.append(word)
        return wordlist

    # the slowest proceed
    def _lemma_(self, wordbag):
        logging.info("Lemmatizing words")
        # this method owe to https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
        return [self.lemmatizer.lemmatize(
            word, Data.get_wordnet_pos(word)) for word in wordbag]

    def _gen_dict_(self):
        lookup_table = {}
        dict_size = 0
        logging.info("Generating dictionary")
        if len(self.data) == 0:
            logging.error("data not loaded")
            return
        for file_id in range(len(self.data)):
            word_id_list = []
            for word in self.data[file_id]:
                if word not in self.dict:
                    self.dict.append(word)
                    lookup_table[word] = dict_size
                    dict_size += 1
                word_id_list.append(lookup_table[word])
            self.data[file_id] = word_id_list 
        for file_id in range(len(self.headerdata)):
            word_id_list = []
            for word in self.headerdata[file_id]:
                if word not in self.dict:
                    self.dict.append(word)
                    lookup_table[word] = dict_size
                    dict_size += 1
                word_id_list.append(lookup_table[word])
            self.headerdata[file_id] = word_id_list

    def process(self):
        for docid in range(len(self.data)):
            self.data[docid] = self._lemma_(
                self._strip_stop_words_(
                    self._pre_process_(self.data[docid])))
            self.headerdata[docid] = self._lemma_(
                self._strip_stop_words_(
                    self._pre_process_(self.headerdata[docid])))
        self._gen_dict_()
