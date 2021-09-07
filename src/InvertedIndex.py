import heapq
import os
import time

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
        self.files_remaining = set()
        self.files_to_remove = set()

        self.token_map = {}
        self.token_size = 0
        self.posting = {}
        self.titles = []
        self.total_unique_tokens = 0
        self.index_heads = []

    def get_title_filename(self, file_num):
        return os.path.join(self.path_to_index, f'title_{file_num}.txt')

    def get_token_filename(self, file_num):
        return os.path.join(self.path_to_index, f'__token_{file_num}.txt')

    def get_index_filename(self, file_num):
        return os.path.join(self.path_to_index, f'index_{file_num}.txt')

    def getLine(self, file_num):
        if not self.file_opened[file_num]:
            return ''
        z = self.files[file_num].readline().strip()
        if z == '':
            self.file_opened[file_num] = 0
            self.files_to_remove.add(file_num)
            return ''
        w, p = z.split(':')
        if w in self.token_map:
            self.token_map[w] += ' ' + p
            return ''
        self.token_map[w] = p
        return w

    def merge_files(self):
        end = time.time()
        self.files = [open(os.path.join(self.path_to_index, filename), 'r')
                      for filename in os.listdir(self.path_to_index) if
                      filename.startswith('__')]
        self.files_remaining = set(x for x in range(len(self.files)))
        self.file_opened = [1] * len(self.files)
        heap = [self.getLine(x) for x in range(len(self.files)) if x != '']
        heapq.heapify(heap)
        size = 0

        while len(heap) > 0:
            x = heapq.heappop(heap)
            self.posting[x] = self.token_map.pop(x, '')
            size += len(x) + len(self.posting[x]) + 1

            for f in self.files_remaining:
                if (w := self.getLine(f)) != '':
                    self.total_unique_tokens += 1
                    heapq.heappush(heap, w)
            self.files_remaining.difference_update(self.files_to_remove)
            self.files_to_remove = set()

            if size >= MAX_INDEX_FILE_SIZE:
                self.write_indexes()
                size = 0
        self.write_indexes()

        print("Time for merging: ", time.time() - end)

    def post_cleanup(self):
        index_heads = '\n'.join(self.index_heads)
        with open(os.path.join(self.path_to_index, 'heads.txt'), 'w') as f:
            f.write(index_heads)

        for filename in os.listdir(self.path_to_index):
            if filename.startswith('__'):
                os.remove(os.path.join(self.path_to_index, filename))

    def write_tokens(self):
        formatted_string = '\n'.join(
            tok + ':' + self.token_map[tok] for tok in sorted(self.token_map.keys()))
        with open(self.get_token_filename(self.token_file_count), 'w') as f:
            f.write(formatted_string)
        self.token_file_count += 1
        self.token_map = {}
        self.token_size = 0

    def write_titles(self):
        formatted_string = '\n'.join(self.titles)
        with open(self.get_title_filename(self.title_file_count), 'w') as f:
            f.write(formatted_string)
        self.title_file_count += 1
        self.titles = []

    def write_indexes(self):
        if len(self.posting) == 0:
            return
        sorted_keys = sorted(self.posting.keys())
        self.index_heads.append(sorted_keys[0])
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

    def add_titles(self, title):
        self.titles.append(title.strip())
        if len(self.titles) >= MAX_TITLES:
            self.write_titles()

    def merge_tokens(self, doc_id, doc_map):
        # (count, id,  tags)
        for tok, val in doc_map.items():
            if tok in self.token_map:
                z = ' ' + format_tuple(doc_id, val[0], val[1])
                self.token_map[tok] += z
                self.token_size += len(z)
            else:
                self.token_map[tok] = format_tuple(doc_id, val[0], val[1])
                self.token_size += len(self.token_map[tok]) + len(tok) + 1
        if self.token_size >= MAX_TOKEN_FILE_SIZE:
            self.write_tokens()
