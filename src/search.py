import os
import pickle
import re
import sys
import time
from linecache import getline, clearcache
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
        st = time.time()

        indices = [x.start() for x in self.field_regex.finditer(self.query_string)]
        if len(indices) > 0:
            if indices[0] != 0: indices = [0] + indices
            parts = [self.query_string[i:j].strip() for i, j in zip(indices, indices[1:] + [None])]
        else:
            parts = [self.query_string.strip()]
        for q in parts:
            tag, x = (q[0], q[2:]) if len(q) > 2 and q[1] == ':' else ('e', q)
            # print(tag, x)
            for y in x.split():
                if y == '' or y in self.stop_words: continue
                y = self.stemmer.stemWord(y)
                if y in self.curr_query:
                    self.curr_query[y] += tag
                else:
                    self.curr_query[y] = tag
        self.curr_query = {k: ('' if (z := ''.join(set(v))) == 'e' else z.replace('e', '')) for k, v
                           in self.curr_query.items()}
        print("Time taken for word extraction: ", time.time() - st)
        # print(self.curr_query, '\n\n')

    # This get all the required data from the index files
    # word count contains in how many documents the word came. Form :- {word : count}
    # word doc map contains the list of doc_id and frequency of the word in that document.
    # Form :- {word : [(frequency, doc_id)]}
    def get_index_data(self):
        st = time.time()
        word_file_map = {}
        for tok in self.curr_query.keys():
            file_no = self.search_file(tok)
            if file_no in word_file_map:
                word_file_map[file_no].add(tok)
            else:
                word_file_map[file_no] = {tok}
        print(word_file_map)
        print("Time taken for getting search data: ", time.time() - st)

        st = time.time()

        for file_no, words in word_file_map.items():
            with open(os.path.join(self.path_to_index, f'index_{file_no}.txt'), 'r') as f:
                max_word = max(words)
                for line in f:
                    ind = line.find(':')
                    if ind == -1: continue
                    if (w := line[:ind]) > max_word: break
                    if w in words:
                        posting = [(*(x.split(',') + ['b'])[:3],) for x in line[(ind + 1):].split()]
                        self.word_count.update({w: len(posting)})
                        # print(w, len(posting), ":\n", posting, '\n\n', )
                        posting = [(int(x[0]), int(x[1])) for x in posting if
                                   all(z in x[2] for z in self.curr_query[w])]
                        # posting.sort(reverse=True)
                        # posting = posting[:10000]
                        self.word_to_doc_map.update({w: posting})
                        # print(w, len(posting), ":\n", posting, '\n\n')

                        # word_docs = {x[:ind]: [(*(x.split(',') + ['b']),)
                #                        for x in x[(ind + 1):].split()] for x in f.readlines()
                #              if ((ind := x.find(':')) != -1) and x[:ind] in words}
                # word_docs = {k: [(int(x[0]), int(x[1])) for x in v
                #                  if any(z in (x[2] or 'b') for z in self.curr_query[k])] for k, v in
                #              word_docs.items()}
                # self.word_count.update({k: len(v) for k, v in word_docs.items()})
                # self.word_to_doc_map.update(word_docs)
        # print(self.word_to_doc_map)
        print(self.word_count)
        print("Time taken for getting index data: ", time.time() - st)

    # This gets the field length of all the required documents contained in doc_size
    # Form :- {doc_id : doc_size}
    def get_doc_len_data(self):
        st = time.time()
        doc_ids = set(y[1] for doc in self.word_to_doc_map.values() for y in doc)
        max_id = max(doc_ids)
        print("Total docs found: ", len(doc_ids), " Max doc id: ", max_id)
        self.final_score = {x: 0 for x in doc_ids}
        doc_file_map = {}
        for x in doc_ids:
            q, r = x // self.max_file_lines, x % self.max_file_lines
            if q in doc_file_map:
                doc_file_map[q].add(r)
            else:
                doc_file_map[q] = {r}

        print("Total files need to be opened for getting doc len: ", len(doc_file_map.keys()))

        for file_no, lines in doc_file_map.items():
            with open(os.path.join(self.path_to_index, f'freq_{file_no}.txt')) as f:
                file = f.readlines()
                self.doc_size.update({(self.max_file_lines * file_no + line): int(file[line])
                                      for line in lines})

        # self.doc_size.update({(self.max_file_lines * file_no + 1 + line): int(
        #     getline(os.path.join(self.path_to_index, f'freq_{file_no}.txt'), line + 1).rstrip()) for
        #                       file_no, lines in doc_file_map.items() for line in sorted(lines)})
        # f_name = os.path.join(self.path_to_index, 'freqs.txt')
        # self.doc_size = {x: int(getline(f_name, x - 1).rstrip()) for x in doc_ids}
        # with open(os.path.join(self.path_to_index, f'freqs.txt'), 'r') as fp:
        #     for i, line in enumerate(fp):
        #         if (i + 1) in doc_ids:
        #             self.doc_size[i + 1] = int(line.rstrip())
        #         elif i + 1 > max_id:
        #             break
        # pprint(self.doc_size)
        print("Time taken for getting doc len data: ", time.time() - st)

    def process_query(self, query_string):
        self.query_string = query_string
        self.extract_words()
        if len(self.curr_query) == 0:
            print('Results:\nNo documents found')
            return
        self.get_index_data()
        if len(self.word_count) == 0:
            print('Results:\nNo documents found')
            return
        self.get_doc_len_data()
        self.calculate_scores()
        # print("\nFinal scores: ")
        # pprint(sorted(self.final_score.items(), key=lambda x: -x[1]))
        self.get_results()
        # self.getResults()

    def get_results(self):
        st = time.time()
        file_map, title_map = {}, {}
        for x in self.results:
            q, r = x // self.max_file_lines, x % self.max_file_lines
            if q in file_map:
                file_map[q].add(r)
            else:
                file_map[q] = {r}

        # for file_no, lines in file_map.items():
        #     with open(os.path.join(self.path_to_index, f'title_{file_no}.txt')) as f:
        #         file = f.readlines()
        #         title_map.update({(self.max_file_lines * file_no + line): (file[line])
        #                           for line in lines})

        for f_no, lines in file_map.items():
            f_name = os.path.join(self.path_to_index, f'title_{f_no}.txt')
            title_map.update(
                {(self.max_file_lines * f_no + li): getline(f_name, li + 1).rstrip() for li in
                 lines})

        self.results = [(x, title_map[x]) for x in self.results]
        print("Time taken for getting title data: ", time.time() - st)

        print("\nResults: ")
        print(
            '\n'.join(str(x[0]) + ',\t\t' + x[1] + '\t\t' + str(self.final_score[x[0]]) for x in
                      self.results))


if __name__ == '__main__':
    tt = time.time()
    path_to_index = sys.argv[1]
    path_to_query = sys.argv[2]
    qp = QueryProcessor(path_to_index)
    with open(os.path.join(os.getcwd(), path_to_query), 'r') as f:
        for line in f:
            start = time.time()
            qry = line.lower().replace(',', ' ').strip()
            qp.process_query(qry)
            print("Time taken: ", time.time() - start)
            print()

    print("Total time taken: ", time.time())
