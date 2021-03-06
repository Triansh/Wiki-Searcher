import os
import config
import re
import pickle
from Stemmer import Stemmer
from collections import Counter


class TextProcessor(object):
    def __init__(self):
        self.stemmer = Stemmer('english')
        with open(os.path.join(os.getcwd(), 'src/stopwords.pkl'), 'rb') as f:
            self.stop_words = set(pickle.load(f))
        self.digits = set('0123456789')

        self.token_regex = re.compile(config.token_regex)
        self.infobox_regex = re.compile(config.infobox_regex)
        self.category_regex = re.compile(config.category_regex)
        self.link_regex = re.compile(config.links_regex)
        self.ref1_regex = re.compile(config.ref1_regex)
        self.ref2_regex = re.compile(config.ref2_regex)

        self.garbage_regex = re.compile(config.garbage_regex)
        self.ignore_ref_regex = re.compile(config.ignore_ref_regex)
        self.http_regex = re.compile(config.http_regex)
        self.html_regex = re.compile(config.remove_html_regex)

        self.doc_map = {}
        self.weights = {'t': 7, 'i': 3, 'c': 2, 'l': 1, 'r': 1, 'b': 1}

    def process_doc(self, doc):
        self.doc_map = {}
        title = doc['title'].strip()
        content = doc['text']
        content = self.ignore_ref_regex.sub(' ', content)
        content = self.extract_ref_tags(content)
        content = self.extract_categories(content)
        content = self.extract_infobox(content)
        content = self.extract_ref_section(content)
        content = self.extract_links(content)
        self.cleanup(content, 'b')
        self.extract_title(title)

    def extract_title(self, title):
        self.cleanup(title, 't')

    def re_sub(self, category):
        def replace(match):
            self.cleanup(match.group(0), category)
            return ' '

        return replace

    # Remove infoboxes
    def extract_infobox(self, content):
        return self.infobox_regex.sub(self.re_sub('i'), content)

    # Remove Category
    def extract_categories(self, content):
        return self.category_regex.sub(self.re_sub('c'), content)

    # Remove reference tags
    def extract_ref_tags(self, content):
        return self.ref1_regex.sub(self.re_sub('r'), content)

    # Remove references section
    def extract_ref_section(self, content):
        return self.ref2_regex.sub(self.re_sub('r'), content)

    # Remove external links section
    def extract_links(self, content):
        return self.link_regex.sub(self.re_sub('l'), content)

    def cleanup(self, ct, tag):

        content = self.html_regex.sub(' ', ct)
        content = self.http_regex.sub(' ', content)

        term_map = Counter(x for x in self.token_regex.split(content) if
                           (1 < len(x) <= 20) and x not in self.stop_words)

        for token, val in term_map.items():
            tok = self.stemmer.stemWord(token)
            if (1 < len(tok) <= 20) and not tok[:2] == "00" and not (
                    tok[0] in self.digits and len(tok) > 5) and not self.garbage_regex.match(tok):
                if tok in self.doc_map:
                    self.doc_map[tok][0] += val * self.weights[tag]
                    self.doc_map[tok][1] += tag
                else:
                    self.doc_map[tok] = [val * self.weights[tag], tag]
