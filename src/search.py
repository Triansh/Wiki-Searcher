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

        self.path_to_index = path_to_index
        self.file: int

        self.stem_words = set()
        self.words = {}  # {word : {title : [ids], body: [ids] } }
        self.mapper = {}
        self.result = {}
        self.for_json = {'t': 'title', 'b': 'body', 'i': 'infobox', 'c': 'categories',
                         'r': 'references', 'l': 'links'}

        self.tags = set(list("tbircl"))
        self.curr_query = {x: [] for x in self.tags}
        self.field_regex = re.compile(r"[tbircl]:")
        self.file = open(self.path_to_index + '/index_1.txt', 'r')

    def load_file_data(self):
        # { word as key and rest compressed string as value}
        data = {z[0]: z[1] for x in self.file.readlines()
                if (z := x.strip().split(':') or True) and z[0] in self.stem_words}
        # {word as key and value of the form [(id,), (id, tbir), ()]
        data = {w: [(*x.split(',')[1:],) for x in s.split()] for w, s in data.items()}
        # print([x for x in data.keys()])
        for w, v in data.items():
            self.words[w] = {x: [] for x in self.for_json.values()}
            for z in v:
                if len(z) == 1:
                    self.words[w][self.for_json['b']].append(int(z[0]))
                else:
                    for tag in z[1]:
                        self.words[w][self.for_json[tag]].append(int(z[0]))
        # print(self.words)
        # print([x for x in self.words.keys()])

    def extract_words(self, query_string):
        indices = [x.start() for x in self.field_regex.finditer(query_string.strip())]
        if len(indices) > 0:
            if indices[0] != 0: indices = [0] + indices
            parts = [query_string[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]
            # print(parts)
        else:
            parts = [query_string]
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
        # print(self.words, self.curr_query)
        for words in self.curr_query.values():
            for w in words:
                if w in self.mapper:
                    self.result[w] = self.words[self.mapper[w]]
                else:
                    self.result[w] = {x: [] for x in self.for_json.values()}

        # with open('output.json', 'w') as f:
        print(json.dumps(self.result, indent=4, sort_keys=True))


if __name__ == '__main__':
    start = time.time()
    path_to_index = sys.argv[1]
    # query = ' '.join(sys.argv[2:])
    query = sys.argv[2].lower()
    # print(query)
    file_path = os.path.join(os.getcwd(), path_to_index)

    qp = QueryProcessor(file_path)
    qp.process_query(query)
    # print("Time taken: ", time.time() - start)

    pass
