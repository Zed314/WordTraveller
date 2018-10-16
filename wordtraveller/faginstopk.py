import operator
from . import query, analysis
from . import filemanager as fm
from sortedcontainers import SortedDict
from pathlib import Path

def createMockData(ownfilemanager):
    voc = SortedDict()

    pathlist = Path("./tests/data/test1/").glob('**/la*')
    for path in pathlist:
        analysis.analyse_newspaper(path, voc)
    ownfilemanager.save_vocabularyAndPL_file(voc)

if __name__ == "__main__" :
    currentWorkspace = './tests/workspace/test1/'
    filename = 'test1'
    filemanag = fm.FileManager(filename, currentWorkspace)
    createMockData(filemanag)

    savedVoc = filemanag.read_vocabulary()

    mot1 = query.get_posting_list(savedVoc,"aa", filemanag)
    mot2 = query.get_posting_list(savedVoc,"bb", filemanag)
    mot3 = query.get_posting_list(savedVoc,"cc", filemanag)
    print(mot1)
    print(mot2)
    print(mot3)
    # filemanager = fm.FileManager("testalex", './workspace/alex/')
    # createMockPL(filemanager)

    # savedVoc = filemanager.read_vocabulary()
    
    # for i,voc in enumerate(savedVoc):
    #     print(voc)

    # posting_lists = query.get_posting_list(voc, 'cc', filemanager)
    # print(posting_lists)

