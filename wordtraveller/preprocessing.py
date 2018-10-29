import nltk
import re
import tempfile


class Preprocessor:

    def __init__(self):
        nltk.download('stopwords', download_dir=tempfile.gettempdir())
        nltk.data.path.append(tempfile.gettempdir())
        self.regex_money = re.compile(r'(\$€¥)\d+((\.\d+)?(\s(million|billion))?)?')
        self.regex_number = re.compile(     r'\d+((\.\d+)?(\s(million|billion))?)?')
        self.stemmer = nltk.stem.PorterStemmer()
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'([\w\-\<\>]+)')
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def process(self, text):
        terms = []
        text = self.regex_money.sub('<money>', text)  # we first have to search for money instead of number
        text = self.regex_number.sub('<number>', text)
        words = self.tokenizer.tokenize(text)
        for word in words:
            term = word.lower()
            term = self.stemmer.stem(term)
            if term not in self.stopwords:
                terms.append(term)
        return terms


