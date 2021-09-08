from math import log


class Ranker(object):

    def __init__(self):
        self.k1 = 1.2
        self.b = 0.75
        self.total_docs = 52612  # 21384756
        self.avg_doc_len = 20000
        self.idf_scores = {}
        self.word_count = {}
        self.word_to_doc_map = {}
        self.final_score = {}
        self.doc_size = {}
        self.results = []

    def calculate_scores(self):
        self.idf_scores = {k: self.get_idf(v) for k, v in self.word_count.items()}
        for w, d in self.word_to_doc_map.items():
            for doc_data in d:
                self.final_score[doc_data[1]] += self.get_score(w, doc_data[1], doc_data[0])
        self.results = [k for k, v in
                        sorted(self.final_score.items(), key=lambda x: x[1], reverse=True)[:10]]

    def get_score(self, word, doc_id, word_freq):
        return (self.idf_scores[word] * word_freq * (self.k1 + 1) / (word_freq + (
                self.k1 * (1 - self.b + (self.b * self.doc_size[doc_id] / self.avg_doc_len)))))

    def get_idf(self, val):
        return log(1 + ((self.total_docs - val + 0.5) / (val + 0.5)))
