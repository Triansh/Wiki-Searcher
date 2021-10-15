import os
import time
from heapq import heappush, heappop, heapify

from config import MAX_TOKEN_FILE_SIZE, MAX_TITLES, MAX_INDEX_FILE_SIZE


def format_tuple(doc_id, count, tags):
    if tags == 'b':
        return ','.join((str(count), str(doc_id)))
    else:
        return ','.join((str(count), str(doc_id), tags))


class InvertedIndex(object):

    def __init__(self, path_to_index):
        self.path_to_index = os.path.join(os.getcwd(), path_to_index)
        self.token_file_count = 0
        self.title_file_count = 0
        self.index_file_count = 0

        self.files = []
        self.file_opened = []

        self.token_map = {}
        self.token_size = 0
        self.posting = {}
        self.posting_size = 0

        self.titles = ""
        self.doc_freq = ""
        self.index_heads = ""
        self.title_count = 0
        self.total_unique_tokens = 0

    def get_title_filename(self, file_num):
        return os.path.join(self.path_to_index, f'title_{file_num}.txt')

    def get_token_filename(self, file_num):
        return os.path.join(self.path_to_index, f'__token_{file_num}.txt')

    def get_index_filename(self, file_num):
        return os.path.join(self.path_to_index, f'index_{file_num}.txt')

    def get_doc_freq_filename(self, file_num):
        return os.path.join(self.path_to_index, f'freq_{file_num}.txt')

    def get_word(self, file_num):
        if not self.file_opened[file_num]:
            return ''
        z = self.files[file_num].readline().rstrip()
        if z == '':
            self.file_opened[file_num] = 0
            return ''
        w, p = z.split(':')
        if w in self.token_map:
            self.token_map[w] += ' ' + p
        else:
            self.token_map[w] = p
        return w

    def merge_files(self):
        end = time.time()
        self.files = [open(os.path.join(self.path_to_index, filename), 'r')
                      for filename in os.listdir(self.path_to_index) if
                      filename.startswith('__')]
        self.file_opened = [1] * len(self.files)
        heap = [(z, x) for x in range(len(self.files)) if (z := self.get_word(x)) != '']
        heapify(heap)

        while len(heap):
            x, file_no = heappop(heap)
            self.posting[x] = self.token_map.pop(x, '')
            self.posting_size += len(x) + len(self.posting[x]) + 1
            self.total_unique_tokens += 1

            while len(heap) and heap[0][0] == x:
                y, f = heappop(heap)
                if (w := self.get_word(f)) != '':
                    heappush(heap, (w, f))

            if (w := self.get_word(file_no)) != '':
                heappush(heap, (w, file_no))

            if self.posting_size >= MAX_INDEX_FILE_SIZE:
                self.write_indexes()
                self.posting_size = 0
        self.write_indexes()

        print("Time for merging: ", time.time() - end)

    def post_cleanup(self):
        with open(os.path.join(self.path_to_index, 'heads.txt'), 'w') as f:
            f.write(self.index_heads)

        with open(os.path.join(self.path_to_index, 'freqs.txt'), 'w') as f:
            f.write(self.doc_freq.rstrip())

        for filename in os.listdir(self.path_to_index):
            if filename.startswith('__'):
                os.remove(os.path.join(self.path_to_index, filename))

    def write_tokens(self):
        if len(self.token_map) == 0:
            return
        formatted_string = '\n'.join(
            tok + ':' + self.token_map[tok] for tok in sorted(self.token_map.keys()))
        with open(self.get_token_filename(self.token_file_count), 'w') as f:
            f.write(formatted_string)
        self.token_file_count += 1
        self.token_map = {}
        self.token_size = 0

    def write_titles(self):
        if len(self.titles) == 0:
            return
        with open(self.get_title_filename(self.title_file_count), 'w') as f:
            f.write(self.titles)
        self.title_file_count += 1
        self.title_count = 0
        self.titles = ""

    def write_indexes(self):
        if len(self.posting) == 0:
            return
        sorted_keys = sorted(self.posting.keys())
        self.index_heads += sorted_keys[0] + '\n'
        formatted_string = '\n'.join(x + ':' + self.posting[x] for x in sorted_keys)
        with open(self.get_index_filename(self.index_file_count), 'w') as f:
            f.write(formatted_string)
        self.index_file_count += 1
        self.posting = {}

    def finish(self):
        self.write_tokens()
        self.write_titles()
        self.merge_files()
        self.post_cleanup()

    def add_titles(self, title, doc_freq):
        self.titles += title + '\n'
        self.doc_freq += str(doc_freq) + '\n'
        self.title_count += 1
        if self.title_count >= MAX_TITLES:
            self.write_titles()

    def merge_tokens(self, doc_id, doc_map, title):
        self.add_titles(title.strip(), sum(ct for tok, (ct, tags) in doc_map.items()))
        for tok, val in doc_map.items():
            if tok in self.token_map:
                z = ' ' + format_tuple(doc_id, val[0], ''.join(set(val[1])))
                self.token_map[tok] += z
                self.token_size += len(z)
            else:
                self.token_map[tok] = format_tuple(doc_id, val[0], ''.join(set(val[1])))
                self.token_size += len(self.token_map[tok]) + len(tok) + 1
        if self.token_size >= MAX_TOKEN_FILE_SIZE:
            self.write_tokens()
