
import re
import nltk
import filemanager
import preprocessing

from lxml import etree
from filemanager import FileManager
from pathlib import Path
from sortedcontainers import SortedDict

preprocessor = preprocessing.Preprocessor()

def analyse_newspaper(path, voc):

    raw = path.read_text()
    tree = etree.fromstring("<NEWSPAPER>" + raw + "</NEWSPAPER>")

    for document in tree.xpath("//DOC"):

        text = ""

        for p in document.xpath("./TEXT/P"):
            text += p.text

        voc_doc = {}
        id_doc = int(document.xpath("./DOCID")[0].text)
        terms = preprocessor.process(text)

        for term in terms:
            if term in voc_doc:
                voc_doc[term] = voc_doc[term] + 1
            else:
                voc_doc[term] = 1

        for term, occurrences in voc_doc.items():
            if term in voc:
                voc[term][id_doc] = occurrences
            else:
                voc[term] = SortedDict()
                voc[term][id_doc] = occurrences

#DEPRECATED, moved to filemanager, use save_vocabularyAndPL_file
#Save a memory vocabulary that contains both voc and PLs to disk using
#textual and binary format
def save_vocabulary(voc, filename, workspace):
    # map vocabulary offset
    vocabulary = SortedDict()
    current_offset = 0
    # save all the posting lists
    # TODO make a btter call to the consturctore "filemanager.FileManager(..,..) seems a bit wirde
    file_manager = FileManager(filename, workspace)

    for word, pl in voc.items():
        current_offset += len(pl)
        vocabulary[word] = current_offset

    # saving the plsting lists
    file_manager.save_postLists_file(voc)
    # save the vocabulary
    file_manager.save_vocabulary(vocabulary)



if __name__ == "__main__":

    pathlist = Path("./data/latimesMini/").glob('**/la*')

    vocabulary = SortedDict()
    filemanager = FileManager("test1")
    for i, newspaper_path in enumerate(pathlist):
        if i<1:
            analyse_newspaper(newspaper_path, vocabulary)
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = SortedDict()
            print('file %s finished!' % i)
    filemanager.mergePartialVocsAndPL()
    #save_vocabulary(vocabulary,"test1","workspace/")
    #filemanager.save_vocabularyAndPL_file(vocabulary, True)
