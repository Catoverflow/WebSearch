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


stopword = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


class Data(object):
    def __init__(self):
        self.data = []
        self.headerdata = []
        self.metadata = []
        self.dict = {}
        self.syn_table = {}

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

    @staticmethod
    def dump(sentence):
        logging.info("Dumping input")
        return Data.lemma(Data.strip_stop_words(Data.pre_process(sentence)))

    @staticmethod
    def pre_process(sentence):
        sentence = sentence.lower()
        # match most of valid email addresses
        sentence = sub(
            '\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b', '', sentence)
        # match url
        sentence = sub(
            r'((http|https)\:\/\/)?[a-z0-9\.\/\?\:@\-_=#]+\.([a-z]){2,6}([a-z0-9\.\&\/\?\:@\-_=#])*', '', sentence)
        # match time
        sentence = sub('[0-9]{1,}:[0-9]{1,}(:[0-9]{2})?(am|pm)?', '', sentence)
        # split connected words
        sentence = sub('\-', ' ', sentence)
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

    @staticmethod
    def strip_stop_words(wordbag):
        wordlist = []
        for word in wordbag:
            if word not in stopword:
                wordlist.append(word)
        return wordlist

    # the slowest proceed
    @staticmethod
    def lemma(wordbag):
        # this method owe to https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
        return [lemmatizer.lemmatize(
            word, Data.get_wordnet_pos(word)) for word in wordbag]

    def gen_dict(self):
        wid = 0
        for docid in range(len(self.data)):
            wordlist = []
            for word in self.data[docid]:
                if word not in self.dict.keys():
                    # has synonym
                    if word in self.syn_table.keys() and self.syn_table[word] in self.dict.keys():
                        # point to same id of synonym
                        self.dict[word] = self.dict[self.syn_table[word]]
                    else:
                        # add new key
                        self.dict[word] = wid
                        wid += 1
                wordlist.append(self.dict[word])
            self.data[docid] = wordlist
        for docid in range(len(self.headerdata)):
            wordlist = []
            for word in self.headerdata[docid]:
                if word not in self.dict.keys():
                    if word in self.syn_table.keys() and self.syn_table[word] in self.dict.keys():
                        self.dict[word] = self.dict[self.syn_table[word]]
                    else:
                        self.dict[word] = wid
                        wid += 1
                wordlist.append(self.dict[word])
            self.headerdata[docid] = wordlist

    # Synonyms table from github.com/SuzanaK/english_synonyms_antonyms_list
    def parse_syn(self):
        with open('dataset/english_synonyms_and_antonyms.csv', 'r') as f:
            for line in f:
                word = line.split('\t')[0]
                synonym = line.split('\t')[1].split(', ')[0]
                self.syn_table[word] = synonym

    def process(self):
        logging.info("Lemmatizing words")
        for docid in range(len(self.data)):
            if docid % 1000 == 0:
                logging.debug(f"{docid} document processed")
            self.data[docid] = self.lemma(
                self.strip_stop_words(
                    self.pre_process(self.data[docid])))
            self.headerdata[docid] = self.lemma(
                self.strip_stop_words(
                    self.pre_process(self.headerdata[docid])))
        self.parse_syn()
        self.gen_dict()
