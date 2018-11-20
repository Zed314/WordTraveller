import numpy as np
import argparse
from scipy import spatial
import wordtraveller.filemanager as fm
import wordtraveller.randomIndexing as ri
from sklearn.metrics.pairwise import cosine_similarity

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
    # return classify_cosinus_distance(inX,dataSet,k)
    return classify_euclidean(inX,dataSet,k)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str, default='./workspace/',
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-f", type=str,
                        help="nom de fichier VOC et PL ", required=True)
    parser.add_argument("-t", type=str,
                        help="term pour chercher les termes plus proches ", required=True)

    args = parser.parse_args()

    group = np.array([[1, 1.1], [1, 1], [0, 0], [0, 0.1]])
    # print(" {} {} {}".format(group[0], group[1], cosine_similarity()))
    random_indexing = ri.RandomIndexing()
    filemanager = fm.FileManager(args.f, args.d)

    ri_term, ri_voc = filemanager.read_random_indexing(random_indexing.getTermDimension())


    try:
        indexToSearch = ri_term.index(args.t)
        # for i,ri1 in enumerate(ri_voc):
        #     if i<20000 and i>19990:
        #         print("{} : {}".format(ri_term[i],ri_voc[i]))
        print("Finding: {} ".format(ri_term[indexToSearch]))
        res = classify(ri_voc[indexToSearch], ri_voc, 20)
        for i,mot in enumerate(res):
            print("{:<3} : {}".format(i,ri_term[mot]))
    except ValueError as e:
        print(args.t + ' is not in the indexed list')