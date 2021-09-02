token_regex = r'[^0-9a-z]+'
infobox_regex = r"{{ ?infobox(.|\n)*?\n}}"
category_regex = r"\[\[ ?category.*?\]\]"
# ref1_regex = r"(< ?ref([^>])*>.*?</ref>)"
ref1_regex = r"<([^>])*>(.|\n)*?</([^>])*>"
ref2_regex = r"== ?references ?==(.|\n)*?\n\n"
links_regex = r"== ?external links ?==(.|\n)*?\n\n"

ignore_ref_regex = r"(< ?ref[^/>]*/>)"
garbage_regex = r"([0-9]+[a-z]+[0-9a-z]+)|([a-z]+[0-9]+[0-9a-z]+)|([0-9]{4}[a-z0-9]+)"
http_regex = r"(https?://|www.)[^\s]+"
# http_regex = r"https?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+"
# attr_regex = r"(\w+ )*?\w+ *="
attr_regex = r"[a-z0-9_]+ *="
MAX_TOKEN_SIZE = 200000
