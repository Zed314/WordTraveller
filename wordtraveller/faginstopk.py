import operator
from . import query, analysis
from . import filemanager as fm
from sortedcontainers import SortedDict
from pathlib import Path

def createMockPL(filemanager):
    pathlist = Path("./tests/data/test1/").glob('**/la*')

    vocabulary = SortedDict()
    for i, newspaper_path in enumerate(pathlist):
        if i<4:
            analysis.analyse_newspaper(newspaper_path, vocabulary)
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = SortedDict()
            print('file %s finished!' % i)
    filemanager.mergePartialVocsAndPL()

if __name__ == "__main__" :
    filemanager = fm.FileManager("testalex", './workspace/alex/')
    # createMockPL(filemanager)

    savedVoc = filemanager.read_vocabulary()
    
    for i,voc in enumerate(savedVoc):
        print(voc)

    posting_lists = query.get_posting_list(voc, 'aa', filemanager)
    print(posting_lists)

