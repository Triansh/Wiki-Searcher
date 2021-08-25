import config
from config import punctuations, extra_stop_words
import re
from nltk.corpus import stopwords
from Stemmer import Stemmer
# from nltk.stem import LancasterStemmer

class TextProcessor(object):
    def __init__(self):
        self.stemmer = Stemmer('english')
        # self.stemmer = LancasterStemmer()
        self.stop_words = set(stopwords.words('english') + punctuations + extra_stop_words)

        self.token_regex = re.compile(config.token_regex)
        self.infobox_regex = re.compile(config.infobox_regex)
        self.category_regex = re.compile(config.category_regex)
        self.link_regex = re.compile(config.links_regex)
        self.reference_regex = re.compile(config.reference_regex)
        self.garbage_regex = re.compile(config.garbage_regex)

        self.doc_map = {}

    def processDoc(self, doc):
        self.doc_map = {}
        title = doc['title']
        content = doc['text'].lower()
        self.cleanup(content, '', False)
        self.extract_title(title.lower())
        self.extract_infobox(content)
        self.extract_categories(content)
        self.extract_links(content)
        self.extract_references(content + title.lower())
        return self.doc_map

    # Extract titles and don't stem it
    def extract_title(self, content):
        title = content.strip()
        texts = self.cleanup(title, 't', True, False)

    # Remove infoboxes to avoid redundant content
    def extract_infobox(self, content):
        splits = [x.end() for x in self.infobox_regex.finditer(content)]
        texts = [self.cleanup(content[index:(index + x)], 'i') for index in splits if
                 (x := content[index:].find('\n}}')) != -1]

    # Remove Category to avoid redundant content
    def extract_categories(self, content):
        splits = [x.end() for x in self.category_regex.finditer(content)]
        texts = [self.cleanup(content[index:(index + x)], 'c') for index in splits if
                 (x := content[index:].find(']]')) != -1]

    # Remove reference tags and https to avoid redundant content
    def extract_references(self, content):
        splits = [x.end() for x in self.reference_regex.finditer(content)]
        texts = [self.cleanup(content[index:(index + x)], 'r') for index in splits if
                 (x := content[index:].find('</ref>')) != -1]
        # print(texts)

    # Remove https and cite to avoid redundant content
    def extract_links(self, content):
        splits = [x.end() for x in self.link_regex.finditer(content)]
        texts = [self.cleanup(content[index:(index + x)], 'l') for index in splits if
                 (x := content[index:].find('\n\n')) != -1]
        # print(texts)

    def cleanup(self, content, add_tag, reduce=True, stem=True):

        stem_sentence = [(self.stemmer.stemWord(x) if stem else x) for x in
                         self.token_regex.split(content.strip()) if (x not in self.stop_words)]
        if reduce:
            stem_sentence = set(stem_sentence)
        stem_sentence = [x for x in stem_sentence if
                         len(x) > 1 and (not self.garbage_regex.match(x)) and
                         not (x[0] in '0123456789' and len(x) > 4)]
        for token in stem_sentence:
            if token in self.doc_map:
                if add_tag == "":
                    self.doc_map[token][0] += 1
                else:
                    self.doc_map[token][1] += add_tag
            else:
                self.doc_map[token] = [1, '']

        # return " ".join(stem_sentence)
        return ""
