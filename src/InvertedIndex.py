import os
from utils import WordToken, Heap
from config import MAX_TOKEN_SIZE, MAX_TITLES


class InvertedIndex(object):

    def __init__(self, path_to_index):
        self.path_to_index = os.path.join(os.getcwd(), path_to_index)
        self.token_file_count = 1
        self.title_file_count = 1
        self.index_file_count = 1
        self.files = []

        self.token_map = {}
        self.posting = {}
        self.titles = []
        self.token_count = 0
        self.total_unique_tokens = 0
        # self.threads = []

    def get_title_filename(self, file_num):
        return os.path.join(self.path_to_index, f'title_{file_num}.txt')

    def get_token_filename(self, file_num):
        return os.path.join(self.path_to_index, f'__index_{file_num}.txt')

    def get_index_filename(self, file_num):
        return os.path.join(self.path_to_index, f'index_{file_num}.txt')

    @staticmethod
    def format_tuple(doc_id, count, tags):
        if tags == 'b':
            return ','.join((str(count), str(doc_id)))
        else:
            return ','.join((str(count), str(doc_id), tags))

    def getLine(self, file_num) -> WordToken:
        z = self.files[file_num].readline().strip()
        if z == '':
            w, p = '', ''
        else:
            w, p = z.split(':')
        return WordToken(w, p, file_num)

    def merge_files(self):
        # print(os.listdir(self.path_to_index))
        self.files = [open(os.path.join(self.path_to_index, filename), 'r')
                      for filename in os.listdir(self.path_to_index) if filename.startswith('__')]

        items = [self.getLine(x) for x in range(len(self.files))]
        heap = Heap(items)
        count_words = 0

        while not heap.empty():
            x = heap.pop()

            if x.word in self.posting:
                self.posting[x.word].merge(x)
            else:
                self.posting[x.word] = x
                self.total_unique_tokens += 1
                count_words += 1

            heap.add(self.getLine(x.file_no))
            while not heap.empty() and x.word == heap.top().word:
                z = heap.pop()
                self.posting[x.word].merge(z)
                heap.add(self.getLine(z.file_no))

            if count_words >= MAX_TOKEN_SIZE:
                count_words = 0
                self.write_indexes()
        self.write_indexes()

    def delete_files(self):
        for filename in os.listdir(self.path_to_index):
            if filename.startswith('__'):
                os.remove(os.path.join(self.path_to_index, filename))

    def write_tokens(self):
        formatted_string = '\n'.join(
            [tok + ':' + ' '.join(self.token_map[tok]) for tok in sorted(self.token_map.keys())])
        with open(self.get_token_filename(self.token_file_count), 'w') as f:
            f.write(formatted_string)
        self.token_file_count += 1
        self.token_map = {}

    def write_titles(self):
        formatted_string = '\n'.join(self.titles)
        with open(self.get_title_filename(self.title_file_count), 'w') as f:
            f.write(formatted_string)
        self.title_file_count += 1
        self.titles = []

    def write_indexes(self):
        if len(self.posting) == 0: return
        formatted_string = '\n'.join(
            [x + ':' + self.posting[x].posting for x in sorted(self.posting.keys())])
        with open(self.get_index_filename(self.index_file_count), 'w') as f:
            f.write(formatted_string)
        self.index_file_count += 1
        self.posting = {}

    # def start_thread(self):
    #     t = Thread(
    #         target=self.write_files, args=(copy.deepcopy(self.token_map), self.file_count))
    #     t.start()
    #     self.threads.append(t)
    #     self.reset()

    def finish(self):
        self.write_tokens()
        self.write_titles()
        self.merge_files()
        self.delete_files()
        # all(t.join() or True for t in self.threads)

    def add_titles(self, title):
        self.titles.append(title.strip())
        if len(self.titles) >= MAX_TITLES:
            self.write_titles()

    def merge_tokens(self, doc_id, doc_map):
        # (count, id,  tags)
        for tok, val in doc_map.items():
            if tok in self.token_map:
                self.token_map[tok].append(self.format_tuple(doc_id, val[0], ''.join(val[1])))
            else:
                self.token_map[tok] = [self.format_tuple(doc_id, val[0], ''.join(val[1]))]
                self.token_count += 1
        if len(self.token_map) >= MAX_TOKEN_SIZE:
            self.write_tokens()
