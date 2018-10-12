from . import filemanager
from . import preprocessing

from lxml import etree
from pathlib import Path
from sortedcontainers import SortedDict


def analyse_newspaper(path, voc):

    raw = path.read_text()
    tree = etree.fromstring("<NEWSPAPER>" + raw + "</NEWSPAPER>")

    for document in tree.xpath("//DOC"):

        text = ""
        for p in document.xpath("./TEXT/P"):
            text += p.text

        voc_doc = {}
        id_doc = int(document.xpath("./DOCID")[0].text)
        # numDocument = document.xpath("./DOCNO")[0].text

        preprocessor = preprocessing.Preprocessor()
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
                voc[term] = {}
                voc[term][id_doc] = occurrences


def save_vocabulary(voc, filename, workspace):
    # map vocabulary offset
    vocabulary = SortedDict()
    current_offset = 0
    # save all the posting lists
    # TODO make a btter call to the consturctore "filemanager.FileManager(..,..) seems a bit wirde
    file_manager = filemanager.FileManager(filename, workspace)

    for word, pl in voc.items():
        current_offset += len(pl)
        vocabulary[word] = current_offset

    # saving the plsting lists
    file_manager.save_postLists_file(voc)
    # save the vocabulary
    file_manager.save_vocabulary(vocabulary)


if __name__ == "__main__":
    # todo : add parametrization from command line to choose which folder we shoud parse

    pathlist = Path("./data/latimesMini/").glob('**/la*')

    vocabulary = SortedDict()
    for i, newspaper_path in enumerate(pathlist):
        analyse_newspaper(newspaper_path, vocabulary)
        print('file %s finished!' % i)

    save_vocabulary(vocabulary, 'test1', './workspace/')
