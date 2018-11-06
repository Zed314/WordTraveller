from . import query, analysis
from . import filemanager as fm
from sortedcontainers import SortedDict
from pathlib import Path
import time

# Vu que les int ne peuvent pas se modifier par reference, j'ai du creer une variable globale
# Cette variable me sert pour apres savoir si les scores qui restent dans m sont plus grands que ceux déjà existants
last_score_of_c = 0


def apply_top_k_algo(words, voc, filemanager, k):

    posting_lists_ordered_by_id = SortedDict()
    posting_lists_ordered_by_score = SortedDict()
    for word in words:
        posting_lists_ordered_by_id[word], posting_lists_ordered_by_score[word] = query.get_posting_list(
        voc, word, filemanager, returnPostingListOrderedByScore = True)
    
    print('ww: {}'.format(posting_lists_ordered_by_id))
#    posting_lists_ordered_by_score = SortedDict()
    print('ww: {}'.format(posting_lists_ordered_by_score))

    # pl_aa = SortedDict()
    # pl_aa[3] = [1]
    # pl_aa[2] = [2]
    # pl_aa[1] = [3]
    # pl_bb = SortedDict()
    # pl_bb[1] = [1, 2]
    # pl_cc = SortedDict()
    # pl_cc[1] = [3]

    # posting_lists_ordered_by_score = dict()
    # posting_lists_ordered_by_score['aa'] = pl_aa
    # posting_lists_ordered_by_score['bb'] = pl_bb
    # posting_lists_ordered_by_score['cc'] = pl_cc

    return find_fagins_top_k(posting_lists_ordered_by_id,
                      posting_lists_ordered_by_score, k)


def aggregative_function_mean(values):
    """
    Preconditions:
        values: array of values (int or float).
    Postconditions:
        Returns the mean of this values.
    """
    sumValues = sum(values)
    if(len(values) == 0):
        return 0
    else:
        return sumValues/len(values)


def push_to_m(m, c, docId, score, nb_of_PL, aggregative_function):
    """
    Preconditions:
        m: dictionnary with the documents already seen.
        c: dictionnary with the documents already seen by all the posting lists.
        docId: document ID.
        score: score of this document in the posting list.
        nb_of_PL: number of posting lists used in the algorithm.
    Postconditions:
        The function save the tuple [docId,score] to m.
        If the tuple has been already seen by all the posting list apply 
        aggregation function to and save the result to c.
    """
    global last_score_of_c
    if(docId in m):
        # print('[{}],[{}],[{}],[{}]'.format(m[docId],nb_of_PL,len(m[docId]),docId))
        m[docId] += [score]
        if(len(m[docId]) == nb_of_PL):
            mean_score = aggregative_function(m[docId])
            # print('calculMean: {}|{}|{}'.format(docId,m[docId],mean_score))
            c[docId] = mean_score
            last_score_of_c = mean_score
            del m[docId]
    elif nb_of_PL == 1:
        m[docId] = [score]
        if(len(m[docId]) == nb_of_PL):
            mean_score = aggregative_function(m[docId])
            c[docId] = mean_score
            last_score_of_c = mean_score
            del m[docId]
    else:
        m[docId] = [score]
    print('c: {} || m: {}'.format(c, m))


def add_next_score(score, idsDoc, pl_id, current_scores):
    """
    Preconditions:
        score: is a score to be added to the current_scores.
        idsDoc: an array of document-ids having the score.
        pl_id: posting list id, usually the term.
        current_scores: SortedDict with the scores we are working on.
    Postconditions:
        The fonction save add the tuple [docId, pl_id] to the array current_scores.
        We use this function to add a new value to the scores' array we are working on.
    """
    for idDoc in idsDoc:
        if(score not in current_scores):
            current_scores[score] = dict()
        # on met en dernier [idDoc, idPostingList]
        current_scores[score][len(current_scores[score])] = [idDoc, pl_id]


def get_score_by_doc_id(doc_id, postingListsOrderedById, aggregation_function):
    score = 0
    all_scores = []
    for posting_list in postingListsOrderedById:
        if(doc_id in postingListsOrderedById[posting_list]):
            score_doc_id = postingListsOrderedById[posting_list][doc_id]
            # TODO: score_doc_id[0] = score, score_doc_id[1] = term frequency
            all_scores.append(score_doc_id[0])#1 ou 0 ?
            # Pour mockData()
            # all_scores.append(score_doc_id)
    score = aggregation_function(all_scores)
    return score


def find_fagins_top_k(postingListsOrderedById, postingListsOrderedByScore, k):
    global last_score_of_c

    iterators = dict()
    currentScores = SortedDict()
    # posting_list_id sera le terme de la posting_list
    for posting_list_id in postingListsOrderedByScore:
        iterators[posting_list_id] = reversed(
            postingListsOrderedByScore[posting_list_id])
        # next donne la clé
        score = next(iterators[posting_list_id])
        idsDoc = postingListsOrderedByScore[posting_list_id][score]
        # On initialise la structure de donnees du score
        add_next_score(score, idsDoc, posting_list_id, currentScores)

    c = dict()
    m = dict()
    while len(c) < k and len(currentScores) > 0:
        print("Current {}".format(currentScores))
        item = currentScores.popitem()
        score = item[0]
        postingListId = item[1][0][1]
        docId = item[1][0][0]
        push_to_m(m, c, docId, score, len(
            postingListsOrderedByScore), aggregative_function_mean)
        if(len(item[1]) > 1):
            for doc in item[1]:
                used_docId = item[1][doc][0]
                pl_id = item[1][doc][1]
                if(not (docId == used_docId and pl_id == postingListId)):
                    if score not in currentScores:
                        currentScores[score] = dict()
                    currentScores[score][len(currentScores[score])] = [
                        used_docId, pl_id]
        # getting next new score and add it to currentScores
        try:
            newScore = next(iterators[postingListId])
            idsDoc = postingListsOrderedByScore[postingListId][newScore]
            add_next_score(newScore, idsDoc, postingListId, currentScores)
        except StopIteration:
            print("No more values in postingLists")

    # Verify if there is a better score in the values seen (m)
    for doc_id in m:
        score = get_score_by_doc_id(
            doc_id, postingListsOrderedById, aggregative_function_mean)
        if(score > last_score_of_c):
            # TODO: regarder s'il y a moyen de ne pas faire for loop
            for c_value in c:
                if(c[c_value] == last_score_of_c):
                    del c[c_value]
                    break
            c[doc_id] = score
            last_score_of_c = score
    print('final top {} : {}'.format(k, c))
    return c


def createMockData():
    pl1_score = SortedDict()
    # pl1_score[0.90] += [3]
    pl1_score[0.80] = [5]
    pl1_score[0.70] = [6]
    pl1_score[0.60] = [4]
    pl1_score[0.50] = [1]
    pl1_score[0.40] = [3]
    pl1_score[0.90] = [2]

    pl2_score = SortedDict()
    pl2_score[0.80] = [5]
    pl2_score[0.75] = [2]
    pl2_score[0.74] = [6]
    pl2_score[0.74] += [1]
    pl2_score[0.85] = [3]
    pl2_score[0.70] = [4]

    postingListsOrderedByScore = dict()
    postingListsOrderedByScore['aaa'] = pl1_score
    postingListsOrderedByScore['bbb'] = pl2_score

    pl1_id = dict()
    pl1_id[3] = [0.40,5] # query.get_posting_list nous donne [score,tf]
    pl1_id[1] = [0.50,6]

    pl2_id = dict()
    pl2_id[3] = [0.85,5]
    pl2_id[1] = [0.74,4]

    postingListsOrderedById = dict()
    postingListsOrderedById['aaa'] = pl1_id
    postingListsOrderedById['bbb'] = pl2_id
    print('postingListsOrderedById : {}'.format(postingListsOrderedById))
    print('postingListsOrderedByScore : {}'.format(postingListsOrderedByScore))
    return postingListsOrderedById, postingListsOrderedByScore


if __name__ == "__main__":

    # Applying Top K Algorithm to mockdata
    # postingListsOrderedById, postingListsOrderedByScore = createMockData()
    # top_k = find_fagins_top_k(postingListsOrderedById, postingListsOrderedByScore, 3)
    
    currentWorkspace = './workspace/testalex/'
    filename = 'test1'
    filemanag = fm.FileManager(filename, currentWorkspace)

    tempVoc = SortedDict()

    pathlist = Path("./tests/data/test4/").glob('**/la*')
    for path in pathlist:
        analysis.analyse_newspaper(path, tempVoc, True)
    filemanag.save_vocabularyAndPL_file(tempVoc)

    start = time.time()
    savedVoc = filemanag.read_vocabulary()
    end = time.time()

    print("Red in {} s".format(end - start))
    print("savedDoc : {}".format(savedVoc))

    start = time.time()
    # print(query.get_posting_list(savedVoc, "aa", filemanag))
    topk = apply_top_k_algo(['aa', 'bb'], savedVoc, filemanag, 5)
    end = time.time()
    print('result: {} , done in {}'.format(topk, end - start))

