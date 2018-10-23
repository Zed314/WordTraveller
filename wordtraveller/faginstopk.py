import operator
from . import query, analysis
from . import filemanager as fm
from sortedcontainers import SortedDict
from pathlib import Path

# Vu que les int ne peuvent pas se modifier par reference, j'ai du creer une variable global
# Cette variable me sers pour apres savoir si les scores qui restent dans m sont plus grandes que celles déjà existantes
last_score_of_c = 0


def createMockData(ownfilemanager):
    voc = SortedDict()

    pathlist = Path("./tests/data/test1/").glob('**/la*')
    for path in pathlist:
        analysis.analyse_newspaper(path, voc)
    ownfilemanager.save_vocabularyAndPL_file(voc)


def mean(values):
    sumValues = sum(values)
    return sumValues/len(values)


def push_to_m(m, c, docId, score, nb_of_PL):
    global last_score_of_c
    if(docId in m):
        # print('[{}],[{}],[{}],[{}]'.format(m[docId],nb_of_PL,len(m[docId]),docId))
        m[docId] += [score]
        if(len(m[docId]) == nb_of_PL):
            mean_score = mean(m[docId])
            # print('calculMean: {}|{}|{}'.format(docId,m[docId],mean_score))
            c[docId] = mean_score
            last_score_of_c = mean_score
            del m[docId]
    else:
        m[docId] = [score]
    print('c: {} || m: {}'.format(c, m))


def add_next_score(score, idsDoc, pl_id, currentScores):
    for idDoc in idsDoc:
        if(score not in currentScores):
            currentScores[score] = dict()
        # on met en dernier [idDoc, idPostingList]
        currentScores[score][len(currentScores[score])] = [idDoc, pl_id]


def get_score_by_doc_id(doc_id, postingListsOrderedById, aggregation_function):
    score = 0
    all_scores = []
    for posting_list in postingListsOrderedById:
        score_doc_id = postingListsOrderedById[posting_list][doc_id]
        all_scores.append(score_doc_id)
    score = aggregation_function(all_scores)
    return score

def fagins_top_k_algo(words, voc, filemanager, k):
    pl1_score = dict()
    pl1_score[0.90] = [2]
    # pl1_score[0.90] += [3]
    pl1_score[0.80] = [5]
    pl1_score[0.70] = [6]
    pl1_score[0.60] = [4]
    pl1_score[0.50] = [1]
    pl1_score[0.40] = [3]

    pl2_score = dict()
    pl2_score[0.85] = [3]
    pl2_score[0.80] = [5]
    pl2_score[0.75] = [2]
    pl2_score[0.74] = [6]
    pl2_score[0.74] += [1]
    pl2_score[0.70] = [4]

    postingListsOrderedByScore = dict()
    postingListsOrderedByScore['aaa'] = pl1_score
    postingListsOrderedByScore['bbb'] = pl2_score
    print('postingListsOrderedByScore: {}'.format(postingListsOrderedByScore))

    pl1_id = dict()
    pl1_id[3] = 0.40
    pl1_id[1] = 0.50

    pl2_id = dict()
    pl2_id[3] = 0.85
    pl2_id[1] = 0.74

    postingListsOrderedById = dict()
    postingListsOrderedById['aaa'] = pl1_id
    postingListsOrderedById['bbb'] = pl2_id
    # postingListsOrderedById = [pl1_id,pl2_id]

    # Algo commence ici
    global last_score_of_c
    iterators = dict()
    currentScores = SortedDict()
    # posting_list_id sera le terme du posting_list
    for posting_list_id in postingListsOrderedByScore:
        print("POST:{}".format(postingListsOrderedByScore[posting_list_id]))
        iterators[posting_list_id] = iter(
            postingListsOrderedByScore[posting_list_id])
        # next donne la clé
        score = next(iterators[posting_list_id])
        idsDoc = postingListsOrderedByScore[posting_list_id][score]
        # On initialise la structure de donnees du score
        add_next_score(score, idsDoc, posting_list_id, currentScores)

    c = dict()
    m = dict()
    while len(c) < k:
        print("Current {}".format(currentScores))
        item = currentScores.popitem()
        score = item[0]
        postingListId = item[1][0][1]
        docId = item[1][0][0]
        push_to_m(m, c, docId, score, len(postingListsOrderedByScore))
        if(len(item[1]) > 1):
            for i, doc in enumerate(item[1]):
                used_docId = item[1][doc][0]
                pl_id = item[1][doc][1]
                # print("EXNUMerate: {},{}".format(i,value_from_list))
                if(docId == used_docId and pl_id == postingListId):
                    pass
                else:
                    if score not in currentScores:
                        currentScores[score] = dict()
                    currentScores[score][len(currentScores[score])] = [
                        used_docId, pl_id]

        # getting next new score
        try:
            newScore = next(iterators[postingListId])
            # print("Score:", newScore)
            idsDoc = postingListsOrderedByScore[postingListId][newScore]
            # print('idsDoc:{}'.format(idsDoc))
            add_next_score(newScore, idsDoc, postingListId, currentScores)
        except StopIteration:
            print("No more values in postingLists")

    print("last_  {}".format(last_score_of_c))
    for doc_id in m:
        score = get_score_by_doc_id(doc_id, postingListsOrderedById, mean)
        if(score > last_score_of_c):
            c.popitem()
            c[doc_id] = score
            last_score_of_c = score
    print('final top {} : {}'.format(k,c))
    return c


if __name__ == "__main__":
    currentWorkspace = './tests/workspace/test1/'
    filename = 'test1'
    filemanag = fm.FileManager(filename, currentWorkspace)
    createMockData(filemanag)

    savedVoc = filemanag.read_vocabulary()

    top_k = fagins_top_k_algo(["aa", "bb"], savedVoc, filemanag, 3)
    
    # mot1 = query.get_posting_list(savedVoc,"aa", filemanag)
    # mot2 = query.get_posting_list(savedVoc,"bb", filemanag)
    # mot3 = query.get_posting_list(savedVoc,"cc", filemanag)
    # print(mot1)
    # print(mot2)
    # print(mot3)
