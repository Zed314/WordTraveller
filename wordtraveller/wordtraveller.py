import argparse


def analysis_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", type=str,
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-q", type=str,
                        help="requête des termes separés par un virgule. Ex: voiture,maison ")
    parser.add_argument("--file", type=str,
                        help="nombre de résultats souhaité de documents ")
    parser.add_argument("-n", type=str,
                        help="fichier avec un nombre de mots pour la requête (à definir la structure de ce fichier)")

    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    analysis_parameters()