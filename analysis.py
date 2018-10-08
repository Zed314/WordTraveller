import re
import nltk
import fileManager

from lxml import etree
from pathlib import Path
from nltk import tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sortedcontainers import SortedDict




def downloadNLTKDependencies():
    nltk.download('stopwords')

def analyseNewspaper(path, voc):

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
        idDocument = int(document.xpath("./DOCID")[0].text)
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
                voc[word][idDocument] = occ #occurencies
            else:
                voc[word] = {}
                voc[word][idDocument] = occ #occurencies


#def writeToFolder(pathFolder):
 #   if not os.path.isdir(pathFolder):
  #      os.makedirs(pathFolder)
def save(voc):
    #map vocabulary offste
    vocabulary = SortedDict()
    CurrantOffset=0
    #save all the posting lists
    for word, pl in voc.items():
        fileManager.savePostList(pl, CurrantOffset)
        vocabulary[word] = CurrantOffset
        CurrantOffset += len(pl)
    #save the vocabulary
    fileManager.saveVocabulary(vocabulary)
    pass

if __name__ == "__main__":
    voc = SortedDict()
    # todo : add parametrization from command line to choose which folder we shoud parse
    pathlist = Path("data/latimesMini/").glob('**/la*')
    downloadNLTKDependencies()
    i = 1
    for path in pathlist:
        analyseNewspaper(path,voc)
        print("file "+ str(i) + " finished!")
        i = i+1


    #save(voc)
