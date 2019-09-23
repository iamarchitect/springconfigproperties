import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer  # Assuming we're working with English


class Index:
    """ Inverted index datastructure """

    def __init__(self, tokenizer, stemmer=None, stopwords=None):
        """
        tokenizer   -- NLTK compatible tokenizer function
        stemmer     -- NLTK compatible stemmer
        stopwords   -- list of ignored words
        """
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.index = defaultdict(list)
        self.documents = {}
        self.__unique_id = 0
        if not stopwords:
            self.stopwords = set()
        else:
            self.stopwords = set(stopwords)

    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)
            print(word)
            
        if self.index.get(word)==None:
            return None

        return [self.documents.get(id, None) for id in self.index.get(word)]

    def add(self, document):
        """
        Add a document string to the index
        """
        for token in [t.lower() for t in nltk.word_tokenize(document)]:
            if token in self.stopwords:
                continue

            if self.stemmer:
                token = self.stemmer.stem(token)

            if self.__unique_id not in self.index[token]:
                self.index[token].append(self.__unique_id)

        self.documents[self.__unique_id] = document
        self.__unique_id += 1


index = Index(nltk.word_tokenize,
              EnglishStemmer(),
              nltk.corpus.stopwords.words('english'))

index.add('Industrial Disease')
index.add('Private Investigations')
index.add('So Far Away')
index.add('Twisting by the Pool')
index.add('Skateaway')
index.add('Walk of Life')
index.add('Romeo and Juliet')
index.add('Tunnel of Love')
index.add('Money for Nothing')
index.add('Sultans of Swing')

# TOP10 Led Zeppelin
index.add('Stairway To Heaven')
index.add('Kashmir')
index.add('Achilles Last Stand')
index.add('Whole Lotta Love')
index.add('Immigrant Song')
index.add('Black Dog')
index.add('When The Levee Breaks')
index.add('Since I\'ve Been Lovin\' You')
index.add('Since I\'ve Been Loving You')
index.add('Over the Hills and Far Away')
index.add('Dazed and Confused')

print(index.lookup('music'))