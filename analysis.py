import re
import nltk

from lxml import etree
from pathlib import Path
from nltk import tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

#Global scale voc (among all documents)
voc = dict()

def downloadNLTKDependencies():
    nltk.download('stopwords')

def analyseNewspaper(path):

    contents = path.read_text()
    ps = PorterStemmer()    
    tree = etree.fromstring("<NEWSPAPER>"+contents+"</NEWSPAPER>")
    text = ""
    regexMoney = re.compile(r"(\$|€|¥)\d+((\.\d+)?(\s(million|billion))?)?")
    regexNumber = re.compile(r"\d+((\.\d+)?(\s(million|billion))?)?")
    stop_words = [word.lower() for word in set(stopwords.words('english')) ]
    for document in tree.xpath("//DOC"):
        text = ""
        vocDoc = {}
        idDocument = document.xpath("./DOCID")[0].text
        numDocument = document.xpath("./DOCNO")[0].text
        for p in document.xpath("./TEXT/P"):
            text += p.text
        text = re.sub(regexMoney, "<money>", text)
        text = re.sub(regexNumber,"<number>", text)
        tokenizer = RegexpTokenizer(r'([\w\-\<\>]+)')
        listofwords = tokenizer.tokenize(text)
        for i,word in enumerate(listofwords):
            if word.lower() not in stop_words:
                word = ps.stem(word)
                word = word.lower()
                if word in vocDoc:
                    vocDoc[word] = vocDoc[word] + 1
                else:
                    vocDoc[word] = 1
        for word, occ in vocDoc.items():
            if word in voc:
                voc[word][numDocument] = occ #occurencies
            else:
                voc[word] = {}
                voc[word][numDocument] = occ #occurencies

 
#def writeToFolder(pathFolder):
 #   if not os.path.isdir(pathFolder):
  #      os.makedirs(pathFolder)


# todo : add parametrization from command line to choose which folder we shoud parse
pathlist = Path("data/latimesMini/").glob('**/la*')
downloadNLTKDependencies()
i = 1
for path in pathlist:
    analyseNewspaper(path)
    print("file "+ str(i) + " finished!")
    i = i+1
#print the aggregation
for word, pl in voc.items():
    print(word)
    for numDoc, score in pl.items():
        print("{} => {}.".format(numDoc, score))