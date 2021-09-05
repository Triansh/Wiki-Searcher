import heapq


class WordToken(object):
    def __init__(self, word, posting, fileno):
        self.word = word
        self.posting = posting
        self.file_no = fileno

    def merge(self, other):
        self.posting = self.posting + ' ' + other.posting

    def __lt__(self, other):
        if self.word == other.word:
            return self.file_no < other.file_no
        return self.word < other.word


class Heap(object):

    def __init__(self, items):
        self.heap = items
        heapq.heapify(self.heap)

    def add(self, item: WordToken):
        if item.word != '':
            heapq.heappush(self.heap, item)

    def pop(self) -> WordToken:
        return heapq.heappop(self.heap)

    def top(self) -> WordToken:
        return heapq.nsmallest(1, self.heap)[0]

    def empty(self):
        return len(self.heap) == 0
