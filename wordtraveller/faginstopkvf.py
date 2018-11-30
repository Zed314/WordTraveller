import wordtraveller.filemanager as fm
import wordtraveller.query as query
import wordtraveller.analysis as analysis
from sortedcontainers import SortedDict, SortedList
from pathlib import Path
import time
import operator

# Vu que les int ne peuvent pas se modifier par reference, j'ai du creer une variable globale
# Cette variable me sert pour apres savoir si les scores qui restent dans m sont plus grands que ceux déjà existants
last_score_of_c = 0


def apply_top_k_algo(words, voc, filemanager, epsilon, k, typeRequest = 'disjunctive'):
    posting_lists_ordered_by_id = dict()
    posting_lists_ordered_by_score = dict()

    for word in words:

        orderedById, orderedByScore = query.get_posting_list(voc, word, filemanager, True)

        if orderedById and orderedByScore:
            posting_lists_ordered_by_score[word] = orderedByScore
            posting_lists_ordered_by_id[word] = orderedById

    return find_fagins_top_k(posting_lists_ordered_by_id,
                      posting_lists_ordered_by_score, k, typeRequest)


def aggregative_function_mean(values, nb_of_PL):
    """
    Preconditions:
        values: array of values (int or float).
    Postconditions:
        Returns the mean of this values.
    """
    # print("Agregative: {} @ {}".format(values,nb_of_PL))
    sumValues = sum(values)
    if(nb_of_PL == 0):
        return 0
    else:
        return sumValues/nb_of_PL


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
        m[docId] += [score]
        if(len(m[docId]) == nb_of_PL):
            mean_score = aggregative_function(m[docId],nb_of_PL)
            c[docId] = mean_score
            last_score_of_c = mean_score
            del m[docId]
    elif nb_of_PL == 1:
        m[docId] = [score]
        if(len(m[docId]) == nb_of_PL):
            mean_score = aggregative_function(m[docId],nb_of_PL)
            c[docId] = mean_score
            last_score_of_c = mean_score
            del m[docId]
    else:
        m[docId] = [score]
    # print('c: {} || m: {}'.format(c, m))


def get_score_by_doc_id(doc_id, postingListsOrderedById, nb_of_PL, aggregation_function):
    score = 0
    all_scores = []
    for posting_list in postingListsOrderedById:
        if(doc_id in postingListsOrderedById[posting_list]):
            score_doc_id = postingListsOrderedById[posting_list][doc_id]
            # score_doc_id[0] = score, score_doc_id[1] = term frequency
            all_scores.append(score_doc_id[0])#1 ou 0 ?
            # Pour mockData()
            # all_scores.append(score_doc_id)
    score = aggregation_function(all_scores, nb_of_PL)
    return score


def find_fagins_top_k(postingListsOrderedById, postingListsOrderedByScore, k, typeRequest = 'disjunctive'):
    global last_score_of_c
    """ Returns the top k element in an array of tuples, where the first member
    of a tuple is the doc id and the second is the score """
    iterators = dict()
    currentScores = SortedList()
    # posting_list_id sera le terme de la posting_list
    for posting_list_id in postingListsOrderedByScore:
        # TODO : Remove obligation to reverse
        iterators[posting_list_id] = iter(postingListsOrderedByScore[posting_list_id])
        # next donne la tuple <score,idDocument>
        score,idDoc = next(iterators[posting_list_id])

        # On initialise la structure de donnees du score
        currentScores.add((score, (idDoc,posting_list_id)))

    c = dict()
    m = dict()
    nb_of_PL = len(postingListsOrderedById)
    while len(c) < k and len(currentScores) > 0:
        # Item is the [Score;[[doc_id 1; pl_id 1];[doc_id 2; pl_id 2]]] where scores
        # is the best unreaded score
        score, tuple_docId_postingListId = currentScores.pop()
        docId, postingListId = tuple_docId_postingListId
        push_to_m(m, c, docId, score, nb_of_PL, aggregative_function_mean)

        try:
            # getting next new score and add it to currentScores
            newScore, newIdDoc = next(iterators[postingListId])
            currentScores.add((newScore,(newIdDoc,postingListId)))
        except StopIteration:
            pass
            # print("No more values in postingLists")

    # Verify if there is a better score in the values seen (m)
    for doc_id in m:
        score = get_score_by_doc_id(
            doc_id, postingListsOrderedById, nb_of_PL, aggregative_function_mean)
        if(score > last_score_of_c):
            # TODO: regarder s'il y a moyen de ne pas faire for loop
            if(len(c) == k):
                for c_value in c:
                    if(c[c_value] == last_score_of_c):
                        del c[c_value]
                        break
            c[doc_id] = score
            last_score_of_c = score
        elif(len(c) < k and typeRequest == 'disjunctive'):
            c[doc_id] = score
            last_score_of_c = score
    # We sort depending on the score, in the descending order
    c = sorted(c.items(),key=operator.itemgetter(1),reverse=True)
    return c
