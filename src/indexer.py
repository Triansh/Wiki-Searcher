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
        self.dont_take = False
        self._page = {}
        # self.id_taken = False
        self.tags = ['title', 'text']
        self.processor = TextProcessor()
        # self.titles = []
        self.doc_count = 1
        self.total_words = set()
        self.indexer = InvertedIndex(path_to_index_dir)

    def parse(self, f):
        self.parser.parse(f)

    def characters(self, data):
        self._charBuffer += data

    def startElement(self, name, attrs):
        if name == 'page':
            # self.id_taken = False
            self._page = {}
        if name in self.tags:
            self._charBuffer = ""

    def endElement(self, name):
        if name == 'page':
            # if not self.dont_take:
            # self.titles.append(self._page['title'])
            tok_doc = self.processor.process_doc(self._page)
            # print(words)
            # self.total_words = self.total_words.union(words)
            self.indexer.merge_tokens(self.doc_count, tok_doc)
            self.doc_count += 1

        elif name == 'mediawiki':
            self.indexer.write_files()
            # self.indexer.start_thread()
            # self.indexer.finish()

        # elif name == 'title':
        #     self.dont_take = True if self._charBuffer.lower().startswith("wikipedia:") else False
        #     if not self.dont_take:
        #         self._page[name] = self._charBuffer
        # elif name == 'text':
        #     if not self.dont_take:
        #         self._page[name] = self._charBuffer
        # elif self.id_taken is False:
        #     self._page[name] = self._charBuffer
        #     self.id_taken = True

        if name in self.tags:
            self._page[name] = self._charBuffer

    def getResult(self, path_to_wiki_dump):
        # print(self.processor.cleanup('۵۰۰'.lower(), 'g'))
        self.parse(str(path_to_wiki_dump))
        stats = f"{len(self.total_words)}\n{self.indexer.token_count}\n{self.doc_count}"
        with open(self.path_to_stat, 'w') as f:
            f.write(stats)


if __name__ == '__main__':
    start = time.time()

    path_to_wiki = sys.argv[1]
    path_to_index = sys.argv[2]
    path_to_stat = sys.argv[3]
    handler = WikiParser(path_to_index, path_to_stat)
    handler.getResult(path_to_wiki)

    end = time.time() - start

    print("Time taken: ", end)
