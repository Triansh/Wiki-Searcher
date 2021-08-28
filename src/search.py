import json
import time
import os, sys
import re
from Stemmer import Stemmer
from config import extra_stop_words


class QueryProcessor(object):

    def __init__(self, path_to_index):

        self.stemmer = Stemmer('english')
        self.stop_words = set(extra_stop_words)

        self.path_to_index = path_to_index
        self.file: int

        self.stem_words = set()
        self.words = {}
        self.mapper = {}
        self.result = {}
        self.for_json = {'t': 'title', 'b': 'body', 'i': 'infobox', 'c': 'categories',
                         'r': 'references', 'l': 'links'}

        self.tags = "tbircl"
        self.curr_query = {x: [] for x in self.tags}
        self.field_regex = re.compile(r"[tbircl]:")
        self.get_files()

    def get_files(self):
        self.file = open(self.path_to_index + '/index.txt', 'r')

    def load_file_data(self):
        data = {z[0]: z[1] for x in self.file.readlines()
                if (z := x.strip().split(':') or True) and z[0] in self.stem_words}
        data = {w: [(*x.split(',')[1:],) for x in s.split()] for w, s in data.items()}
        for w, v in data.items():
            self.words[w] = {x: [] for x in self.for_json.values()}
            for z in v:
                if len(z) == 1:
                    self.words[w][self.for_json['b']].append(int(z[0]))
                else:
                    for tag in z[1]:
                        self.words[w][self.for_json[tag]].append(int(z[0]))

    def extract_words(self, query_string):
        indices = [x.start() for x in self.field_regex.finditer(query_string.strip())]
        if len(indices) <= 0: return
        if indices[0] != 0: indices = [0] + indices

        parts = [query_string[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]

        for x in parts:
            if x[1] == ':':
                self.curr_query[x[0]] += [y.strip().lower() for y in x[2:].split() if y != '']
            else:
                self.curr_query['b'] += [y.strip().lower() for y in x.split() if y != '']

    def process_query(self, query_string):
        self.extract_words(query_string)
        self.finish_processing()
        self.load_file_data()
        self.getResults()

    def finish_processing(self):
        self.mapper = {w: self.stemmer.stemWord(w)
                       for x in self.curr_query.values() for w in x
                       if w not in self.stop_words}
        self.stem_words = set(self.mapper.values())

    def getResults(self):

        for words in self.curr_query.values():
            for w in words:
                if w in self.words:
                    self.result = self.words[w]
                else:
                    self.result = {x: [] for x in self.for_json.values()}

        with open('output.json', 'w') as f:
            f.write(json.dumps(self.result))


if __name__ == '__main__':
    start = time.time()
    path_to_index = sys.argv[1]
    query = ' '.join(sys.argv[2:])
    file_path = os.path.join(os.getcwd(), path_to_index)

    qp = QueryProcessor(file_path)
    qp.process_query(query)
    print("Time taken: ", time.time() - start)

    pass
