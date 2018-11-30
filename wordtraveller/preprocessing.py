import re
import tempfile

import nltk


class Preprocessor:
    """ Class that handle the preprocessing steps of the indexation """

    def __init__(self, activate_stemmer=False):
        """ Create the object and the regexes. Initialize the stemmer.
        Preconditions :
            activate_stemmer : boolean to activate or disactivate the stemming
        """
        nltk.download('stopwords', download_dir=tempfile.gettempdir())
        nltk.data.path.append(tempfile.gettempdir())
        self.regex_money = re.compile(
            r'(\$€¥)\d+((\.\d+)?(\s(million|billion))?)?')
        self.regex_number = re.compile(r'\d+((\.\d+)?(\s(million|billion))?)?')
        self.stemmer = None
        if activate_stemmer:
            self.stemmer = nltk.stem.PorterStemmer()
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'([\w\-\<\>]+)')
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def process(self, text):
        """ Apply the regexes, and put the word in lower case. If requested, apply the stemmer """
        terms = []
        # we first have to search for money instead of number
        text = self.regex_money.sub('<money>', text)
        text = self.regex_number.sub('<number>', text)
        words = self.tokenizer.tokenize(text)
        for word in words:
            term = word.lower()
            if self.stemmer is not None:
                term = self.stemmer.stem(term)
            if term not in self.stopwords:
                terms.append(term)
        return terms
