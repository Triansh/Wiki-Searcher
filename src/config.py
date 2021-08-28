token_regex = r'[^a-z0-9]+'
infobox_regex = r"{{ ?infobox(?:.|\n)*?\n}}"
ignore_ref_regex = r"(< ?ref[^/>]*/>)"
reference_regex = r"(< ?ref([^>])*>.*?</ref>)"
category_regex = r"\[\[.*category.*?\]\]"
links_regex = r"==.*external links.*==|==.*links.*=="
garbage_regex = r"([0-9]+[a-z]+[0-9a-z]+)|([a-z]+[0-9]+[0-9a-z]+)|(\d{4}\d+)"
http_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
attr_regex = r"[0-9a-z_]+ *=[^=]"

FILE_TERM_SIZE = 30000

extra_stop_words = ["ll", "ought", "my", "against", "doesn't", "d", "through", "i've", "which",
                    "both", "you're", "whereas", "do", "that's", "hadn't", "theirs", "vs", "weren",
                    "just", "aren't", "i", "does", "went", "whoever", "we're", "what's", "words",
                    "them", "wed", "mightn", "wherever", "won", "mustn", "not", "over", "isn't",
                    "yourselves", "shan", "z", "couldn't", "won't", "me", "within", "their", "is",
                    "after", "wouldnt", "you", "in", "wouldn't", "whenever", "t", "how", "any",
                    "then", "it", "why's", "wasn't", "don", "you'd", "further", "am", "for", "own",
                    "same", "she's", "there's", "there", "out", "s", "by", "they'd", "youd", "ve",
                    "been", "isn", "ourselves", "yet", "were", "re", "at", "wish", "he'll", "below",
                    "if", "on", "each", "his", "x", "hasn't", "our", "under", "com", "whos", "wont",
                    "aren", "i'm", "above", "a", "weren't", "willing", "but", "you'll", "wasnt",
                    "whereby", "themselves", "being", "did", "him", "haven't", "to", "why", "so",
                    "while", "hers", "where's", "such", "he's", "who", "wherein", "whatever",
                    "this", "ma", "they'll", "other", "yours", "as", "m", "cannot", "whether",
                    "again", "once", "whereupon", "be", "himself", "we'd", "than", "most",
                    "mustn't", "no", "that", "werent", "too", "until", "where", "will", "between",
                    "yes", "off", "mightn't", "he", "whereafter", "some", "whence", "here", "i'd",
                    "don't", "she", "very", "when", "who's", "want", "y", "hasn", "these",
                    "didn't", "wasn", "ours", "few", "your", "could", "herself", "whose", "itself",
                    "now", "myself", "here's", "didn", "they", "shouldn", "are", "about", "had",
                    "how's", "her", "having", "can't", "nor", "let's", "I", "from", "down", "whim",
                    "wheres", "because", "can", "needn", "doesn", "whomever", "its", "and", "w",
                    "wants", "into", "with", "needn't", "without", "when's", "they've", "was", "of",
                    "or", "whither", "we'll", "couldn", "he'd", "has", "they're", "welcome",
                    "what'll", "all", "doing", "the", "you've", "those", "shouldn't", "we've",
                    "whom", "we", "should", "who'll", "o", "wouldn", "i'll", "would", "she'll",
                    "hadn", "an", "that'll", "haven", "during", "have", "what", "whole", "more",
                    "whats", "widely", "yourself", "youre", "ain", "way", "should've", "before",
                    "she'd", "it's", "up", "only", "whod", "www", "shan't", "00", "000"]
