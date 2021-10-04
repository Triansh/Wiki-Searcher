import os
import pickle
import re
import sys
import time
from Stemmer import Stemmer

from Ranker import Ranker


class QueryProcessor(Ranker):

    def __init__(self, path_to_index_dir):

        super().__init__()
        self.stemmer = Stemmer('english')
        with open(os.path.join(os.getcwd(), 'src/stopwords.pkl'), 'rb') as f:
            self.stop_words = set(pickle.load(f))

        self.path_to_index = os.path.join(os.getcwd(), path_to_index_dir)
        with open(os.path.join(self.path_to_index, 'heads.txt'), 'r') as f:
            self.index_heads = [x.rstrip() for x in f.readlines()]

        self.curr_query = {}
        self.query_string = ''
        self.results = []
        self.final_result = ''

        for i in range(
                sum((1 if x.startswith('freq_') else 0) for x in os.listdir(self.path_to_index))):
            with open(os.path.join(self.path_to_index, f'freq_{i}.txt'), 'r') as f:
                self.doc_size += [int(z) for x in f if (z := x.rstrip()) != '']

        self.field_regex = re.compile(r"[tbircl]:")

    def reset(self):
        super().reset()
        self.curr_query = {}
        self.results = []

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
            parts = [self.query_string[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]
        else:
            parts = [self.query_string.strip()]
        for q in parts:
            tag, x = (q[0], q[2:]) if len(q) > 2 and q[1] == ':' else ('e', q)
            for y in x.split():
                if y == '' or y in self.stop_words: continue
                y = self.stemmer.stemWord(y)
                if y in self.curr_query:
                    self.curr_query[y] += tag
                else:
                    self.curr_query[y] = tag
        self.curr_query = {k: ('' if (z := ''.join(set(v))) == 'e' else z.replace('e', '')) for k, v
                           in self.curr_query.items()}

    # This get all the required data from the index files
    # word count contains in how many documents the word came. Form :- {word : count}
    # word doc map contains the list of doc_id and frequency of the word in that document.
    # Form :- {word : [(frequency, doc_id)]}
    def get_index_data(self):
        word_file_map = {}
        for tok in self.curr_query.keys():
            file_no = self.search_file(tok)
            if file_no in word_file_map:
                word_file_map[file_no].add(tok)
            else:
                word_file_map[file_no] = {tok}

        for file_no, words in word_file_map.items():
            max_word = max(words)
            with open(os.path.join(self.path_to_index, f'index_{file_no}.txt'), 'r') as f:
                for line in f:
                    ind = line.find(':')
                    if ind == -1:
                        continue
                    elif (w := line[:ind]) > max_word:
                        break
                    elif w in words:
                        posting = [(*(x.split(',') + ['b'])[:3],) for x in line[(ind + 1):].split()]
                        posting = [(int(x[0]), int(x[1])) for x in posting if
                                   self.doc_size[int(x[1])] > 400 and
                                   all(z in x[2] for z in self.curr_query[w])]
                        self.doc_counter.update(x[1] for x in posting)
                        self.word_count.update({w: len(posting)})
                        self.all_word_posting.update({w: posting})

        # print("Time taken for getting index data: ", time.time() - st)

    def process_query(self, query_string):
        self.query_string = query_string
        self.reset()
        self.extract_words()
        if len(self.curr_query) == 0:
            print('Results:\nNo relevant documents found')
            return
        self.get_index_data()
        if len(self.word_count) == 0:
            print('Results:\nNo relevant documents found')
            return
        self.calculate_scores()
        self.get_results()

    def get_results(self):
        file_map, title_map = {}, {}
        for x in self.results:
            q, r = x // self.max_file_lines, x % self.max_file_lines
            if q in file_map:
                file_map[q].add(r)
            else:
                file_map[q] = {r}

        for f_no, lines in file_map.items():
            lines, curr = sorted(lines) + [-1], 0
            with open(os.path.join(self.path_to_index, f'title_{f_no}.txt'), 'r') as fp:
                for i, line in enumerate(fp):
                    if lines[curr] == -1:
                        break
                    elif i == lines[curr]:
                        title_map[self.max_file_lines * f_no + i] = line.rstrip()
                        curr += 1

        self.final_result += '\n'.join(f"{x},  {title_map[x]}" for x in self.results)


if __name__ == '__main__':
    path_to_index = sys.argv[1]
    path_to_query = sys.argv[2]
    qp = QueryProcessor(path_to_index)
    tt = time.time()
    with open(os.path.join(os.getcwd(), path_to_query), 'r') as f:
        for line in f:
            start = time.time()
            qry = line.lower().replace(',', ' ').strip()
            qp.process_query(qry)
            qp.final_result += f"\nTime taken: {time.time() - start}\n\n"

    print("Total time taken: ", time.time() - tt)
    with open(os.path.join(os.getcwd(), 'queries_op.txt'), 'w') as f:
        f.write(qp.final_result)
