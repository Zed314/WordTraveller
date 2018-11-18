
import re
import nltk
import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing
import math
import time


from lxml import etree
from pathlib import Path
from sortedcontainers import SortedDict

preprocessor = preprocessing.Preprocessor()

def setPreprocessor(preprocessorToSet):
    global preprocessor
    preprocessor = preprocessorToSet


def analyse_newspaper(path, voc, randomIndexing=None, computeIDF=False, nbDocToStart = 0, nbDocToScan = -1):
    return analyse_newspaper_optimized(path, voc, randomIndexing, computeIDF, nbDocToStart, nbDocToScan)


def analyse_newspaper_naive(path, voc, randIndexing=None, computeIDF=False, nbDocToStart = 0, nbDocToScan = -1):

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

        # Random Indexing
        if randIndexing is not None:
            randIndexing.setDocumentVector(id_doc)

        for term in terms:
            if term in voc_doc:
                voc_doc[term] = voc_doc[term] + 1
            else:
                voc_doc[term] = 1
            if randIndexing is not None:
                randIndexing.addTermVector(term, id_doc)

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

                idfAndScore[0] = (1+math.log(idfAndScore[1])) * \
                    math.log(nbDiffDocs/(1+nbDocsWithWord))


def analyse_newspaper_optimized(path, voc, randIndexing= None, computeIDF=False, nbDocToStart = 0, nbDocToScan = -1):

    """ Voc is a dictionnary of word and pl (that are also dictionnaries)
    
    Returns the number of docs that were scanned."""
    file = open(path, "r")
    currDocId = 0
    isInText = False
    isInParagraph = False
    currDoc = 0
    nbDocScanned = 0
    documentText = ""
    if type(voc) is dict:
        # print ("voc is a dict")
        pass
    else:
        print("voc is NOT a dict !")
    for line in file:
        if line.startswith("<DOCID>"):
            currDocId = int(line[len("<DOCID> "):-len(" </DOCID>\n")])
        elif line.startswith("</DOC>"):
            # We use the data we accumulate during the process
            if nbDocToStart > currDoc:
                voc_doc = {}
                documentText = ""
                currDoc += 1
                continue
            if nbDocToScan == currDoc:
                break
            voc_doc = {}
            terms = preprocessor.process(documentText)
            terms.append("***NumberDifferentDocs***")

            if randIndexing is not None:
                randIndexing.setDocumentVector(currDocId)
            for term in terms:
                if term in voc_doc:
                    voc_doc[term] = voc_doc[term] + 1
                else:
                    voc_doc[term] = 1
                if randIndexing is not None:
                    randIndexing.addTermVector(term, currDocId)

            for term, occurrences in voc_doc.items():
                if term in voc:
                    voc[term][currDocId] = [0, occurrences]
                else:
                    voc[term] = dict()
                    voc[term][currDocId] = [0, occurrences]
            documentText = ""
            currDoc += 1
            nbDocScanned += 1
            if nbDocScanned == nbDocToScan and nbDocToScan !=-1:
                break
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
            if nbDocToStart > currDoc:
                continue
            documentText += line

    if computeIDF:
        nbDiffDocs = len(voc["***NumberDifferentDocs***"])
        for term, pl in voc.items():
            if term == "***NumberDifferentDocs***":
                continue
            nbDocsWithWord = len(voc[term])
            for idfAndScore in pl.values():
                idfAndScore[0] = (1+math.log(idfAndScore[1])) * \
                    math.log(nbDiffDocs/(1+nbDocsWithWord))
    file.close()

    return nbDocScanned


