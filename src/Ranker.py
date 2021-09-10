from math import log
import time


class Ranker(object):

    def __init__(self):
        self.k1 = 1.2
        self.b = 0.75
        # Small data
        # self.total_docs = 52612
        # self.avg_doc_len = 15296514 / self.total_docs
        # self.max_file_lines = 10 ** 4
        # Large data
        self.total_docs = 21384756
        self.avg_doc_len = 6566129638 / self.total_docs
        self.max_file_lines = 10 ** 4

        self.idf_scores = {}
        self.word_count = {}
        self.word_to_doc_map = {}
        self.final_score = {}
        self.doc_size = {}
        self.results = []
        self.limit = 30

    def calculate_scores(self):
        self.idf_scores = {k: self.get_idf(v) for k, v in self.word_count.items()}
        st = time.time()
        [self.final_score.update(
            {d_id: self.get_score(w, d_id, ct) + self.final_score.get(d_id, 0)})
            for w, d in self.word_to_doc_map.items() for ct, d_id in d]
        # print(self.final_score)
        # for w, d in self.word_to_doc_map.items():
        #     for ct, d_id in d:
        #         self.final_score[d_id] += self.get_score(w, d_id, ct)
        self.results = [k for k, v in
                        sorted(self.final_score.items(), key=lambda x: x[1], reverse=True)[
                        :self.limit]]
        # print(self.results)
        print("Time taken for getting scores: ", time.time() - st)

    def get_score(self, word, doc_id, word_freq):
        return (self.idf_scores[word] * word_freq * (self.k1 + 1) / (word_freq + (
                self.k1 * (1 - self.b + (self.b * self.doc_size[doc_id] / self.avg_doc_len)))))

    def get_idf(self, val):
        return log(1 + ((self.total_docs - val + 0.5) / (val + 0.5)))
