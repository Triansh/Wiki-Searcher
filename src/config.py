token_regex = r'[^\da-z\']+'
infobox_regex = r"{{ ?infobox(?:.|\n)*?\n}}"
ignore_ref_regex = r"(< ?ref[^/>]*/>)"
ref1_regex = r"(< ?ref([^>])*>.*?</ref>)"
category_regex = r"\[\[ ?category.*?\]\]"
ref2_regex = r"== ?references ?==(.|\n)*?\n\n"
links_regex = r"== ?external links ?==(.|\n)*?\n\n"
garbage_regex = r"(\d+[a-z]+[\da-z]+)|([a-z]+\d+[\da-z]+)|(\d{4}[a-z\d]+)"
http_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
attr_regex = r"\w+ *="

MAX_TOKEN_SIZE = 200000
