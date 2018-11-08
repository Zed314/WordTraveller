import argparse
from . import filemanager as fm
from . import naivetopk
from . import faginsta
from . import faginstopk

def analysis_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str,
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-f", type=str,
                        help="nom de fichier VOC et PL ", required=True)
    parser.add_argument("-q", type=str,
                        help="requête des termes separés par un virgule. Ex: voiture,maison ")
    parser.add_argument("--file", type=str,
                        help="fichier avec un nombre de mots pour la requête (à definir la structure de ce fichier)")
    parser.add_argument("-n", type=int, default = 3,
                        help="nombre de résultats souhaité de documents ")
    parser.add_argument("--algo", type=str,default="naive",
                        help="algorithme souhaité pour l'indexation ")

    args = parser.parse_args()
    print(args)
    print("Cest uqou {} {}".format(args.f,args.d))
    filemanager = fm.FileManager(args.f, args.d)
    savedVoc = filemanager.read_vocabulary()

    switchAlgo = {"naive":naivetopk.naive_top_k_algo,
    "fagins": faginstopk.apply_top_k_algo,
    "faginsTA": faginsta.apply_fagins_ta}
    algoFunct = switchAlgo[args.algo]
    words = args.q.split(",")
    result = algoFunct(words, savedVoc, filemanager, args.n)
    print("query result: {}".format(result))


if __name__ == "__main__":
    analysis_parameters()
