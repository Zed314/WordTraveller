
import re
from lxml import etree
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
from pathlib import Path

contents = Path("latimes/la010189").read_text()

tree = etree.fromstring("<NEWSPAPER>"+contents+"</NEWSPAPER>")
analyseText = ""
for text in tree.xpath("//TEXT/P"):
    analyseText +=text.text
#print(analyseText)
analyseText = re.sub(r"\$\d+((\.\d+)?(\s(million|billion))?)?","<money>",analyseText)

#analyseText = re.sub(r"(\d+\.\d+)+","<decimal>",analyseText)
#analyseText = re.sub(r"(\d)+","<number>",analyseText)
tokenizer = RegexpTokenizer(r'(?:[\w\-](?<!_))+')
tokenizer = RegexpTokenizer(r'([\w\-\<\>]+)')
print(tokenizer.tokenize(analyseText))