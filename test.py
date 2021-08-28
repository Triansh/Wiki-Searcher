from nltk.corpus import stopwords

x = []
with open('src/stopwords.txt', 'r') as f:
    x = [x.strip() for x in f.readlines() if x.strip() != '']
    x += stopwords.words('english')
    x = set(x)
    print(len(x))
with open('src/stopwords2.txt', 'w') as f:
    f.write(','.join(f"\"{y}\"" for y in x))
