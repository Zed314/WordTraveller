from numpy import *



def classify(inX, dataSet, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5 # Euclidean distance
    sortedDistIndicies=distances.argsort()
    nearest_neighbors = [x for x in sortedDistIndicies[:k]]
    return nearest_neighbors

if __name__ == "__main__":
    group = array([[1, 1.1], [1, 1], [0, 0], [0, 0.1]])
    res = classify([0, 0], group, 3)
    print(res)