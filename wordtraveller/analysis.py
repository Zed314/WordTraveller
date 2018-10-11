import re
import nltk
import filemanager

from lxml import etree
from pathlib import Path
from nltk import tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sortedcontainers import SortedDict

nltk.download('stopwords')

REGEX_MONEY = re.compile(r"(\$|€|¥)\d+((\.\d+)?(\s(million|billion))?)?")
REGEX_NUMBER = re.compile(r"\d+((\.\d+)?(\s(million|billion))?)?")
ps = PorterStemmer()

def analyseNewspaper(path, voc):

    global REGEX_MONEY
    global REGEX_NUMBER
    global ps # PorterStemmer

    rawContent = path.read_text()
    tree = etree.fromstring("<NEWSPAPER>"+rawContent+"</NEWSPAPER>")
    text = ""
    stop_words = [word.lower() for word in set(stopwords.words('english')) ]
    for document in tree.xpath("//DOC"):
        text = ""
        vocDoc = {}
        idDocument = int(document.xpath("./DOCID")[0].text)
        # numDocument = document.xpath("./DOCNO")[0].text
        for p in document.xpath("./TEXT/P"):
            text += p.text
        text = re.sub(REGEX_MONEY, "<money>", text)
        text = re.sub(REGEX_NUMBER,"<number>", text)
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
        for word, occurencies in vocDoc.items():
            if word in voc:
                voc[word][idDocument] = occurencies
            else:
                voc[word] = {}
                voc[word][idDocument] = occurencies


#def writeToFolder(pathFolder):
 #   if not os.path.isdir(pathFolder):
  #      os.makedirs(pathFolder)
def saveVocabulary(voc, workspace, path):
    #map vocabulary offset
    vocabulary = SortedDict()
    currentOffset = 0
    #save all the posting lists
    fileManager = filemanager.FileManager(path,workspace )

    for word, pl in voc.items():
        currentOffset += len(pl)
        vocabulary[word] = currentOffset

    #saving the plsting lists     
    fileManager.save_postLists_file(voc)
    print("postingLists saved")
    #save the vocabulary
    fileManager.save_vocabulary(vocabulary)
    print("Vocabulary saved")
    pass

if __name__ == "__main__":
    voc = SortedDict()
    # todo : add parametrization from command line to choose which folder we shoud parse
    pathlist = Path("../data/latimesMini/").glob('**/la*')
    i = 1
    for path in pathlist:
        analyseNewspaper(path,voc)
        print("file "+ str(i) + " finished!")
        i = i+1

    saveVocabulary(voc, '../workspace/',"test1" )
