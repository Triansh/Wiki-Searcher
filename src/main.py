# import sys
# import nltk
# from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
# from nltk.corpus import stopwords
# from nltk import sent_tokenize, word_tokenize
#
# porter = PorterStemmer()
# lancaster = LancasterStemmer()
# wordnet_lemmatizer = WordNetLemmatizer()
# stop_words = set(stopwords.words('english'))
# punctuations = "?:!.,;"
#
#
# def processDoc(doc):
#     token_words = word_tokenize(doc)
#     token_words = [x for x in token_words if x not in punctuations]
#     stem_sentence = [porter.stem(x) for x in token_words if x not in stop_words]
#     return " ".join(stem_sentence)
#
#
# if __name__ == '__main__':
#
#     word_list = ["friend", "friendship", "friends", "friendships", "stabil", "destabilize",
#                  "misunderstanding", "railroad", "moonlight", "football"]
#     # print("{0:20}{1:20}{2:20}".format("Word", "Porter Stemmer", "lancaster Stemmer"))
#     for word in word_list:
#         print("{0:20}{1:20}".format(word, wordnet_lemmatizer.lemmatize(word, pos="v")))
#
#     sentence = [
#         "Pythoners are very intelligent and work very pythonly and now they are pythoning their way to success.",
#         "He was running and eating at same time. He has bad habit of swimming after playing long hours in the Sun.",
#     ]
#     # x = [word_tokenize(x.lower()) for x in sentence]
#     x = [processDoc(x.lower()) for x in sentence]
#
#     print("\n".join(x))
