# from collections import deque
# from queue import Queue


class InvertedIndex(object):

    def __init__(self):
        self.token_map = {}
        self.token_count = 0

    def merge_tokens(self, doc_id, doc_map):
        for tok, val in doc_map.items():
            if tok in self.token_map:
                self.token_map[tok].append((doc_id, val[0], val[1]))
            else:
                self.token_map[tok] = []
                self.token_map[tok].append((doc_id, val[0], val[1]))
                self.token_count += 1
