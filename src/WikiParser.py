import xml.sax
from TextProcessor import TextProcessor
from InvertedIndex import InvertedIndex


class WikiParser(xml.sax.handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self._charBuffer = ""
        self._page = {}
        self.id_taken = False
        self.tags = ['title', 'id', 'text']
        self.processor = TextProcessor()
        self.titles = []
        self.doc_count = 0
        self.indexer = InvertedIndex()

    def parse(self, f):
        xml.sax.parse(f, self)

    def characters(self, data):
        self._charBuffer += data

    def startElement(self, name, attrs):
        if name == 'page':
            self.id_taken = False
            self._page = {}
        if name in self.tags:
            self._charBuffer = ""

    def endElement(self, name):
        if name == 'page':
            self.titles.append(self._page['title'])
            self.doc_count += 1
            tok_doc = self.processor.processDoc(self._page)
            self.indexer.merge_tokens(self.doc_count, tok_doc)

        if name in self.tags:
            if name != 'id':
                self._page[name] = self._charBuffer
            elif self.id_taken is False:
                self._page[name] = self._charBuffer
                self.id_taken = True

    def getResult(self, path_to_wiki_dump):
        self.parse(str(path_to_wiki_dump))
        print("Number of tokens: ", self.indexer.token_count)
        print("Number of docs: ", self.doc_count)
        # return self.result
