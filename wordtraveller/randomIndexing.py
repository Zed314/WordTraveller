import wordtraveller.preprocessing as preprocessing
from sortedcontainers import SortedDict
import numpy as np
from pathlib import Path

# TODO: pour saving to disk
import struct
import os


class RandomIndexing:
    DOCUMENT_DIMENSION = 15
    TERM_DIMENSION = DOCUMENT_DIMENSION
    NON_ZEROS_START = 3
    NON_ZEROS_END = 8
    ENCODING = ''

    preprocessor = preprocessing.Preprocessor()

    def __init__(self, preprocessorToSet):
        if(preprocessorToSet):
            self.preprocessor = preprocessorToSet
        self.documents = {}
        self.voc_doc = {}

    def setDimensions(self, doc_dim, term_dim, non_z_start, non_z_end):
        self.DOCUMENT_DIMENSION = doc_dim
        self.TERM_DIMENSION = term_dim
        self.NON_ZEROS_START = non_z_start
        self.NON_ZEROS_END = non_z_end

    def setDocumentVector(self, docId):
        self.documents[docId] = np.zeros((self.DOCUMENT_DIMENSION,), dtype=int)
        non_zeros = np.random.random_integers(self.NON_ZEROS_START, self.NON_ZEROS_END)
        for x in range(0, non_zeros):
            index = np.random.random_integers(self.DOCUMENT_DIMENSION-1,)
            if index % 2:
                self.documents[docId][index] = -1
            else:
                self.documents[docId][index] = 1
        print("documents[{}] {}".format(docId, self.documents[docId]))

    def addTermVector(self, term, docId):
        if term in self.voc_doc:
            self.voc_doc[term] = self.voc_doc[term] + self.documents[docId]
        else:
            self.voc_doc[term] = np.zeros((self.TERM_DIMENSION,), dtype=int)
        print("voc[{}]: {}".format(term, self.voc_doc[term]))

    def getTermsVectors(self):
        return self.voc_doc

def randomIndexing(path, documents, voc_doc, nbDocToStart=0, nbDocToScan=-1):

    global DOCUMENT_DIMENSION
    global TERM_DIMENSION
    global NON_ZEROS_START, NON_ZEROS_END

    file = open(path, "r")

    currentDocId = 0

    isInText = False
    isInParagraph = False
    nbDocScanned = 0
    documentText = ""
    for line in file:
        if line.startswith("<DOCID>"):
            currentDocId = int(line[len("<DOCID> "):-len(" </DOCID>\n")])
            documents[currentDocId] = np.zeros(
                (DOCUMENT_DIMENSION,), dtype=int)
            non_zeros = np.random.random_integers(
                NON_ZEROS_START, NON_ZEROS_END)
            for x in range(0, non_zeros):
                index = np.random.random_integers(DOCUMENT_DIMENSION-1,)
                if index % 2:
                    documents[currentDocId][index] = -1
                else:
                    documents[currentDocId][index] = 1
            print("documents[{}] {}".format(
                currentDocId, documents[currentDocId]))

        elif line.startswith("</DOC>"):
            terms = preprocessor.process(documentText)
            for term in terms:
                if term in voc_doc:
                    voc_doc[term] = voc_doc[term] + documents[currentDocId]
                else:
                    voc_doc[term] = np.zeros((TERM_DIMENSION,), dtype=int)
                print("voc[{}]: {}".format(term, voc_doc[term]))
            documentText = ""
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
            documentText += line
    file.close()


def saveSemantics(vocabulary, path_to_write):
    print("VOC: {}".format(vocabulary))

    if not os.path.exists(path_to_write):
        os.makedirs(path_to_write)
    # create the files
    if not os.path.isfile(self.getPathVoc()):
        file = open(self.getPathVoc(), "wb")
        file.close()
    if not os.path.isfile(self.getPathPL()):
        file = open(self.getPathPL(), "wb")
        file.close()
    file = open(path_to_write + 'termvect.vect', "w")
    for voc in vocabulary:
        file.write("{},{}\n".format(voc, vocabulary[voc]))
    file.close()
    # np_list = np.array([1,2,3,4,5,6,7,8,9,10])
    # buf = struct.pack('10i',*np_list)
    # uncoded = struct.unpack('10i',buf)

    pass


if __name__ == "__main__":
    pathlist = Path('./tests/data/test3/').glob('**/la*')
    documents = {}
    voc_doc = {}

    for path in pathlist:
        randomIndexing(path, documents, voc_doc)

    saveSemantics(voc_doc, './workspace/proves/')
