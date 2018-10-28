
import re
import nltk
from . import filemanager as fm
from . import preprocessing
import math
import time


from lxml import etree
from pathlib import Path
from sortedcontainers import SortedDict

preprocessor = preprocessing.Preprocessor()


def analyse_newspaper(path, voc, computeIDF = False):
    analyse_newspaper_optimized(path, voc, computeIDF)

def analyse_newspaper_naive(path, voc, computeIDF = False):

    raw = path.read_text()
    tree = etree.fromstring("<NEWSPAPER>" + raw + "</NEWSPAPER>")

    for document in tree.xpath("//DOC"):

        text = ""

        for p in document.xpath("./TEXT/P"):
            text += p.text

        voc_doc = {}
        id_doc = int(document.xpath("./DOCID")[0].text)
        terms = preprocessor.process(text)
       
        terms.append("***NumberDifferentDocs***")
        for term in terms:
            if term in voc_doc:
                voc_doc[term] = voc_doc[term] + 1
            else:
                voc_doc[term] = 1

        for term, occurrences in voc_doc.items():
            if term in voc:
                voc[term][id_doc] = [0, occurrences]
            else:
                voc[term] = SortedDict()
                voc[term][id_doc] = [0, occurrences]
    if computeIDF:
        nbDiffDocs = len(voc["***NumberDifferentDocs***"])
        for term, pl in voc.items():
            
            nbDocsWithWord = len(voc[term])
            for idfAndScore in pl.values():

                idfAndScore[0]=(1+math.log(idfAndScore[1]))*math.log(nbDiffDocs/(1+nbDocsWithWord))

def analyse_newspaper_optimized(path, voc, computeIDF = False):

    file = open(path, "r")
    currDocId = 0
    isInText = False
    isInParagraph = False

    documentText = ""
    for line in file:
        if line.startswith("<DOCID>"):
            currDocId = int(line[len("<DOCID> "):-len(" </DOCID>\n")])
        elif line.startswith("</DOC>"):
             #We use the data we accumulate during the process
            voc_doc = {}
            terms = preprocessor.process(documentText)
            terms.append("***NumberDifferentDocs***")
            for term in terms:
                if term in voc_doc:
                    voc_doc[term] = voc_doc[term] + 1
                else:
                    voc_doc[term] = 1

            for term, occurrences in voc_doc.items():
                if term in voc:
                    voc[term][currDocId] = [0, occurrences]
                else:
                    voc[term] = SortedDict()
                    voc[term][currDocId] = [0, occurrences]
            documentText = ""
        elif line.startswith("<TEXT>"):
            isInText = True
        elif line.startswith("</TEXT>"):
            isInText = False
        elif line.startswith("<P>") and isInText:
            isInParagraph = True
        elif line.startswith("</P>") and isInText:
            isInParagraph = False
        elif line.startswith("<"):
            pass
        elif isInText and isInParagraph:
            documentText += line             

    if computeIDF:
        nbDiffDocs = len(voc["***NumberDifferentDocs***"])
        for term, pl in voc.items():
            nbDocsWithWord = len(voc[term])
            for idfAndScore in pl.values():
                idfAndScore[0]=(1+math.log(idfAndScore[1]))*math.log(nbDiffDocs/(1+nbDocsWithWord))
    file.close()



if __name__ == "__main__":

    pathlist = Path("./data/latimesMini/").glob('**/la*')

    vocabulary = SortedDict()
    filemanager = fm.FileManager("test2")
    start = time.time()



    for i, newspaper_path in enumerate(pathlist):
        if i<4:
            analyse_newspaper(newspaper_path, vocabulary,True)
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = SortedDict()
            print('file %s finished!' % i)
    end = time.time()
    print(end - start)
    start = time.time()
    filemanager.mergePartialVocsAndPL()
    end = time.time()
    print(end - start)

