import os
import threading
import config
import re
import pickle
from Stemmer import Stemmer


class TextProcessor(object):
    def __init__(self):
        self.stemmer = Stemmer('english')
        with open(os.path.join(os.getcwd(), 'src/stopwords.pkl'), 'rb') as f:
            self.stop_words = set(pickle.load(f))
        # self.weird = set(list(
        #     "[☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼#$%&()*+,-./:;<=>?@[\]^_`¢£¥₧ƒªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■""}{]"))

        self.token_regex = re.compile(config.token_regex)
        self.infobox_regex = re.compile(config.infobox_regex)
        self.category_regex = re.compile(config.category_regex)
        self.link_regex = re.compile(config.links_regex)
        self.reference_regex = re.compile(config.reference_regex)
        self.ref2_regex = re.compile(config.ref2_regex)

        self.garbage_regex = re.compile(config.garbage_regex)
        self.ignore_ref_regex = re.compile(config.ignore_ref_regex)
        self.http_regex = re.compile(config.http_regex)
        self.attr_regex = re.compile(config.attr_regex)

        self.doc_map = {}

    def remove_pattern(self, content):
        content = self.ignore_ref_regex.sub(' ', content)
        content = self.http_regex.sub(' ', content)
        return content

    def process_doc(self, doc):
        self.doc_map = {}
        title = doc['title'].lower()
        content = self.remove_pattern(doc['text'].lower())

        self.extract_links(content)
        self.extract_ref2(content)

        content = self.attr_regex.sub(' ', content)

        self.cleanup(content + title, '', False)
        self.extract_title(title)
        self.extract_infobox(content)
        self.extract_categories(content)
        self.extract_references(content)
        return self.doc_map

    # Extract titles and don't stem it
    def extract_title(self, content):
        title = content.strip()
        self.cleanup(title, 't', True, False)

    # Remove infoboxes to avoid redundant content
    def extract_infobox(self, content):
        all(self.cleanup(text[(x + 7):], 'i') for text in self.infobox_regex.findall(content) if
            (x := text.find('infobox')) != -1)

    # Remove Category to avoid redundant content
    def extract_categories(self, content):
        all(self.cleanup(text[(x + 8):], 'c') for text in self.category_regex.findall(content) if
            (x := text.find('category')) != -1)

    # Remove references from references section
    def extract_ref2(self, content):
        splits = [x.end() for x in self.ref2_regex.finditer(content)]
        all(self.cleanup(content[index:(index + x)], 'r') for index in splits if
            (x := content[index:].find('\n\n')) != -1)

    # Remove reference tags and https to avoid redundant content
    def extract_references(self, content):
        all(self.cleanup(text[0][(x + 1):], 'r') for text in self.reference_regex.findall(content)
            if (x := text[0].find('>')) != -1)

    # Remove https and cite to avoid redundant content
    def extract_links(self, content):
        splits = [x.end() for x in self.link_regex.finditer(content)]
        all(self.cleanup(content[index:(index + x)], 'l') for index in splits if
            (x := content[index:].find('\n\n')) != -1)

    def cleanup(self, content, add_tag, reduce=True, stem=True):

        # if add_tag == 'i':
        #     print(content)
        #     print()

        stem_sentence = [(self.stemmer.stemWord(x) if stem else x) for y in
                         self.token_regex.split(content.strip()) for x in y.split('\'') if
                         len(x) > 1 and (x not in self.stop_words)]
        if reduce:
            stem_sentence = set(stem_sentence)
        stem_sentence = [x for x in stem_sentence if
                         len(x) > 1
                         # not any(c in self.weird for c in x)
                         and not self.garbage_regex.match(x)
                         and not (x[0:2] == "00")
                         ]
        for token in stem_sentence:
            if token in self.doc_map:
                if add_tag == "":
                    self.doc_map[token][0] += 1
                elif self.doc_map[token][1] == '' or self.doc_map[token][1][-1] != add_tag:
                    self.doc_map[token][1] += add_tag
            else:
                self.doc_map[token] = [1, '']

        # return " ".join(stem_sentence)
        return True
