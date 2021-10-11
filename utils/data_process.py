from json import load
from os import popen, walk
class Data(object):
    def __init__(self,path="./data",maxfile=-1):
        self.path=path
        self.whitelist = {
            "uuid",
            "author",
            "url",
            "title",
            "text",
            "published"
        }
        self.poplist = set({})
        self.maxfile = maxfile
        self.data = {}

    def _dump_(self):
        file_id = 0
        print('Loading all files, this may take a long time...')
        for (root, dirs, files) in walk(self.path):
            for file in files:
                with open(f'{root}/{file}','r') as f:
                    file_id+=1
                    self.data[file_id] = load(f)
                    if file_id % 1000 == 0:
                        print(f'{file_id} file loaded')
                    if file_id == self.maxfile:
                        print(f'{file_id} file loaded')
                        return
        print(f'{file_id} file loaded')

    def _strip_(self):
        print("Removing unneed infomation...")
        for file_id in self.data:
            for key in self.data[file_id].keys():
                if key not in self.poplist and key not in self.whitelist:
                    self.poplist.add(key)
            for key in self.poplist:
                self.data[file_id].pop(key, None)
            if file_id % 1000 == 0:
                print(f'{file_id} file stripped')
        print(f'{file_id} file stripped')

    def load(self):
        self._dump_()
        self._strip_()