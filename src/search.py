import os
import pickle
import re
import sys
import time
from Stemmer import Stemmer

from Ranker import Ranker


class QueryProcessor(Ranker):

    def __init__(self, path_to_index_dir, query_string):

        super().__init__()
        self.stemmer = Stemmer('english')
        with open(os.path.join(os.getcwd(), 'src/stopwords.pkl'), 'rb') as f:
            self.stop_words = set(pickle.load(f))

        self.query_string = query_string.strip()

        self.path_to_index = os.path.join(os.getcwd(), path_to_index_dir)
        with open(os.path.join(self.path_to_index, 'heads.txt'), 'r') as f:
            self.index_heads = [x.rstrip() for x in f.readlines()]

        self.max_file_lines = 10 ** 4

        self.curr_query = {}

        self.field_regex = re.compile(r"[tbircl]:")

    # Binary search on index heads to to get the file no.
    def search_file(self, word):
        s, e, ans = 0, len(self.index_heads) - 1, 0
        while s <= e:
            mid = (s + e) // 2
            if self.index_heads[mid] > word:
                e = mid - 1
            else:
                s = mid + 1
                ans = mid
        return ans

    # Parsing the query into broken words if the tags they require
    # self.curr_query is of the form {word : tags}
    def extract_words(self):
        indices = [x.start() for x in self.field_regex.finditer(self.query_string)]
        if len(indices) > 0:
            if indices[0] != 0: indices = [0] + indices
            parts = [self.query_string[i:j].strip() for i, j in zip(indices, indices[1:] + [0])]
        else:
            parts = [self.query_string.strip()]
        # print(parts)
        for q in parts:
            tag, x = (q[0], q[2:]) if q[1] == ':' else ('bcilrt', q)
            # print(tag, x)
            for y in x.split():
                if y == '' or y in self.stop_words: continue
                y = self.stemmer.stemWord(y)
                if y in self.curr_query:
                    self.curr_query[y] += tag
                else:
                    self.curr_query[y] = tag
        self.curr_query = {k: ''.join(set(v)) for k, v in self.curr_query.items()}
        # print(self.curr_query)

    # This get all the required data from the index files
    # word count contains in how many documents the word came. Form :- {word : count}
    # word doc map contains the list of doc_id and frequency of the word in that document.
    # Form :- {word : [(frequency, doc_id)]}
    def get_index_data(self):
        word_file_map = {}
        for tok, tags in self.curr_query.items():
            file_no = self.search_file(tok)
            if file_no in word_file_map:
                word_file_map[file_no].add(tok)
            else:
                word_file_map[file_no] = {tok}

        for file_no, words in word_file_map.items():
            with open(os.path.join(self.path_to_index, f'index_{file_no}.txt'), 'r') as f:
                word_docs = {z[0]: [tuple(x.split(',') + ['b'])
                                    for x in z[1].split()] for x in f.readlines()
                             if (z := x.split(':') or True) and z[0] in words}
                word_docs = {k: [(int(x[0]), int(x[1])) for x in v
                                 if any(z in (x[2] or 'b') for z in self.curr_query[k])] for k, v in
                             word_docs.items()}
                self.word_count.update({k: len(v) for k, v in word_docs.items()})
                self.word_to_doc_map.update(word_docs)

    # This gets the field length of all the required documents contained in doc_size
    # Form :- {doc_id : doc_size}
    def get_doc_len_data(self):
        doc_ids = set(y[1] for doc in self.word_to_doc_map.values() for y in doc)
        print(sorted(doc_ids))
        self.final_score = {x: 0 for x in doc_ids}
        doc_file_map = {}
        for x in doc_ids:
            q, r = (x - 1) // self.max_file_lines, (x - 1) % self.max_file_lines
            if q in doc_file_map:
                doc_file_map[q].add(r)
            else:
                doc_file_map[q] = {r}

        print(doc_file_map)

        for file_no, lines in doc_file_map.items():
            with open(os.path.join(self.path_to_index, f'freq_{file_no}.txt')) as f:
                file = f.readlines()
                self.doc_size.update({(self.max_file_lines * file_no + 1 + line): int(file[line])
                                      for line in lines})
        print(self.doc_size)

    def process_query(self):
        self.extract_words()
        self.get_index_data()
        self.get_doc_len_data()
        self.calculate_scores()
        self.get_results()
        print(self.final_score)
        # self.getResults()

    def get_results(self):
        file_map, title_map = {}, {}
        for x in self.results:
            q, r = (x - 1) // self.max_file_lines, (x - 1) % self.max_file_lines
            if q in file_map:
                file_map[q].add(r)
            else:
                file_map[q] = {r}

        for f_no, lines in file_map.items():
            with open(os.path.join(self.path_to_index, f'title_{f_no}.txt')) as f:
                file = f.readlines()
                title_map.update(
                    {(self.max_file_lines * f_no + 1 + li): file[li].rstrip() for li in lines})

        self.results = [(x, title_map[x]) for x in self.results]
        print('\n'.join(str(x[0]) + ', ' + x[1] for x in self.results))


if __name__ == '__main__':
    start = time.time()
    path_to_index = sys.argv[1]
    query = sys.argv[2].lower().replace(',', ' ')
    qp = QueryProcessor(path_to_index, query)
    qp.process_query()
    print("Time taken: ", time.time() - start)

    pass
