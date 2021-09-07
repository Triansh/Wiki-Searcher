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
        self.attr_regex = re.compile(config.attr_regex)

        self.doc_map = {}
        self.tag = ''

    def reset(self):
        self.doc_map = {}
        self.tag = ''

    def remove_pattern(self, content):
        content = self.http_regex.sub(' ', content)
        content = self.attr_regex.sub(' ', content)
        return content

    def process_doc(self, doc):
        title = doc['title'].strip()
        content = doc['text']
        content = self.ignore_ref_regex.sub(' ', content)
        # content = self.extract_ref1(content)
        content = self.extract_ref2(content)
        content = self.extract_categories(content)
        content = self.extract_links(content)
        content = self.extract_infobox(content)
        self.extract_title(title)
        self.tag = 'b'
        content = self.extract_ref1(content)
        self.cleanup(self.remove_pattern(content), 'b')

    # Extract titles and don't stem it #TODO
    def extract_title(self, title):
        self.cleanup(title, 't', False)

    # Remove infoboxes
    def extract_infobox(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            self.tag = 'i'
            t = self.extract_ref1(t)
            ind = t.find('infobox')
            self.cleanup(t if ind == -1 else t[(ind + 7):], 'i')
            return ' '

        return self.infobox_regex.sub(res_sub, content)

    # Remove Category
    def extract_categories(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            self.tag = 'c'
            t = self.extract_ref1(t)
            ind = t.find(':')
            self.cleanup(t if ind == -1 else t[ind:], 'c')
            return ' '

        return self.category_regex.sub(res_sub, content)

    # Remove reference tags
    def extract_ref1(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            ind = t.find('>')
            # print(t)
            if ind != -1:
                if 'ref' in t[:ind]:
                    self.cleanup(t[ind:], 'r')
                else:
                    self.cleanup(t[ind:], self.tag)
            return ' '

        return self.ref1_regex.sub(res_sub, content)

    # Remove references section
    def extract_ref2(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            self.tag = 'r'
            t = self.extract_ref1(t)
            ind = t.find('\n')
            self.cleanup(t if ind == -1 else t[ind:], 'r')
            return ' '

        return self.ref2_regex.sub(res_sub, content)

    # Remove external links section
    def extract_links(self, content):
        def res_sub(match_obj):
            t = self.remove_pattern(match_obj.group(0))
            self.tag = 'l'
            t = self.extract_ref1(t)
            ind = t.find('\n')
            self.cleanup(t if ind == -1 else t[ind:], 'l')
            return ' '

        return self.link_regex.sub(res_sub, content)

    def cleanup(self, content, tag, stem=True):

        term_map = Counter(x for x in self.token_regex.split(content)
                           if len(x) > 1 and x not in self.stop_words)

        for token, val in term_map.items():
            tok = self.stemmer.stemWord(token) if stem else token
            if len(tok) > 1 and not tok[:2] == "00" and not (
                    tok[0] in self.digits and len(tok) > 4) and not self.garbage_regex.match(tok):
                if tok in self.doc_map:
                    self.doc_map[tok][0] += val
                    self.doc_map[tok][1] += tag
                else:
                    self.doc_map[tok] = [val, tag]
