from math import log
import time


class Ranker(object):

    def __init__(self):
        self.k1 = 1.2
        self.b = 0
        # Small data
        # self.total_docs = 52612
        # self.avg_doc_len = 15296514 / self.total_docs
        # self.max_file_lines = 10 ** 4
        # Large data
        self.total_docs = 21384756
        # self.avg_doc_len = 6538956940 / self.total_docs  # 6566129638
        self.max_file_lines = 5 * (10 ** 3)

        self.idf_scores = {}
        self.word_count = {}
        self.all_word_posting = {}
        self.final_score = {}
        self.results = []
        self.limit = 20

        self.checker = 0

    def calculate_scores(self):
        st = time.time()
        self.idf_scores = {k: self.get_idf(v) for k, v in self.word_count.items()}
        print(self.idf_scores)
        print("Time taken for getting idf scores: ", time.time() - st)
        st = time.time()
        [self.final_score.update(
            {d_id: self.get_score(w, d_id, ct) + self.final_score.get(d_id, 0)})
            for w, d in self.all_word_posting.items() for ct, d_id in d]
        # print(self.final_score)
        # for w, d in self.all_word_posting.items():
        #     for ct, d_id in d:
        #         self.final_score[d_id] += self.get_score(w, d_id, ct)
        self.results = [k for k, v in
                        sorted(self.final_score.items(), key=lambda x: x[1], reverse=True)[
                        :self.limit]]
        # print(self.results)
        print("Time taken for getting tf scores: ", time.time() - st)

    def get_score(self, word, doc_id, word_freq):
        return self.idf_scores[word] * (1 + (word_freq * (self.k1 + 1) / (word_freq + self.k1)))

    def get_idf(self, val):
        return log(1 + ((self.total_docs - val + 0.5) / (val + 0.5)))
