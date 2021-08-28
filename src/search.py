import os, sys
import re
from Stemmer import Stemmer
from config import extra_stop_words


class QueryProcessor(object):

    def __init__(self, path_to_index):

        self.stemmer = Stemmer('english')
        self.stop_words = set(extra_stop_words)
        self.path_to_index = path_to_index
        self.files = []
        self.word_token_map = {}
        self.query_string = []
        self.tags = "tbircl"
        self.field_regex = re.compile(r"[tbircl]:")
        self.mapper = {}

    def get_files(self):
        self.files = [open(self.path_to_index + '/index.txt')]

    def process_query(self, query):
        query = query.strip()
        indices = [x.start() for x in self.field_regex.finditer(query)]
        if len(indices) <= 0: return
        if indices[0] != 0: indices = [0] + indices
        parts = [query[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]
        dic = {x: [] for x in self.tags}
        for x in parts:
            if x[1] == ':':
                dic[x[0]] += [y.strip() for y in x[2:].split() if y != '']
            else:
                dic['b'] += [y.strip() for y in x.split() if y != '']
        self.query_string.append(dic)

    def finish(self):
        print(self.query_string)
        self.mapper = {w: self.stemmer.stemWord(w)
                       for x in self.query_string for y in x.values() for z in y
                       if (w := z.lower()) not in self.stop_words}
        print(self.mapper)

    def add_query(self, query):
        queries = self.process_query(query)
        # for sent in queries:
        #     tag = sent[0] if sent[1] == ':' else 'b'
        #     for word in (sent if tag == 'b' else sent[2:]).split():
        #         if word in self.word_token_map:
        #             self.word_token_map[word] += tag
        #         else:
        #             self.word_token_map[word] = tag


if __name__ == '__main__':
    path_to_index = sys.argv[1]
    path_to_query = sys.argv[2]
    file_path = os.path.join(os.getcwd(), path_to_index)
    query_path = os.path.join(os.getcwd(), path_to_query)

    print(path_to_query, path_to_index)

    qp = QueryProcessor(file_path)
    with open(query_path) as f:
        z = list(map(qp.add_query, f.readlines()))
        print(z)
    qp.finish()

    pass
