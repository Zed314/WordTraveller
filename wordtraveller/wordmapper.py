import wordtraveller.filemanager as fm
import wordtraveller.analysis as analysis
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
                        help='sum the integers (default: find the max)')
    args = parser.parse_args()

    if not args.d.endswith("/"):
        path = args.d + "/"

    pathlist = Path(args.d).glob('**/la*')


    vocabulary = SortedDict()
    filemanager = fm.FileManager(args.f, args.o)
    for i, newspaper_path in enumerate(pathlist):
            analysis.analyse_newspaper(newspaper_path, vocabulary, True)
            if args.partial:
                filemanager.save_vocabularyAndPL_file(vocabulary, True)
            else:
                filemanager.save_vocabularyAndPL_file(vocabulary, False)
            vocabulary = SortedDict()
            print('file %s finished!' % i)
    if args.partial:
        filemanager.mergePartialVocsAndPL()
    print("PL and VOC merged succesfully")

if __name__ == "__main__" :
    analysis_parameters()
