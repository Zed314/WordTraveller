import wordtraveller.filemanager as fm
import wordtraveller.analysis as analysis
import wordtraveller.preprocessing as preprocessing
import wordtraveller.randomIndexing as ri
import argparse
from pathlib import Path
from sortedcontainers import SortedDict


def analysis_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str,
                        help="dossier avec les documents", required=True)
    parser.add_argument("-f", type=str,
                        help="nom de fichier pour enregistrer les fichiers après l'indexation ", required=True)
    parser.add_argument("-o", type=str, default='./workspace/',
                        help="dossier pour enregistrer les fichiers après l'indexation ")
    parser.add_argument("--zip", type=str,
                        help="compression à faire à la fin ")
    parser.add_argument("--partial", action='store_true',
                        help='enregistrer les fichiers de manière partiale')
    parser.add_argument("--stemmer", action='store_true',
                        help='activer stemmer')
    parser.add_argument("--randomindexing", action='store_true',
                        help='activer random indexing')
    args = parser.parse_args()

    if not args.d.endswith("/"):
        path = args.d + "/"

    pathlist = Path(args.d).glob('**/la*')

    vocabulary = dict()
    filemanager = fm.FileManager(args.f, args.o)
    randomIndexing = None
    if args.randomindexing:
        randomIndexing = ri.RandomIndexing()

    if args.stemmer:
        analysis.setPreprocessor(preprocessing.Preprocessor(True))
    for i, newspaper_path in enumerate(pathlist):
        analysis.analyse_newspaper(newspaper_path, vocabulary, randomIndexing, True)
        if args.partial:
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = dict()
        print('file %s finished!' % i)
    if args.partial:
        filemanager.mergePartialVocsAndPL()
    else:
        filemanager.save_vocabularyAndPL_file(vocabulary)
    # print("VOC: {}".format(vocabulary))
    print("PL and VOC merged succesfully")
    if args.randomindexing:
        filemanager.save_random_indexing(randomIndexing.getTermsVectors(),randomIndexing.getTermDimension())
        print("Random indexing created")

if __name__ == "__main__" :
    analysis_parameters()
