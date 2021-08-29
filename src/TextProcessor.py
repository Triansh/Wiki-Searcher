import os
import config
import re
import pickle
from Stemmer import Stemmer


class TextProcessor(object):
    def __init__(self):
        self.stemmer = Stemmer('english')
        with open(os.path.join(os.getcwd(), 'src/stopwords.pkl'), 'rb') as f:
            self.stop_words = set(pickle.load(f))

        self.token_regex = re.compile(config.token_regex)
        self.infobox_regex = re.compile(config.infobox_regex)
        self.category_regex = re.compile(config.category_regex)
        self.link_regex = re.compile(config.links_regex)
        self.ref1_regex = re.compile(config.ref1_regex)
        self.ref2_regex = re.compile(config.ref2_regex)

        self.garbage_regex = re.compile(config.garbage_regex)
        self.ignore_ref_regex = re.compile(config.ignore_ref_regex)
        self.http_regex = re.compile(config.http_regex)
        self.attr_regex = re.compile(config.attr_regex)

        self.doc_map = {}

    def remove_pattern(self, content):
        content = self.http_regex.sub(' ', content)
        content = self.attr_regex.sub(' ', content)
        return content

    def process_doc(self, doc):
        self.doc_map = {}
        title = doc['title'].lower().strip()

        content = self.ignore_ref_regex.sub(' ', doc['text'].lower())
        content = self.extract_infobox(content)
        content = self.extract_ref2(content)
        content = self.extract_links(content)
        content = self.extract_ref1(content)
        content = self.extract_categories(content)
        self.extract_title(title)
        self.cleanup(self.remove_pattern(content + title), '', False)

        return self.doc_map

    # Extract titles and don't stem it #TODO
    def extract_title(self, title):
        self.cleanup(title, 't', True, True)

    # Remove infoboxes
    def extract_infobox(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            ind = t.find('infobox')
            self.cleanup(t if ind == -1 else t[(ind + 7):], 'i')
            return ' '

        return self.infobox_regex.sub(res_sub, content)

    # Remove Category
    def extract_categories(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            ind = t.find(':')
            self.cleanup(t if ind == -1 else t[ind:], 'c')
            return ' '

        return self.category_regex.sub(res_sub, content)

    # Remove reference tags
    def extract_ref1(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            ind = t.find('>')
            self.cleanup(t if ind == -1 else t[ind:], 'r')
            return ' '

        return self.ref1_regex.sub(res_sub, content)

    # Remove references section
    def extract_ref2(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            ind = t.find('\n')
            self.cleanup(t if ind == -1 else t[ind:], 'r')
            return ' '

        return self.ref2_regex.sub(res_sub, content)

    # Remove external links section
    def extract_links(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            ind = t.find('\n')
            self.cleanup(t if ind == -1 else t[ind:], 'l')
            return ' '

        return self.link_regex.sub(res_sub, content)

    def cleanup(self, content, add_tag, reduce=True, stem=True):

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
