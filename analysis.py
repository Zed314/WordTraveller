
import re
from lxml import etree
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
from pathlib import Path

contents = Path("latimes/la010189").read_text()

tree = etree.fromstring("<NEWSPAPER>"+contents+"</NEWSPAPER>")
analyseText = ""
regexMoney = re.compile(r"(\$|€|¥)\d+((\.\d+)?(\s(million|billion))?)?")
regexNumber = re.compile(r"\d+((\.\d+)?(\s(million|billion))?)?")
for text in tree.xpath("//DOC/TEXT"):
    analyseText = ""
    for p in text.xpath("./P"):
        analyseText += p.text
    analyseText = re.sub(regexMoney, "<money>", analyseText)
    analyseText = re.sub(regexNumber,"<number>",analyseText)
  
    tokenizer = RegexpTokenizer(r'([\w\-\<\>]+)')
    print(tokenizer.tokenize(analyseText))
