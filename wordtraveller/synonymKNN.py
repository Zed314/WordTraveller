import numpy as np
import argparse
from scipy import spatial
import wordtraveller.filemanager as fm
import wordtraveller.randomIndexing as ri
from sklearn.metrics.pairwise import cosine_similarity
import wordtraveller.preprocessing as pp

def classify_euclidean(inX, dataset, k):
    dataSetSize = dataset.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataset
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5 # Euclidean distance
    sortedDistIndicies=distances.argsort()
    nearest_neighbors = [x for x in sortedDistIndicies[:k]]
    return nearest_neighbors

def classify_cosinus_distance(inX, dataset, k):
    distances = []
    for vec in dataset:
        distances.append(1-cosin_distance(inX,vec))
    ordered = np.argsort(distances)
    nearest_neighbors = [x for x in ordered[:k]]
    return nearest_neighbors

def classify(inX, dataSet, k):
    return classify_cosinus_distance(inX,dataSet,k)
    # return classify_euclidean(inX,dataSet,k)

def cosin_distance(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)

def get_synonyms(term, n, term_dimension, filemanager):
    ri_term, ri_voc = filemanager.read_random_indexing(term_dimension)

    try:
        indexToSearch = ri_term.index(term)
        # print("Finding: {} ".format(ri_term[indexToSearch]))
        result = classify(ri_voc[indexToSearch], ri_voc, n)
        synonym_result = []
        for term_index in result:
            # print("{:<3} : {}".format(i,ri_term[mot]))
            synonym_result.append(ri_term[term_index])
    except ValueError:
        raise Exception(term + ' not found in the indexed list')

    return synonym_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str, default='./workspace/',
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-f", type=str,
                        help="nom de fichier VOC et PL ", required=True)
    parser.add_argument("-t", type=str,
                        help="term pour chercher les termes plus proches ", required=True)
    parser.add_argument("--stemmer", action='store_true',
                        help='activer stemmer')

    args = parser.parse_args()

    random_indexing = ri.RandomIndexing()
    filemanager = fm.FileManager(args.f, args.d)

    ri_term, ri_voc = filemanager.read_random_indexing(random_indexing.getTermDimension())
    if args.stemmer:
        preprocessor = pp.Preprocessor(True)
    else:
        preprocessor = pp.Preprocessor(False)

    stemmed = preprocessor.process(args.t)
    try:
        indexToSearch = ri_term.index(stemmed[0])
        print("Synonymes for : {} ".format(ri_term[indexToSearch]))
        res = classify(ri_voc[indexToSearch], ri_voc, 20)
        for i,term_index in enumerate(res):
            print("{:<3} : {}".format(i,ri_term[term_index]))
    except ValueError as e:
        print(args.t + ' is not in the indexed list')