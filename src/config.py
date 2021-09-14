token_regex = r'[^0-9a-z]+'
infobox_regex = r"{{ ?infobox(.|\n)*?\n}}"
category_regex = r"\[\[ ?category.*?\]\]"
ref1_regex = r"< ?ref[^>]*>(?:.|\n)*?< ?/ref[^>]*>"
ref2_regex = r"== ?references ?==(?:.|\n)*?\n\n"
links_regex = r"== ?external links ?==(?:.|\n)*?\n\n"

ignore_ref_regex = r"<(?!>/).*?/>"
garbage_regex = r"([0-9]+[a-z]+[0-9a-z]+)|([a-z]+[0-9]+[0-9a-z]+)"
http_regex = r"(https?://|www.)[^(\s|\||})]+"
remove_html_regex = r"<[^>]*>"
# attr_regex = r"(\w+ )*?\w+ *="
# attr_regex = r"\w+ *="

MAX_TOKEN_FILE_SIZE = 80 * (10 ** 6)
MAX_TITLES = 5 * (10 ** 3)
MAX_INDEX_FILE_SIZE = 10 * (10 ** 6)
