import json
import time
import os, sys
import re
from Stemmer import Stemmer
import pickle


class QueryProcessor(object):

    def __init__(self, path_to_index):

        self.stemmer = Stemmer('english')
        with open(os.path.join(os.getcwd(), 'src/stopwords.pkl'), 'rb') as f:
            self.stop_words = set(pickle.load(f))

        self.path_to_index = os.path.join(os.getcwd(), path_to_index)
        self.index_files, self.title_files, self.index_heads = [], [], []
        self.get_all_files()

        self.stem_words = set()
        self.mapper = {}
        self.curr_query = {}

        self.tags = set(list("tbircle"))
        self.field_regex = re.compile(r"[tbircl]:")

    def get_all_files(self):
        self.index_files = [open(os.path.join(self.path_to_index, filename), 'r')
                            for filename in os.listdir(self.path_to_index)
                            if filename.startswith('index_')]
        self.title_files = [open(os.path.join(self.path_to_index, filename), 'r')
                            for filename in os.listdir(self.path_to_index)
                            if filename.startswith('title_')]
        with open('heads.txt', 'r') as f:
            self.index_heads = [x.strip() for x in f.readlines()]

    def search_file(self, word):
        s, e, ans = 0, len(self.index_files), 0
        while s <= e:
            mid = (s + e) // 2
            if self.index_heads[mid] > word:
                e = mid - 1
            else:
                s = mid + 1
                ans = mid
        return ans

    def extract_words(self, query_string):
        indices = [x.start() for x in self.field_regex.finditer(query_string.strip())]
        if len(indices) > 0:
            if indices[0] != 0: indices = [0] + indices
            parts = [query_string[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]
        else:
            parts = [query_string]

        for x in parts:
            tag = 'e'
            if x[1] == ':':
                tag, x = x[0], x[2:]
            for y in x[2:].split():
                if y == '' or y in self.stop_words: continue
                if y in self.curr_query:
                    self.curr_query[y] += tag
                else:
                    self.curr_query[y] = tag
                    self.mapper[y] = self.stemmer.stemWord(y)
        self.curr_query = {k: ''.join(set(list(v))) for k, v in self.curr_query.items()}
        self.stem_words = set(self.mapper.values())

    def process_query(self, query_string):
        self.extract_words(query_string)
        # self.load_file_data()
        # self.getResults()

    def getResults(self):
        pass
        # with open('output.json', 'w') as f:
        # print(json.dumps(self.result, indent=4))


if __name__ == '__main__':
    start = time.time()
    path_to_index = sys.argv[1]
    query = sys.argv[2].lower().replace(',', ' ')
    qp = QueryProcessor(path_to_index)
    qp.process_query(query)
    print("Time taken: ", time.time() - start)

    pass
