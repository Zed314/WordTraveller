
import re
import nltk
from . import filemanager as fm
from . import preprocessing
import math

from lxml import etree
from pathlib import Path
from sortedcontainers import SortedDict

preprocessor = preprocessing.Preprocessor()

def analyse_newspaper(path, voc, computeIDF = False):

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
if __name__ == "__main__":

    pathlist = Path("./data/latimesMini/").glob('**/la*')

    vocabulary = SortedDict()
    filemanager = fm.FileManager("test2")
    for i, newspaper_path in enumerate(pathlist):
        if i<2:
            analyse_newspaper(newspaper_path, vocabulary,True)
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = SortedDict()
            print('file %s finished!' % i)
    filemanager.mergePartialVocsAndPL()

