import argparse
from . import filemanager as fm
from . import naivetopk
from . import faginsta
from . import faginstopk
from . import view


def analysis_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str, default = './workspace/',
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-f", type=str,
                        help="nom de fichier VOC et PL ", required=True)
    parser.add_argument("-q", type=str,
                        help="requête des termes separés par un virgule. Ex: voiture,maison ", required = True)
    parser.add_argument("--file", type=str,
                        help="fichier avec un nombre de mots pour la requête (à definir la structure de ce fichier)")
    parser.add_argument("-n", type=int, default = 3,
                        help="nombre de résultats souhaité de documents ")
    parser.add_argument("--algo", type=str,default="naive",
                        help="algorithme souhaité pour l'indexation ")
    parser.add_argument("--view", type=str,default="simple",
                        help="type de visulasation simple ou fullText ")
    parser.add_argument("--vpath", type=str,default="./data/latimesMini/",
                        help="path des fichier sources pour --view fullText")

    args = parser.parse_args()
    # print('Args : {}'.format(args))
    filemanager = fm.FileManager(args.f, args.d)
    savedVoc = filemanager.read_vocabulary()

    switchAlgo = {"naive":naivetopk.naive_top_k_algo,
    "fagins": faginstopk.apply_top_k_algo,
    "faginsTA": faginsta.apply_fagins_ta}
    
    algoFunct = switchAlgo[args.algo]
    words = args.q.split(",")
    result = algoFunct(words, savedVoc, filemanager, args.n)

    switchView = {"simple": view.displayResults,
    "fullText": view.displayResultsText}
    viewFunct = switchView[args.view]
    viewFunct(result, args.vpath)


if __name__ == "__main__":
    analysis_parameters()
