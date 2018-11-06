import operator
from . import query, filemanager, analysis
from sortedcontainers import SortedDict
from pathlib import Path


def conjuctive_queries(words, voc, filemanager):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    print("**********************posting_lists:")
    print(posting_lists)
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

    print(docs)

    return docs


def disjuctive_queries(words, voc, filemanager):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    print("pl:")
    print(posting_lists)
    docs = set()
    for posting_list in posting_lists:
        for doc in posting_list:
            docs.add(doc)
    print(docs)

    return docs


#get_docs_func can be conjuctive_queries or disjuctive_queries
def naive_top_k_algo(words, voc, filemanager, k, get_docs_func):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    docs = get_docs_func(words, voc, filemanager)
    aggregated_posting_list = aggregate_scores(posting_lists, docs, aggregative_function_sum)
    find_top_k(aggregated_posting_list, k)


def aggregate_scores(posting_lists, docs, aggregative_function):
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
    """ We agregatet the idf score and not the number of occurences"""
    res = 0
    for score in scores:
        res += score[0]
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
    print("Res :"+str(first_k_doc))
    return first_k_doc

if __name__ == "__main__" :


    pathlist = Path("./tests/data/test4/").glob('**/la*')

    vocabulary = SortedDict()
    filemanager = filemanager.FileManager("test4", "./workspace/testalex/")
    for i, newspaper_path in enumerate(pathlist):
        if i < 3:
            analysis.analyse_newspaper(newspaper_path, vocabulary, True)
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = SortedDict()
            print('file %s finished!' % i)
    filemanager.mergePartialVocsAndPL()
    savedVoc = filemanager.read_vocabulary()

    naive_top_k_algo(['aa', 'bb'], savedVoc, filemanager, 5, conjuctive_queries)
    print("**************")

