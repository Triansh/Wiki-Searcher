import sys
from WikiParser import WikiParser
import time

if __name__ == '__main__':
    path_to_wiki = sys.argv[1]
    # parser = xml.sax.make_parser()
    # parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = WikiParser()
    # parser.setContentHandler(handler)
    start = time.time()
    handler.getResult(path_to_wiki)
    end = time.time() - start

    print("Time taken: ", end)
