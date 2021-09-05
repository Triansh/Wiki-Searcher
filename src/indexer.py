import sys, os
import time
import xml.sax
from TextProcessor import TextProcessor
from InvertedIndex import InvertedIndex


class WikiParser(xml.sax.handler.ContentHandler):
    def __init__(self, path_to_index_dir, path_to_stat_file):
        super().__init__()

        self.path_to_stat = os.path.join(os.getcwd(), path_to_stat_file)

        self.parser = xml.sax.make_parser()
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.parser.setContentHandler(self)

        self._charBuffer = ""
        self._page = {}
        self.tags = ['title', 'text']
        self.processor = TextProcessor()
        self.doc_count = 0
        self.indexer = InvertedIndex(path_to_index_dir)

    def parse(self, f):
        self.parser.parse(f)

    def characters(self, data):
        self._charBuffer += data

    def startElement(self, name, attrs):
        if name == 'page':
            self._page = {}
        if name in self.tags:
            self._charBuffer = ""

    def endElement(self, name):
        if name == 'page':
            self.doc_count += 1
            tok_doc = self.processor.process_doc(self._page)
            self.indexer.merge_tokens(self.doc_count, tok_doc)
            self.indexer.add_titles(self._page['title'])
        elif name == 'mediawiki':
            self.indexer.finish()

        if name in self.tags:
            self._page[name] = self._charBuffer.lower()

    def getResult(self, path_to_wiki_dump):
        self.parse(str(path_to_wiki_dump))
        stats = f"{len(self.processor.total_words)}\n{self.indexer.total_unique_tokens}\n{self.doc_count}\n"
        with open(self.path_to_stat, 'w') as f:
            f.write(stats)


if __name__ == '__main__':
    end = time.time()
    path_to_wiki = sys.argv[1]
    path_to_index = sys.argv[2]
    path_to_stat = sys.argv[3]
    handler = WikiParser(path_to_index, path_to_stat)
    handler.getResult(path_to_wiki)
    print("Time taken: ", time.time() - end)
