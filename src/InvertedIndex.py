# import copy
import os


# from multiprocessing import Process
# from threading import Thread
# from config import MAX_TOKEN_SIZE


class InvertedIndex(object):

    def __init__(self, path_to_index):
        self.token_map = {}
        self.token_count = 0
        self.path_to_index = os.path.join(os.getcwd(), path_to_index)
        self.file_count = 1

        # self.threads = []

    def get_filename(self, file_num):
        return os.path.join(self.path_to_index, f'index_{file_num}.txt')

    @staticmethod
    def format_tuple(doc_id, count, tags):
        x = ','.join((str(count), str(doc_id), ''.join(tags)))
        return x[:-1] if x[-1] == ',' else x

    # def write_files(self, tok_map, file_num):
    #     formatted_string = '\n'.join([tok + ':' + ' '.join(tok_map[tok])
    #                                   for tok in sorted(tok_map.keys())])
    #     with open(self.get_filename(file_num), 'w') as f:
    #         f.write(formatted_string)

    def write_files(self):
        formatted_string = '\n'.join([tok + ':' + ' '.join(self.token_map[tok])
                                      for tok in sorted(self.token_map.keys())])
        with open(self.get_filename(self.file_count), 'w') as f:
            f.write(formatted_string)
        self.reset()

    def reset(self):
        self.token_map = {}
        self.file_count += 1

    # def start_thread(self):
    #     t = Thread(
    #         target=self.write_files, args=(copy.deepcopy(self.token_map), self.file_count))
    #     t.start()
    #     self.threads.append(t)
    #     self.reset()

    # def finish(self):
    #     all(t.join() or True for t in self.threads)

    def merge_tokens(self, doc_id, doc_map):
        # (count, id,  tags)
        for tok, val in doc_map.items():
            if tok in self.token_map:
                self.token_map[tok].append(self.format_tuple(doc_id, val[0], val[1]))
            else:
                self.token_map[tok] = [self.format_tuple(doc_id, val[0], val[1])]
                self.token_count += 1

        # if len(self.token_map) >= MAX_TOKEN_SIZE:
        #     self.start_thread()
        #     self.file_count += 1
        #     self.reset()
