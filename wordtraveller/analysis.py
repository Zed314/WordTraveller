import re
import nltk
import filemanager

from lxml import etree
from filemanager import FileManager
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

def savePartialVocabulary(voc,workspace, number):
     #map vocabulary offset
    vocabulary = SortedDict()
    currentOffset = 0
    #save all the posting lists
    for word, pl in voc.items():
        filemanager.savePostList(pl, currentOffset, workspace, "partialPL"+str(number)+".temp")
        vocabulary[word] = currentOffset
        currentOffset += len(pl)
    #save the vocabulary
    filemanager.saveVocabulary(vocabulary, workspace,"partialVOC"+str(number)+".temp")
    print("Vocabulary saved")

def saveVocabulary(voc, filename, workspace):


    #map vocabulary offset
    vocabulary = SortedDict()
    currentOffset = 0
    #save all the posting lists
    #TODO make a btter call to the consturctore "filemanager.FileManager(..,..) seems a bit wirde
    fileManager = filemanager.FileManager(filename,workspace)

    for word, pl in voc.items():
        currentOffset += len(pl)
        vocabulary[word] = currentOffset

    #saving the plsting lists
    fileManager.save_postLists_file(voc)
    #save the vocabulary
    filemanager.saveVocabulary(vocabulary, workspace)
    print("Vocabulary saved")



if __name__ == "__main__":
    voc = SortedDict()
    # todo : add parametrization from command line to choose which folder we shoud parse
    pathlist = Path("data/latimesMini/").glob('**/la*')
    namePartialVoc=[]
    namePartialPL=[]
    i = 1
    for path in pathlist:
   #     analyseNewspaper(path, voc)
   #     savePartialVocabulary(voc,"./workspace/", i)
  #      voc = SortedDict()
       # #saveVocabulary(voc, './workspace/', "partialVOC"+str(i)+".temp","partialPL"+str(i)+".temp")
   #     print("file "+ str(i) + " finished!")
    #    namePartialPL.append("partialPL"+str(i)+".temp")
     #   namePartialVoc.append("partialVOC"+str(i)+".temp")
        i = i+1
    filemanager = FileManager("partialTest")
    filemanager.mergePartialVocsAndPL(namePartialVoc,namePartialPL)
    #saveVocabulary(voc, './workspace/')
    saveVocabulary(voc, 'test1', './workspace/')
