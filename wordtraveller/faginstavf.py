import wordtraveller.filemanager as fm
import wordtraveller.query as query
import wordtraveller.analysis as analysis
from sortedcontainers import SortedList
from pathlib import Path
import operator

# Vu que les int ne peuvent pas se modifier par reference, j'ai du créer une variable globale
# Cette variable me sert pour apres savoir si les scores qui restent dans m sont plus grands que ceux déjà existants
last_score_of_c = 0

def apply_fagins_ta(words, voc, filemanager, epsilon, k):
    """ 
    Apply the fagins ta algorithm 
    Preconditions:
        words : an array of words to do the research on
        voc : a dictionnay of words and offsets
        filemanager : a filemanager to grab the posting lists
        epsilon : parameter for the algorithm
        k : number of results
    Postconditions:
        Returns top k documents
    """
    posting_lists_ordered_by_id = dict()
    posting_lists_ordered_by_score = dict()
    for word in words:
        orderedById, orderedByScore = query.get_posting_list(voc, word, filemanager, True)

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

def find_fagins_ta(postingListsOrderedById, postingListsOrderedByScore, epsilon, k, aggregative_function=aggregative_function_mean):
    global last_score_of_c
    """
    Execute the fagins algorithm.
    Preconditions:
        postingListsOrderedById : A list of posting lists ordred by Id of the word of the request
        postingListsOrderedByScore : A list of posting lists ordereds by Score of the words of the request
        epsilon : the parameter of the algorithm
        k : number of documents wanted
        aggregative_function : aggregation function to use for the scores when the request have several words
    Postconditions:
        Returns the top k element in an array of tuples, where the first member
        of a tuple is the doc id and the second is the score
    """
    iterators = dict()
    currentScores = SortedList()
    
    for posting_list_id in postingListsOrderedByScore:
        iterators[posting_list_id] = iter(
            postingListsOrderedByScore[posting_list_id])
        score,idDoc = next(iterators[posting_list_id])
        currentScores.add((score,(idDoc,posting_list_id)))


    c = dict()
    tau_i = dict()
    tau = 101  # 101 represents here + infinite 
    muMin = 100  # 100 represents here + infinite
    nb_of_PL = len(postingListsOrderedById)
    while (muMin <= tau/(1 + epsilon) or len(c) < (k)) and len(currentScores) > 0 :

        # Item is the [Score;[[doc_id 1; pl_id 1];[doc_id 2; pl_id 2]]] where scores
        # is the best unreaded score
        score, tuple_docId_postingListId = currentScores.pop()
        docId, postingListId = tuple_docId_postingListId
        tau_i[postingListId] = score
        mu = compute_mu(docId, postingListsOrderedById, nb_of_PL,
                        aggregative_function)
        if len(c) < (k):
            c[docId] = mu
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


        # getting next new score and add it to currentScores


        try:
            newScore, newIdDoc = next(iterators[postingListId])
            currentScores.add((newScore,(newIdDoc,postingListId)))

        except StopIteration:
            pass

    return sorted(c.items(),key=operator.itemgetter(1),reverse=True)