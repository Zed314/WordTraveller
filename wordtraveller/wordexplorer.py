import argparse
import wordtraveller.filemanager as fm
import wordtraveller.naivetopk as naivetopk
import wordtraveller.faginstavf as faginsta
import wordtraveller.faginstopkvf as faginstopk
import wordtraveller.view as view
import wordtraveller.preprocessing as preprocessing
import wordtraveller.randomIndexing as ri

preprocessor = preprocessing.Preprocessor(True)

def analysis_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str, default='./workspace/',
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-f", type=str,
                        help="nom de fichier VOC et PL ", required=True)
    parser.add_argument("-q", type=str,
                        help="requête des termes separés par un virgule. Ex: voiture,maison ", required=True)
    parser.add_argument("--file", type=str,
                        help="fichier avec un nombre de mots pour la requête (à definir la structure de ce fichier)")
    parser.add_argument("-n", type=int, default=3,
                        help="nombre de résultats souhaité de documents ")
    parser.add_argument("--algo", type=str, default="naive",
                        help="algorithme souhaité pour l'indexation ")
    parser.add_argument("--view", type=str, default="simple",
                        help="type de visulasation simple ou fullText ")
    parser.add_argument("--vpath", type=str, default="./data/latimesMini/",
                        help="path des fichier sources pour --view fullText")
    parser.add_argument("--randomindexing", action='store_true',
                        help='activer query random indexing')


    args = parser.parse_args()
    # print('Args : {}'.format(args))
    filemanager = fm.FileManager(args.f, args.d)
    savedVoc = filemanager.read_vocabulary()

    random_indexing = None
    if args.randomindexing:
        random_indexing = ri.RandomIndexing()

    epsilon = 0

    switchAlgo = {"naive": naivetopk.apply_naive_top_k_algo,
                  "fagins": faginstopk.apply_top_k_algo,
                  "faginsTA": faginsta.apply_fagins_ta}

    algoFunct = switchAlgo[args.algo]
    words = preprocessor.process(args.q)
    print (words)

    # TODO: random indexing: voir comment l'appliquer
    if args.randomindexing:
        ri_voc = filemanager.read_random_indexing(random_indexing.getTermDimension())
        for i,ri1 in enumerate(ri_voc):
            if i<20:
                print("{} : {}".format(ri1,ri_voc[ri1]))

    result = algoFunct(words, savedVoc, filemanager, epsilon, args.n)
    print(result)

    switchView = {"simple": view.displayResults,
                  "fullText": view.displayResultsText}
    viewFunct = switchView[args.view]
    viewFunct(result, args.vpath)


if __name__ == "__main__":
    analysis_parameters()
