import argparse

import wordtraveller.compressor as compressor
import wordtraveller.faginstavf as faginsta
import wordtraveller.faginstopkvf as faginstopk
import wordtraveller.filemanager as fm
import wordtraveller.naivetopk as naivetopk
import wordtraveller.preprocessing as preprocessing
import wordtraveller.randomIndexing as ri
import wordtraveller.randomIndexingFindSynonym as synknn
import wordtraveller.view as view

preprocessor = preprocessing.Preprocessor(True)


def analysis_parameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", type=str, default='./workspace/',
                        help="dossier avec les fichier VOC et PL résultat de l'indexation")
    parser.add_argument("-f", type=str,
                        help="nom de fichier VOC et PL ", required=True)
    parser.add_argument("-q", type=str,
                        help="requête des termes separés par un virgule. Ex: voiture,maison ", required=True)
    parser.add_argument("-n", type=int, default=3,
                        help="nombre de résultats souhaité de documents ")
    parser.add_argument("--stemmer", action='store_true',
                        help="activer le stemming sur les termes de la requête")
    parser.add_argument("--algo", type=str, default="naive",
                        help="algorithme souhaité pour la requête ")
    parser.add_argument("--view", type=str, default="simple",
                        help="type de visualisation. Options possible: simple ou fullText ")
    parser.add_argument("--vpath", type=str, default="./data/latimes/",
                        help="path des fichier sources pour --view fullText")
    parser.add_argument("--improvedquery", action='store_true',
                        help="activer recherche de synonymes pour l'amélioration de la requête")

    args = parser.parse_args()
    latimes_path = args.d
    if not args.d.endswith("/"):
        latimes_path += "/"
    filemanager = fm.FileManager(args.f, latimes_path)
    savedVoc = filemanager.read_vocabulary()
    if args.stemmer:
        print("Stemmer activated")
        preprocessor = preprocessing.Preprocessor(True)
    else :
        preprocessor = preprocessing.Preprocessor(False)
    epsilon = 0

    switchAlgo = {"naive": naivetopk.apply_naive_top_k_algo,
                  "fagins": faginstopk.apply_top_k_algo,
                  "faginsTA": faginsta.apply_fagins_ta}

    algoFunct = switchAlgo[args.algo]

    words = preprocessor.process(args.q)
    words_request = []
    if args.improvedquery:
        random_indexing = ri.RandomIndexing()
        for word in words:
            words_request.append(word)

            try:
                synonymes = synknn.get_synonyms(
                    word, 2, random_indexing.getTermDimension(), filemanager)
                if len(synonymes) == 2:
                    words_request.append(synonymes[1])
            except Exception as e:
                print(e)
        print("Improved query: {}".format(words_request))
    else:
        words_request = words

    if (not filemanager.doesUnCompressedVersionExists()) and filemanager.doesCompressedVersionExists():
        print("Unzipping in progress…")
        compressor.decompressZip(filemanager.getPathPLCompressed(),filemanager.getPathPLCompressed())
        compressor.decompressZip(filemanager.getPathVocCompressed(),filemanager.getPathVocCompressed())
        compressor.decompressZip(filemanager.getPathPLScore(),filemanager.getPathPLScore())
        compressor.decompressPLVBYTE(filemanager)

    result = algoFunct(words_request, savedVoc, filemanager, epsilon, args.n)

    switchView = {"simple": view.displayResults,
                  "fullText": view.displayResultsText}
    viewFunct = switchView[args.view]
    print("\nResults: ")
    viewFunct(result, args.vpath)


if __name__ == "__main__":
    analysis_parameters()
