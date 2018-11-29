
import math
import re
import time
import numpy
from pathlib import Path
from threading import Thread

import nltk
from lxml import etree
from sortedcontainers import SortedDict

import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing

preprocessor = preprocessing.Preprocessor()


class AnalyseThread(Thread):
    def __init__(self, function, chunkpath, voc, randIndexing=None, computeIDF=False, nbDocToStart=0, nbDocToScan=-1):
        Thread.__init__(self)
        self.function = function
        self.chunkpath = chunkpath
        self.voc = voc
        self.randIndexing = randIndexing
        self.computeIDF = computeIDF
        self.nbDocToStart = nbDocToStart
        self.nbDocToScan = nbDocToScan

        self.res = 1

    def run(self):
        resTotal = 0
        for path in self.chunkpath:
            resTotal += self.function(path, self.voc, self.randIndexing,
                                      self.computeIDF, self.nbDocToStart, self.nbDocToScan)
            print(path)
        self.res = resTotal


def setPreprocessor(preprocessorToSet):
    global preprocessor
    preprocessor = preprocessorToSet


def analyse_newspaper(path, voc, randomIndexing=None, computeIDF=False, nbDocToStart=0, nbDocToScan=-1):
    #return analyse_newspaper_optimized(path, voc, randomIndexing, computeIDF, nbDocToStart, nbDocToScan)
    if randomIndexing is not None :
          analyse_newspaper_optimized(path, voc, randomIndexing, computeIDF, nbDocToStart, nbDocToScan)

    if isinstance(path, list):
         return analyse_newspaper_multithread(path, voc, randomIndexing, computeIDF, nbDocToStart, nbDocToScan)
    else :
         return analyse_newspaper_optimized(path, voc, randomIndexing, computeIDF, nbDocToStart, nbDocToScan)


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


def analyse_newspaper_multithread(paths, voc, randIndexing=None, computeIDF=False, nbDocToStart=0, nbDocToScan=-1):
    if type(voc) is dict:
        pass
    else:
        print("ERROR")
    nbThread = 4
  #  vocs = [dict() for x in range(nbThread)]
    vocs = []
 #   pathsDivided = chunks(paths, nbThread)
    threads = []
    res = 0
   # voc = dict()
    chunksPaths = chunks(paths, 4)
    for chunkPath in chunksPaths:

        newDict = dict()
        thread = AnalyseThread(analyse_newspaper_optimized, chunkPath,
                               newDict, randIndexing, False, nbDocToStart, nbDocToScan)
        threads.append(thread)
        thread.start()
       # vocs.append(newDict)

    #thread = AnalyseThread(analyse_newspaper_optimized,path,voc, randIndexing, computeIDF, nbDocToStart, nbDocToScan)
    for thread in threads:
        thread.join()
        res += thread.res
        vocs.append(thread.voc)

    for vocToMerge in vocs:
        for word in vocToMerge:
            if word in voc:
                voc[word].update(vocToMerge[word])
            else:
                voc[word] = vocToMerge[word]
    if computeIDF:
        nbDiffDocs = len(voc["***NumberDifferentDocs***"])
        for term, pl in voc.items():
            nbDocsWithWord = len(pl)
            for idfAndScore in pl.values():
                idfAndScore[0] = (1+math.log(idfAndScore[1])) * \
                    math.log(nbDiffDocs/(1+nbDocsWithWord))

    return res

def computeIDF(voc):
    nbDiffDocs = len(voc["***NumberDifferentDocs***"])
    for term, pl in voc.items():
        nbDocsWithWord = len(pl)
        if term == "***NumberDifferentDocs***":
                continue
        for idfAndScore in pl.values():
            idfAndScore[0] = (1+numpy.log(idfAndScore[1])) * \
                numpy.log(nbDiffDocs/(1+nbDocsWithWord))

def analyse_newspaper_naive(path, voc, randIndexing=None, computeIDF=False, nbDocToStart=0, nbDocToScan=-1):

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
            if term == "***NumberDifferentDocs***":
                continue
            nbDocsWithWord = len(voc[term])
            for idfAndScore in pl.values():

                idfAndScore[0] = (1+math.log(idfAndScore[1])) * \
                    math.log(nbDiffDocs/(1+nbDocsWithWord))


def analyse_newspaper_optimized(path, voc, randIndexing=None, computeIDF=False, nbDocToStart=0, nbDocToScan=-1):
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
            if nbDocScanned == nbDocToScan and nbDocToScan != -1:
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
            nbDocsWithWord = len(voc[term])
            for idfAndScore in pl.values():
                idfAndScore[0] = (1+math.log(idfAndScore[1])) * \
                    math.log(nbDiffDocs/(1+nbDocsWithWord))
    file.close()

    return nbDocScanned
