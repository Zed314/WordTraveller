import argparse
from . import filemanager as fm
from . import naivetopk


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
    parser.add_argument("-n", type=str,
                        help="nombre de résultats souhaité de documents ")

    args = parser.parse_args()
    print(args)
    print("Cest uqou {} {}".format(args.f,args.d))
    filemanager = fm.FileManager(args.f, args.d)
    savedVoc = filemanager.read_vocabulary()
    words = args.q.split(",")
    result = naivetopk.naive_top_k_algo(words, savedVoc, filemanager, 3, naivetopk.conjuctive_queries)
    print("query result: {}".format(result))


if __name__ == "__main__":
    analysis_parameters()
