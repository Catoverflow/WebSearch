from json import load
from os import walk
class Data(object):
    def __init__(self,path="./data"):
        self.path=path

    def _dump_(self):
        self.data = {}
        file_id = 0
        print('Loading all files, this may take a long time...')
        for (root, dirs, files) in walk(self.path):
            for file in files:
                with open(f'{root}/{file}','r') as f:
                    self.data[file_id] = load(f)
                    file_id+=1
                    if file_id % 1000 == 0:
                        print(f'{file_id} file loaded')
        print(f'{file_id} file loaded')

    def _strip_(self):
        print("Removing unneed infomation...")
        for file_id in self.data:
            self.data[file_id].pop("thread",None)
            self.data[file_id].pop("organizations",None)
            self.data[file_id].pop("ord_in_thread",None)
            self.data[file_id].pop("locations",None)
            self.data[file_id].pop("entities",None)
            self.data[file_id].pop("highlightText",None)
            self.data[file_id].pop("language",None)
            self.data[file_id].pop("persons",None)
            self.data[file_id].pop("external_links",None)
            self.data[file_id].pop("crawled",None)
            self.data[file_id].pop("highlightTitle",None)
            if file_id % 1000 == 0:
                print(f'{file_id} file stripped')
        print(f'{file_id} file stripped')

    def load(self):
        self._dump_()
        self._strip_()
