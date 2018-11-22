import wordtraveller.filemanager as fm
import wordtraveller.analysis as analysis
import wordtraveller.preprocessing as preprocessing
import wordtraveller.randomIndexing as ri
import argparse
from pathlib import Path
from sortedcontainers import SortedDict
from tqdm import tqdm


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
    parser.add_argument("--partial", type=int,default=-1,
                        help='créer les fichiers par réunion de plusieurs fichiers avec une granularité (par défaut : un pour chaque journal)')
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


    if args.partial !=-1:
        for newspaper_path in tqdm(list(pathlist)):
            analysis.analyse_newspaper(newspaper_path, vocabulary, randomIndexing, True)
            filemanager.save_vocabularyAndPL_file(vocabulary, True)
            vocabulary = dict()
        filemanager.mergePartialVocsAndPL()
        print("PL and VOC merged succesfully")
    else :
        for newspaper_path in tqdm(list(pathlist)):
            analysis.analyse_newspaper(newspaper_path, vocabulary, randomIndexing, True)
        filemanager.save_vocabularyAndPL_file(vocabulary)
        
    print("Inverted file created !")
    
    if args.randomindexing:
        filemanager.save_random_indexing(randomIndexing.getTermsVectors(),randomIndexing.getTermDimension())
        print("Random indexing created")

if __name__ == "__main__" :
    analysis_parameters()
