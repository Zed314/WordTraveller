from . import query, analysis
from . import filemanager as fm
from sortedcontainers import SortedDict
from pathlib import Path
import operator

# Vu que les int ne peuvent pas se modifier par reference, j'ai du creer une variable global
# Cette variable me sers pour apres savoir si les scores qui restent dans m sont plus grandes que celles déjà existantes
last_score_of_c = 0


def apply_fagins_ta(words, voc, filemanager, epsilon, k):
    posting_lists_ordered_by_id = SortedDict()
    posting_lists_ordered_by_score = SortedDict()
    for word in words:
        orderedById, orderedByScore = query.get_posting_list(
        voc, word, filemanager, returnPostingListOrderedByScore = True)
        if orderedById and orderedByScore:
            posting_lists_ordered_by_score[word] = orderedByScore
            posting_lists_ordered_by_id[word] = orderedById
    return find_fagins_ta(posting_lists_ordered_by_id,
                          posting_lists_ordered_by_score, epsilon, k)


def aggregative_function_mean(values, nb_of_PL):
    """
    Preconditions:
        values: array of values (int or float).
        nb_of_PL: the number of postingList
    Postconditions:
        Returns the mean of this values.
    """
    sumValues = sum(values)
    if(nb_of_PL == 0):
        return 0
    else:
        return sumValues/nb_of_PL


def compute_mu(docId, postingListsOrderedById, nb_of_PL, aggregative_function):
    """
    Preconditions:
        docId: Id of a document,
        postingListsOrderedById: all the postingLists with a random access by id
        aggregative_function: fonctione used to agegat the an array of valuses,
            typicly mean.

    Postconditions:
        The fonctione returns mu,  being the aggegation of the scores of the
        document docId.
    """

    values = [-1]*len(postingListsOrderedById)
    i = 0
    for posting_list_id in postingListsOrderedById:
        if docId in postingListsOrderedById[posting_list_id]:
            values[i] = postingListsOrderedById[posting_list_id][docId]
            i += 1
    tmp = [l[0] for l in values[0:i]]
    mu = aggregative_function(tmp, nb_of_PL)
    return mu


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


# n'as pas l'aire d'étre utiliser ailleur
def get_score_by_doc_id(doc_id, postingListsOrderedById, aggregation_function):
    score = 0
    all_scores = []
    for posting_list in postingListsOrderedById:
        score_doc_id = postingListsOrderedById[posting_list][doc_id]
        all_scores.append(score_doc_id)
    score = aggregation_function(all_scores)
    return score


def find_fagins_ta(postingListsOrderedById, postingListsOrderedByScore, epsilon, k, aggregative_function=aggregative_function_mean):
    global last_score_of_c

    iterators = dict()
    currentScores = SortedDict()
    # posting_list_id sera le terme de la posting_list
    for posting_list_id in postingListsOrderedByScore:
<<<<<<< HEAD
=======
        print("posting_list_id {}".format(posting_list_id))
>>>>>>> 1cdb305ea472c9e3c7df28a08c222ddb561fea27
        iterators[posting_list_id] = reversed(
            postingListsOrderedByScore[posting_list_id])
        # next donne la clé
        score = next(iterators[posting_list_id])
        idsDoc = postingListsOrderedByScore[posting_list_id][score]
        # On initialise la structure de donnees du score
        add_next_score(score, idsDoc, posting_list_id, currentScores)

    c = dict()
    tau_i = dict()
    tau = 101  # 100 représente ici +l'infini.
    muMin = 100  # 10 représente ici +l'infini.
    nb_of_PL = len(postingListsOrderedById)
    while (muMin <= tau/(1 + epsilon) or len(c) < (k))and len(currentScores) > 0 :

        # Item is the [Score;[[doc_id 1; pl_id 1];[doc_id 2; pl_id 2]]] where scores
        # is the best unreaded score
        item = currentScores.popitem()
        score = item[0]
        postingListId = item[1][0][1]
        docId = item[1][0][0]
        tau_i[postingListId] = score
        mu = compute_mu(docId, postingListsOrderedById, nb_of_PL,
                        aggregative_function)
        if len(c) < (k):
            c[docId] = mu
        # muMin = min(muMin,mu )
            # Not sure that it changes anything tho
            muMin = min(c.values())
        elif muMin < mu and docId not in c:
            # Remove the document with the smallest score from C
            for docIdInC in c:
                if c[docIdInC] == muMin:
                    c.pop(docIdInC)
                    break
            c[docId] = mu
            muMin = min(c.values())

        if len(tau_i) == len(postingListsOrderedById):
            tau = aggregative_function(tau_i.values(),nb_of_PL)


        # if there is an other document in currentScores with the same score that the curent one
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
            pass
            # print("No more values in postingLists")

    return sorted(c.items(),key=operator.itemgetter(1),reverse=True)


def createMockData():
    pl1_score = SortedDict()
    pl1_score[0.90] = [2]
    #pl1_score[0.90] += [3]
    pl1_score[0.80] = [5]
    pl1_score[0.70] = [6]
    pl1_score[0.60] = [4]
    pl1_score[0.50] = [1]
    pl1_score[0.40] = [3]

    pl2_score = SortedDict()
    pl2_score[0.85] = [3]
    pl2_score[0.80] = [5]
    pl2_score[0.75] = [2]
    pl2_score[0.74] = [6]
    pl2_score[0.74] += [1]
    pl2_score[0.70] = [4]

    postingListsOrderedByScore = dict()
    postingListsOrderedByScore['aaa'] = pl1_score
    postingListsOrderedByScore['bbb'] = pl2_score

    pl1_id = dict()
    pl1_id[6] = [0.70, 4] # query.get_posting_list nous donne [score,tf]
    pl1_id[5] = [0.80, 6]
    pl1_id[4] = [0.60, 3]
    pl1_id[3] = [0.40, 4]
    pl1_id[2] = [0.90, 8]
    pl1_id[1] = [0.50, 3]

    pl2_id = dict()
    pl2_id[1] = [0.74, 2]
    pl2_id[2] = [0.75, 3]
    pl2_id[3] = [0.85, 4]
    pl2_id[4] = [0.70, 2]
    pl2_id[5] = [0.80, 6]
    pl2_id[6] = [0.74, 4]

    postingListsOrderedById = dict()
    postingListsOrderedById['aaa'] = pl1_id
    postingListsOrderedById['bbb'] = pl2_id
    print('postingListsOrderedById : {}'.format(postingListsOrderedById))
    print('postingListsOrderedByScore : {}'.format(postingListsOrderedByScore))
    return postingListsOrderedById, postingListsOrderedByScore


if __name__ == "__main__":

    # Applying Top K Algorithm to mockData
    # postingListsOrderedById, postingListsOrderedByScore = createMockData()
    # c = find_fagins_ta(postingListsOrderedById, postingListsOrderedByScore, 3, aggregative_function_mean)
    # print("Resulta c : {}".format(c))

    currentWorkspace = './workspace/testfaginsta/'
    filename = 'test1'
    filemanag = fm.FileManager(filename, currentWorkspace)

    tempVoc = SortedDict()

    pathlist = Path("./tests/data/test4/").glob('**/la*')
    for path in pathlist:
        analysis.analyse_newspaper(path, tempVoc, True)
    filemanag.save_vocabularyAndPL_file(tempVoc)

    savedVoc = filemanag.read_vocabulary()
    faginsta = apply_fagins_ta(['aa', 'bb'], savedVoc, filemanag, 2)
    print("result faginsTA : {}".format(faginsta))
