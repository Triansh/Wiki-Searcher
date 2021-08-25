token_regex = r'[^a-zA-Z0-9]+'
infobox_regex = r"{{infobox|{{ infobox"
reference_regex = r"<ref"
category_regex = r"\[\[.*category"
links_regex = r"==.*external links.*==|==.*links.*=="
garbage_regex = r"([0-9]+[a-z]+[0-9a-z]+)|([a-z]+[0-9]+[0-9a-z]+)"

extra_stop_words = ['https', 'url', 'http', 'ref']
punctuations = list("?:!.,;")