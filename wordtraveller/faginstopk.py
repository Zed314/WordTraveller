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

def mergeAndOrderDict(dictionnaries):
    resList = SortedDict()
    for dictionnary in dictionnaries:
        for key, value in dictionnary.items():
            if(key in resList):
                resList[key] += value
            else:   
                resList[key] = [] + value
    return resList

def fagins_top_k_algo(words, voc, filemanager, k):
    # for word in words:
    #     postList = query.get_posting_list(voc, word, filemanager)
    #     print(postList)
    # posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    pl1 = dict()
    pl2 = dict()
    pl1[0.90] = [2]
    pl1[0.90] += [3]
    pl1[0.80] = [5]
    pl1[0.70] = [6]
    pl1[0.60] = [4]
    pl1[0.50] = [1]
    pl1[0.40] = [3]
    pl2[0.85] = [3]
    pl2[0.80] = [5]
    pl2[0.75] = [2]
    pl2[0.74] = [6]
    pl2[0.74] += [1]
    pl2[0.70] = [4]
    posting_lists = []
    posting_lists.append(pl1)
    posting_lists.append(pl2)
    dictlist = mergeAndOrderDict(posting_lists)
    
    postingListsOrderedByScore = [pl1,pl2]
    print(postingListsOrderedByScore)
    iterators = dict()
    currentScores = SortedDict()
    i = 0
    for postingList in postingListsOrderedByScore:
        iterators[i] = iter(postingList)
        score = next(iterators[i])
        idsDoc = postingList[score]

        currentScores[score] = dict()
        for idDoc in idsDoc:
            currentScores[score][len(currentScores[score])] = [idDoc, i]
        i += 1

    while True:
        pass
        # item = currentScores.popitem() # ça donne le dernier du sortedDict = +haut score
        # score = 
        # if(len(item) == 1) or item[0]:

    # print(currentScores)


if __name__ == "__main__" :
    currentWorkspace = './tests/workspace/test1/'
    filename = 'test1'
    filemanag = fm.FileManager(filename, currentWorkspace)
    createMockData(filemanag)

    savedVoc = filemanag.read_vocabulary()

    fagins_top_k_algo(["aa","bb"],savedVoc,filemanag,3)

    # mot1 = query.get_posting_list(savedVoc,"aa", filemanag)
    # mot2 = query.get_posting_list(savedVoc,"bb", filemanag)
    # mot3 = query.get_posting_list(savedVoc,"cc", filemanag)
    # print(mot1)
    # print(mot2)
    # print(mot3)
    