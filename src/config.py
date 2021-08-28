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

extra_stop_words = ["with", "down", "they'll", "words", "he'll", "any", "she'd", "to", "are", "was",
                    "above", "re", "that", "whole", "aren", "couldn", "about", "werent", "my",
                    "ought", "wed", "z", "which", "while", "do", "who'll", "over", "won", "our",
                    "did", "when", "it's", "be", "whom", "whither", "just", "didn't", "why", "w",
                    "she's", "would", "own", "been", "let's", "nor", "you're", "whos", "he", "by",
                    "that's", "after", "she", "whod", "who", "more", "i'll", "off", "no", "youre",
                    "t", "yet", "i'd", "below", "very", "needn", "didn", "ourselves", "before",
                    "lt", "mustn't", "gte", "these", "gt", "or", "whatever", "whim", "x", "m",
                    "then", "as", "further", "there", "now", "ain", "needn't", "doing", "where's",
                    "should've", "an", "them", "herself", "you'd", "went", "yours", "in",
                    "themselves", "doesn't", "too", "yes", "each", "myself", "this", "you", "doesn",
                    "what'll", "autocollaps", "yourselves", "than", "ve", "hasn't", "youd", "him",
                    "only", "want", "how's", "here", "from", "some", "they're", "don't", "wasnt",
                    "won't", "your", "I", "yourself", "that'll", "where", "out", "ma", "s",
                    "has", "until", "being", "hadn't", "o", "on", "how", "am", "you've", "wherein",
                    "whereupon", "wherever", "y", "mightn't", "widely", "most", "mustn", "i",
                    "whether", "whereby", "hadn", "we'd", "wants", "haven", "up", "within",
                    "during", "few", "autocollapse", "should", "had", "whereafter", "shouldn't",
                    "again", "ours", "when's", "so", "wasn't", "itself", "of", "whereas", "if",
                    "it", "he's", "himself", "there's", "whoever", "hers", "weren", "wouldnt",
                    "mightn", "without", "he'd", "the", "they'd", "whence", "we're", "we've", "and",
                    "wont", "me", "under", "were", "between", "his", "what", "whose", "can", "d",
                    "wouldn't", "all", "couldn't", "for", "here's", "such", "we", "a", "we'll",
                    "wheres", "wasn", "ll", "you'll", "at", "welcome", "other", "not", "whomever",
                    "their", "is", "isn't", "against", "its", "she'll", "shouldn", "vs", "com",
                    "theirs", "wish", "whats", "does", "what's", "could", "isn", "same", "through",
                    "ref", "i've", "cannot", "into", "shan't", "lte", "both", "why's", "don",
                    "shan", "once", "they've", "whenever", "will", "haven't", "but", "willing",
                    "hasn", "aren't", "her", "those", "weren't", "wouldn", "because", "having",
                    "can't", "www", "they", "have", "who's", "i'm", "way"]
