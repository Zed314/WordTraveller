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

def mean(values):
    sumValues = sum(values)
    return sumValues/len(values)
        

def pushing_to_m(m,c,docId,score,nb_of_PL):
    if(docId in m):
        m[docId] += [score]
        if(len(m[docId])== nb_of_PL):
            mean_score = mean(m[docId])
            # print('calculMean: {}|{}|{}'.format(docId,m[docId],mean_score))
            c[docId] = mean_score
            del m[docId]
    else:
        m[docId] = [score]
    print('c: {} || m: {}'.format(c,m))

def add_next_score(score, idsDoc, pl_id, currentScores):
    for idDoc in idsDoc:
        if(score not in currentScores):
            currentScores[score] = dict()  
        # on met en dernier [idDoc, idPostingList] 
        currentScores[score][len(currentScores[score])] = [idDoc, pl_id]

def fagins_top_k_algo(words, voc, filemanager, k):
    pl1 = dict()
    pl2 = dict()
    pl1[0.90] = [2]
    # pl1[0.90] += [3]
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
    
    postingListsOrderedByScore = [pl1,pl2]
    print('postingListsOrderedByScore: {}'.format(postingListsOrderedByScore))
    iterators = dict()
    currentScores = SortedDict()
    i = 0
    for postingList in postingListsOrderedByScore:
        iterators[i] = iter(postingList)
        # next donne la clé
        score = next(iterators[i])
        idsDoc = postingList[score]
        # On initialise la structure de donnees du score
        add_next_score(score, idsDoc, i, currentScores)
        i += 1
    print("Current: {}".format(currentScores))

    c = dict()
    m = dict()
    while len(c) <= k:
        item = currentScores.popitem()
        score = item[0]
        postingListId = item[1][0][1]
        docId = item[1][0][0]

        pushing_to_m(m, c, docId, score, len(postingListsOrderedByScore))

        if(len(item[1]) > 1):
            currentScores[score] = dict()
            for i,doc in enumerate(item[1]):
                pl_id = item[1][doc][1]
                if(i>0):
                    currentScores[score][len(currentScores[score])] = [docId, pl_id]

        # getting next new score
        newScore = next(iterators[postingListId])
        print("Score:", newScore)
        #------------------------------------------------
        idsDoc = postingListsOrderedByScore[postingListId][newScore]
        # print(idsDoc)
        add_next_score(newScore, idsDoc, postingListId, currentScores)



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
    