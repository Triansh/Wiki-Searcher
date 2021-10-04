from math import log
from collections import Counter


class Ranker(object):

    def __init__(self):
        self.k1 = 1.2
        self.b = 0.75
        self.total_docs = 16195639
        self.avg_doc_len = 5600
        self.min_doc_size = 3000
        self.max_doc_size = 18000

        self.max_file_lines = 1 * (10 ** 4)
        self.reset()
        self.results = []
        self.doc_size = []

        self.limit = 10

    def reset(self):
        self.idf_scores = {}
        self.word_count = {}
        self.all_word_posting = {}
        self.final_score = {}
        self.doc_counter = Counter()

    def calculate_scores(self):
        self.idf_scores = {k: self.get_idf(v) for k, v in self.word_count.items()}
        [self.final_score.update(
            {d_id: self.get_score(w, d_id, ct) + self.final_score.get(d_id, 0)})
            for w, d in self.all_word_posting.items() for ct, d_id in d]
        self.results = sorted([(self.doc_counter[k], v, k) for k, v in self.final_score.items()],
                              reverse=True)[:self.limit]
        self.results = [x[2] for x in self.results]

    def get_score(self, word, doc_id, word_freq):
        d_size = max(self.min_doc_size, min(self.max_doc_size, self.doc_size[doc_id]))
        return self.idf_scores[word] * word_freq * (self.k1 + 1) / (word_freq + (
                self.k1 * (1 - self.b + (self.b * d_size / self.avg_doc_len))))

    def get_idf(self, val):
        return log(1 + ((self.total_docs - val + 0.5) / (val + 0.5)))
