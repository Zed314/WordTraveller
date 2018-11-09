import operator
import wordtraveller.query as query
import wordtraveller.filemanager as filemanager
import wordtraveller.analysis as analysis
from sortedcontainers import SortedDict
from pathlib import Path


def conjunctive_queries(words, voc, filemanager):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
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


def disjunctive_queries(words, voc, filemanager):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    # print("pl: {}".format(posting_lists))
    docs = set()
    for posting_list in posting_lists:
        for doc in posting_list:
            docs.add(doc)
    # print('docs : {}'.format(docs))

    return docs


#get_docs_func can be conjunctive_queries or disjunctive_queries
def naive_top_k_algo(words, voc, filemanager, epsilon, k, get_docs_func=disjunctive_queries):
    posting_lists = [query.get_posting_list(voc, word, filemanager) for word in words]
    if all((not posting_list) for posting_list in posting_lists):
        return []
    docs = get_docs_func(words, voc, filemanager)
    aggregated_posting_list = aggregate_scores(posting_lists, docs, aggregative_function_mean)
    return find_top_k(aggregated_posting_list, k)


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
        res += score[0]
    return res/len(scores)


def aggregative_function_min(scores):
    res = scores[0]
    for score in scores:
        res = min(res, score)
    return res


def find_top_k(aggregated_posting_list, k):
    sorted_list = sorted(aggregated_posting_list.items(), key=operator.itemgetter(1), reverse=True)
    first_k_doc = [x for x in sorted_list[:k] if x[1] != 0]
    # print('Result first_k_doc: {}'.format(first_k_doc))
    return first_k_doc

if __name__ == "__main__" :


    pathlist = Path("./tests/data/test4/").glob('**/la*')

    vocabulary = SortedDict()
    filemanager = filemanager.FileManager("test500", "./workspace/")
    # for i, newspaper_path in enumerate(pathlist):
    #     if i < 2:
    #         analysis.analyse_newspaper(newspaper_path, vocabulary, True)
    #         filemanager.save_vocabularyAndPL_file(vocabulary, True)
    #         vocabulary = SortedDict()
    #         print('file %s finished!' % i)
    # filemanager.mergePartialVocsAndPL()
    savedVoc = filemanager.read_vocabulary()
    words = ["manipul", 'maniscalco', 'manischewitz']
    result = naive_top_k_algo(words, savedVoc, filemanager, 10, disjunctive_queries)
    print("Result: {}".format(result))
