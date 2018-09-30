
import re
from lxml import etree
from nltk import tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from pathlib import Path

from pathlib import Path

def analyseNewspaper(path):

    contents = path.read_text()
    ps = PorterStemmer()    
    tree = etree.fromstring("<NEWSPAPER>"+contents+"</NEWSPAPER>")
    article = ""
    regexMoney = re.compile(r"(\$|€|¥)\d+((\.\d+)?(\s(million|billion))?)?")
    regexNumber = re.compile(r"\d+((\.\d+)?(\s(million|billion))?)?")
    for text in tree.xpath("//DOC/TEXT"):
        article = ""
        for p in text.xpath("./P"):
            article += p.text
        article = re.sub(regexMoney, "<money>", article)
        article = re.sub(regexNumber,"<number>",article)

        tokenizer = RegexpTokenizer(r'([\w\-\<\>]+)')
        listofwords = tokenizer.tokenize(article)
        for i,word in enumerate(listofwords):
            listofwords[i] = ps.stem(word)
        print(listofwords)


pathlist = Path("latimes/").glob('**/la*')

for path in pathlist:
    analyseNewspaper(path)