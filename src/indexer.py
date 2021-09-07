import sys
import os
import time
import xml.sax
import resource

from TextProcessor import TextProcessor
from InvertedIndex import InvertedIndex


class WikiParser(xml.sax.handler.ContentHandler):
    def __init__(self, path_to_index_dir, path_to_stat_file):
        super().__init__()

        self.parser = xml.sax.make_parser()
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.parser.setContentHandler(self)

        self.path_to_stat = os.path.join(os.getcwd(), path_to_stat_file)
        self.indexer = InvertedIndex(path_to_index_dir)
        self.processor = TextProcessor()

        self._charBuffer = ""
        self._page = {}
        self.doc_count = 0

    def characters(self, data):
        self._charBuffer += data

    def startElement(self, name, attrs):
        if name == 'page':
            self._page = {}
        elif name == 'title' or name == 'text':
            self._charBuffer = ""

    def endElement(self, name):
        if name == 'page':
            self.doc_count += 1
            self.processor.process_doc(self._page)
            self.indexer.merge_tokens(self.doc_count, self.processor.doc_map, self._page['title'])
            self.processor.reset()
        elif name == 'title' or name == 'text':
            self._page[name] = self._charBuffer.lower()
        elif name == 'mediawiki':
            self.indexer.finish()

    def getResult(self, path_to_wiki_dump):
        self.parser.parse(str(path_to_wiki_dump))
        stats = f"""
        Number of total unique tokens: {self.indexer.total_unique_tokens}
        Number of documents: {self.doc_count}
        Number of intermediate files: {self.indexer.token_file_count}
        Number of index files in index: {self.indexer.index_file_count}
        Number of title files in index: {self.indexer.title_file_count}
        Total files: {self.indexer.index_file_count + self.indexer.title_file_count + 1}"""
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
    print("Memory taken: ", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (10 ** 6), " GB")
