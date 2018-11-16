import wordtraveller.preprocessing as preprocessing
from sortedcontainers import SortedDict
import numpy as np
from pathlib import Path

preprocessor = preprocessing.Preprocessor()

def randomIndexing(path, nbDocToStart = 0, nbDocToScan = -1):
    # if(not path.endswith('/')):
    #     path = path + '/'
    DOCUMENT_DIMENSION = 20
    TERM_DIMENSION = DOCUMENT_DIMENSION

    file = open(path, "r")
    
    voc = SortedDict()
    
    currentDocId = 0

    isInText = False
    isInParagraph = False
    # currDoc = 0
    nbDocScanned = 0
    documentText = ""
    documents = {}
    for line in file:
        if line.startswith("<DOCID>"):
            currentDocId = int(line[len("<DOCID> "):-len(" </DOCID>\n")])
            documents[currentDocId] = np.zeros((DOCUMENT_DIMENSION,), dtype=int)
            non_zeros = np.random.random_integers(3,8)
            for x in range(0, non_zeros):
                index = np.random.random_integers(DOCUMENT_DIMENSION-1,)
                if index%2:
                    documents[currentDocId][index] = -1
                else:
                    documents[currentDocId][index] = 1
            print("documents[{}] {}".format(currentDocId,documents[currentDocId]))

        elif line.startswith("</DOC>"):
            # We use the data we accumulate during the process
            # if nbDocToStart > currDoc:
            #     voc_doc = {}
            #     documentText = ""
            #     currDoc += 1
            #     continue
            # if nbDocToScan == currDoc:
            #     break
            voc_doc = {}
            terms = preprocessor.process(documentText)
            # terms.append("***NumberDifferentDocs***")
            for term in terms:
                if term in voc_doc:
                    voc_doc[term] = voc_doc[term] + documents[currentDocId]
                else:
                    voc_doc[term] = [0]*TERM_DIMENSION
                print("voc[{}]: {}".format(term,voc_doc[term]))
            # for term, occurrences in voc_doc.items():
            #     if term in voc:
            #         voc[term][currentDocId] = [0, occurrences]
            #     else:
            #         voc[term] = SortedDict()
            #         voc[term][currentDocId] = [0, occurrences]
            documentText = ""
            # currDoc += 1
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
            # if nbDocToStart > currDoc:
            #     continue
            documentText += line
    file.close()


if __name__ == "__main__":
    pathlist = Path('./tests/data/test4/').glob('**/la*')
    for path in pathlist:
        randomIndexing(path)

