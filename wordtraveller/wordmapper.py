import wordtraveller.filemanager as fm
import wordtraveller.analysis as analysis
import wordtraveller.preprocessing as preprocessing
import wordtraveller.randomIndexing as ri
import wordtraveller.compressor as zip
import argparse
import time
from pathlib import Path
from sortedcontainers import SortedDict
from tqdm import tqdm

MAX_RANDOM_INDEXING = 10


def analysis_parameters():
    global MAX_RANDOM_INDEXING

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str,
                        help="dossier avec les documents", required=True)
    parser.add_argument("-f", type=str,
                        help="nom de fichier pour enregistrer les fichiers après l'indexation ", required=True)
    parser.add_argument("-o", type=str, default='./workspace/',
                        help="dossier pour enregistrer les fichiers après l'indexation ")
    parser.add_argument("--zip", action='store_true',
                        help="compression zip à la fin")
    parser.add_argument("--partial", type = int, default = -1,
                        help='créer les fichiers par réunion de plusieurs fichiers avec une granularité de documents choisie. Si -2, alors granularité d\'un journal. Valeur conseillée : 2000.')
    parser.add_argument("--stemmer", action='store_true',
                        help='activer stemmer')
    parser.add_argument("--randomindexing", action='store_true',
                        help='activer random indexing')
    args = parser.parse_args()

    latimes_path = args.d
    if not args.d.endswith("/"):
        latimes_path += "/"

    workspace_path = args.o
    if not args.d.endswith("/"):
        workspace_path += "/"

    pathlist = Path(latimes_path).glob('**/la*')

    vocabulary = dict()
    filemanager = fm.FileManager(args.f, workspace_path)
    random_indexing = None
    if args.randomindexing:
        random_indexing = ri.RandomIndexing()

    if args.stemmer:
        analysis.setPreprocessor(preprocessing.Preprocessor(True))
    
    if args.partial == -2:
        print("Partial analysis in progress")
        for newspaper_path in tqdm(list(pathlist)):
            docsRedInDocIteration = analysis.analyse_newspaper(newspaper_path, vocabulary, None, False)
            filemanager.save_vocabularyAndPL_file(vocabulary, isPartial=True)
            vocabulary = dict()
        print("Merging in progress…")
        filemanager.mergePartialVocsAndPL()
        print("PL and VOC merged succesfully")
    if args.partial != -1:
        nbDocsInMemory = 0
        stepFlush = args.partial

        rand_indexing_counter = 0
        for newspaper_path in tqdm(list(pathlist)):

            docsRedInDocIteration = -1
            nbDocsRedInThisJournal = 0
            while(docsRedInDocIteration != 0):
                if rand_indexing_counter < MAX_RANDOM_INDEXING:
                    docsRedInDocIteration = analysis.analyse_newspaper(
                        newspaper_path, vocabulary, random_indexing, False, nbDocsRedInThisJournal, nbDocsRedInThisJournal+stepFlush)
                else:
                    docsRedInDocIteration = analysis.analyse_newspaper(
                        newspaper_path, vocabulary, None, False, nbDocsRedInThisJournal, nbDocsRedInThisJournal+stepFlush)
                nbDocsInMemory += docsRedInDocIteration
                nbDocsRedInThisJournal += docsRedInDocIteration
                if nbDocsInMemory >= stepFlush:
                    filemanager.save_vocabularyAndPL_file(
                        vocabulary, isPartial=True)
                    vocabulary = dict()
                    nbDocsInMemory = 0
                rand_indexing_counter += 1

        if nbDocsInMemory != 0:
            filemanager.save_vocabularyAndPL_file(vocabulary, isPartial=True)

        print("Merging in progress…")

        filemanager.mergePartialVocsAndPL()
        print("PL and VOC merged succesfully")
        print("Inverted file created !")

    else:
        print("Non partial")
        rand_indexing_counter = 0
        for newspaper_path in tqdm(list(pathlist)):
            if rand_indexing_counter < MAX_RANDOM_INDEXING:
                rand_indexing_counter += 1
                analysis.analyse_newspaper(
                    newspaper_path, vocabulary, random_indexing, False)
            else:
                analysis.analyse_newspaper(
                    newspaper_path, vocabulary, None, False)
        analysis.computeIDF(vocabulary)
        filemanager.save_vocabularyAndPL_file(vocabulary)

        print("Inverted file created !")

    if args.zip:

        print("Compressing…")
        filemanager = fm.FileManager(args.f, args.o)

        zip.compressPLVBYTEFromSavedVocAndPL(filemanager)

        zip.compressZip(filemanager.getPathPLCompressed())

        zip.compressZip(filemanager.getPathVocCompressed())

        zip.compressZip(filemanager.getPathPLScore())

        print("Compressed !")

    if args.randomindexing:
        filemanager.save_random_indexing(
            random_indexing.getTermsVectors(), random_indexing.getTermDimension())
        print("Random indexing created")


if __name__ == "__main__":
    analysis_parameters()
