token_regex = r'[^0-9a-z]+'
infobox_regex = r"{{ ?infobox(.|\n)*?\n}}"
category_regex = r"\[\[ ?category.*?\]\]"
ref1_regex = r"<[^>]*>(.|\n)*?< ?/[^>]*>"
ref2_regex = r"== ?references ?==(.|\n)*?\n\n"
links_regex = r"== ?external links ?==(.|\n)*?\n\n"

ignore_ref_regex = r"<(?!>/).*?/>"
garbage_regex = r"([0-9]+[a-z]+[0-9a-z]+)|([a-z]+[0-9]+[0-9a-z]+)"
http_regex = r"(https?://|www.)[^\s]+"
attr_regex = r"[a-z0-9_]+ *="

MAX_TOKEN_FILE_SIZE = 10 * (10 ** 6)
MAX_TITLES = 1 * (10 ** 4)
MAX_INDEX_FILE_SIZE = 10 * (10 ** 6)
