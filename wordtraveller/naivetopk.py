import operator
import wordtraveller.query as query
import wordtraveller.filemanager as filemanager
import wordtraveller.analysis as analysis
from sortedcontainers import SortedDict
from pathlib import Path


def conjunctive_queries(posting_lists):
    """
    To find each DOC ID for which all the query terms are present
    Preconditions:
        posting_lists: all the postingLists.
    Postconditions:
        Returns an array of doc
    """
    #posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    # print("**********************posting_lists: {}".format(posting_lists))
    smallest_pl_length = len(posting_lists[0])
    smallest_pl = posting_lists[0]
    for posting_list in posting_lists:
        if len(posting_list) < smallest_pl_length:
            smallest_pl_length = len(posting_list)
            smallest_pl = posting_list

    docs = set()

    for doc in smallest_pl:
        find_doc = True
        for posting_list in posting_lists:
            if doc in posting_list:
                find_doc = True
            else:
                find_doc = False
                break
        if find_doc:
            docs.add(doc)

    # print('docs : {}'.format(docs))

    return docs


def disjunctive_queries(posting_lists):
    """
    To find each DOC ID for which at least one query terms are present
    Preconditions:
        posting_lists: all the postingLists.
    Postconditions:
        Returns an array of doc
    """
    #posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    # print("pl: {}".format(posting_lists))
    docs = set()
    for posting_list in posting_lists:
        for doc in posting_list:
            docs.add(doc)
    # print('docs : {}'.format(docs))

    return docs

def apply_naive_top_k_algo(words, voc, filemanager, epsilon, k, get_docs_func=disjunctive_queries):
    """
    Apply the naive top k algorithm
    Preconditions:
        words : an array of words to do the research on
        voc : a dictionnay of words and offsets
        filemanager : a filemanager to grab the posting lists
        epsilon : parameter for the algorithm
        k : number of results
        get_docs_func : type of request(can be conjunctive_queries or disjunctive_queries)
    Postconditions:
        Returns top k documents
    """
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    if all((not posting_list) for posting_list in posting_lists):
        return []
    return naive_top_k_algo(posting_lists, k, get_docs_func)

#get_docs_func can be conjunctive_queries or disjunctive_queries
def naive_top_k_algo(posting_lists, k, get_docs_func):
    docs = get_docs_func( posting_lists)
    aggregated_posting_list = aggregate_scores(posting_lists, docs, aggregative_function_mean)
    return find_top_k(aggregated_posting_list, k)


def aggregate_scores(posting_lists, docs, aggregative_function):
    """
    Aggregate scores.
    Preconditions:
        posting_lists: all the postingLists.
        docs: documents need to be sorted
        aggregative_function: function used for aggregate scores
    Postconditions:
        Returns aggregated postingLists
    """
    aggregated_posting_list = dict()
    scores = []
    for doc in docs:
        for posting_list in posting_lists:
            if doc in posting_list:
                scores.append(posting_list[doc])
            else:
                scores.append([0, 0])
        aggregated_posting_list[doc] = aggregative_function(scores)
        scores = []
    return aggregated_posting_list


def aggregative_function_sum(scores):
    """
    Preconditions:
        scores: array of scores (int or float).
    Postconditions:
        Returns the sum of this values.
    """
    res = 0
    for score in scores:
        res += score[0]
    return res


def aggregative_function_mean(scores):
    """
    Preconditions:
        scores: array of scores (int or float).
    Postconditions:
        Returns the mean of this values.
    """
    res = 0
    for score in scores:
        res += score[0]
    return res/len(scores)


def aggregative_function_min(scores):
    """
    Preconditions:
        scores: array of scores (int or float).
    Postconditions:
        Returns the minimum of this values.
    """
    res = scores[0]
    for score in scores:
        res = min(res, score)
    return res


def find_top_k(aggregated_posting_list, k):
    """
    Execute the naive top k algorithm.
    Preconditions:
        aggregated_posting_list : A list of posting lists with aggregated scores
        k : number of documents wanted
    Postconditions:
        Returns an array of top k documents
    """
    sorted_list = sorted(aggregated_posting_list.items(), key=operator.itemgetter(1), reverse=True)
    first_k_doc = [x for x in sorted_list[:k] if x[1] != 0]
    return first_k_doc

