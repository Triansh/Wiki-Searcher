import os


class InvertedIndex(object):

    def __init__(self, path_to_index):
        self.token_map = {}
        self.token_count = 0
        self.path_to_index = os.path.join(os.getcwd(), path_to_index)
        self.file_path = os.path.join(self.path_to_index, 'index.txt')

    @staticmethod
    def format_tuple(doc_id, count, tags):
        x = ','.join((str(doc_id), str(count), ''.join(tags)))
        return x[:-1] if x[-1] == ',' else x

    def finish(self):
        formatted_string = '\n'.join([tok + ':' + ' '.join(self.token_map[tok])
                                      for tok in sorted(self.token_map.keys())])
        with open(self.file_path, 'w') as f:
            f.write(formatted_string)

    def merge_tokens(self, doc_id, doc_map):
        # (id, count, tags)
        for tok, val in doc_map.items():
            if tok in self.token_map:
                self.token_map[tok].append(self.format_tuple(doc_id, val[0], val[1]))
            else:
                self.token_map[tok] = [self.format_tuple(doc_id, val[0], val[1])]
                self.token_count += 1
