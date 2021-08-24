import config
import re
from nltk.corpus import stopwords
import Stemmer


# import pprint


class TextProcessor(object):
    def __init__(self):
        self.stemmer = Stemmer.Stemmer('english')
        self.stop_words = set(stopwords.words('english') + list("?:!.,;"))

        self.token_regex = re.compile(config.token_regex)
        self.infobox_regex = re.compile(config.infobox_regex)
        self.category_regex = re.compile(config.category_regex)
        self.link_regex = re.compile(config.links_regex)
        self.reference_regex = re.compile(config.reference_regex)

        self.doc_map = {}

    def processDoc(self, doc):
        self.doc_map = {}
        title = doc['title'].lower()
        content = doc['text'].lower()
        self.extract_title(title)
        self.extract_infobox(content)
        self.extract_categories(content)
        self.extract_links(content)
        self.extract_references(content)
        self.cleanup(content)
        # print()

    def extract_title(self, content):
        # print("Title: ")
        title = content.strip()
        texts = self.cleanup(title, 't', False)

        # pprint.pprint(texts)

    # Remove infoboxes to avoid redundant content
    def extract_infobox(self, content):
        # print("Infobox: ")
        splits = [x.start() for x in self.infobox_regex.finditer(content)]
        # print("Len splits:", len(splits))
        texts = [self.cleanup(content[index:(index + x)], 'i') for index in splits if
                 (x := content[index:].find('\n}}')) != -1]

        # pprint.pprint(texts)

    # Remove Category to avoid redundant content
    def extract_categories(self, content):
        # print("Categories: ")
        splits = [x.start() for x in self.category_regex.finditer(content)]
        # print("Len splits:", len(splits))
        texts = [self.cleanup(content[index:(index + x)], 'c') for index in splits if
                 (x := content[index:].find(']]')) != -1]

        # pprint.pprint(texts)

    # Remove refernce tags and https to avoid redundant content
    def extract_references(self, content):
        # print("References: ")
        splits = [x.start() for x in self.reference_regex.finditer(content)]
        # print("Len splits:", len(splits))
        texts = [(content[index:(index + x)], '') for index in splits if
                 (x := content[index:].find('</ref>')) != -1]

        # pprint.pprint(texts)

    # Remove https and cite to avoid redundant content
    def extract_links(self, content):
        # print("Links: ")
        splits = [x.start() for x in self.link_regex.finditer(content)]
        # print("Len splits:", len(splits))
        texts = [(content[index:(index + x)], '') for index in splits if
                 (x := content[index:].find('\n\n')) != -1]

        # pprint.pprint(texts)

    def cleanup(self, content, add_tag='', stem=True):
        stem_sentence = [(self.stemmer.stemWord(x) if stem else x) for x in
                         self.token_regex.split(content.strip()) if
                         (x not in self.stop_words)]
        for token in stem_sentence:
            if token in self.doc_map:
                if add_tag == "":
                    self.doc_map[token][0] += 1
                else:
                    self.doc_map[token][1] += add_tag
            else:
                self.doc_map[token] = [1, 'b']

        return ""
        # return " ".join(stem_sentence)
