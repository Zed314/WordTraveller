import operator
from . import query, filemanager, analysis
from sortedcontainers import SortedDict
from pathlib import Path


def naive_top_k_algo(words, voc, filemanager, k):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    # TODO: Fonction qui permet de recuperer tous les docx?
    aggregated_posting_list = aggregate_scores(posting_lists, [1, 2, 3], aggregative_function_min)
    find_top_k(aggregated_posting_list, k)


def aggregate_scores(posting_lists, docs, aggregative_function):
    aggregated_posting_list = dict()
    scores = []
    for doc in docs:
        for posting_list in posting_lists:
            if doc in posting_list:
                scores.append(posting_list[doc])
            else:
                scores.append(0)
        aggregated_posting_list[doc] = aggregative_function(scores)
        scores = []
    return aggregated_posting_list


def aggregative_function_sum(scores):
    res = 0
    for score in scores:
        res += score
    return res


def aggregative_function_mean(scores):
    res = 0
    for score in scores:
        res += score
    return res/len(scores)


def aggregative_function_min(scores):
    res = scores[0]
    for score in scores:
        res = min(res, score)
    return res


def find_top_k(aggregated_posting_list, k):
    sorted_list = sorted(aggregated_posting_list.items(), key=operator.itemgetter(1), reverse=True)
    first_k_doc = [x[0] for x in sorted_list[:k] if x[1] != 0]
    print(first_k_doc)
    return first_k_doc

if __name__ == "__main__" :
    #x = [{1: 2, 3: 4, 4: 3, 2: 1, 0: 0}, {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}]
    #aggregation(x)
    voc = SortedDict()
    currentWorkspace = './tests/workspace/test1/'
    filename = 'test1'

    pathlist = Path("./tests/data/test1/").glob('**/la*')
    for path in pathlist:
        analysis.analyse_newspaper(path, voc)

    analysis.save_vocabulary(voc, filename, currentWorkspace)

    filemanager = filemanager.FileManager(filename, currentWorkspace)

    savedVoc = filemanager.read_vocabulary()
    words = ["aa", "bb"]
    naive_top_k_algo(words, savedVoc, filemanager, 3)

