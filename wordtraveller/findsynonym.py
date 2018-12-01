import codecs
from pathlib import Path
import nltk

from lxml import etree

import gensim
import argparse
import wordtraveller.preprocessing as preprocessing
from gensim.models.word2vec import LineSentence


def read_source_file(path):
    """ Read the raw newspaper data from ./data/latimes/ and return the content
    of the p tags (after preprocessing)
    Postcondition : Returns a list of words foundt in ./data/latimes
    """
    preprocessor = preprocessing.Preprocessor(True)
    pathlist = Path(path).glob('**/la*')
    terms = []
    for i, newspaper_path in enumerate(pathlist):
        raw = newspaper_path.read_text()
        tree = etree.fromstring("<NEWSPAPER>" + raw + "</NEWSPAPER>")
        for document in tree.xpath("//DOC"):
            text = ""
            for p in document.xpath("./TEXT/P"):
                text += p.text
            terms[len(terms):len(terms)] = preprocessor.process(text)
    return terms


def write_file(target_file_name, content):
    """ Write the content into a file 
    Preconditions : 
        target_file_name : path to the file
        content : the string to write
    """
    file_write = codecs.open(target_file_name, 'w+', 'utf-8')
    file_write.writelines(content)
    print("Write sussfully!")
    file_write.close()


def separate_word(separated_file, path = "./data/latimes/"):
    """ Helper function to write words into the file located at the path in parameter """
    terms = read_source_file(path)
    word_line = ' '.join(terms)
    output = codecs.open(separated_file, 'w', 'utf-8')
    output.write(word_line)
    output.close()
    return separated_file


def build_model(source_separated_words_file, model_path):
    """ Build the model and write it into model_path based on the data from source_separated_words_file.
    """

    print("start building...", source_separated_words_file)
    model = gensim.models.Word2Vec(LineSentence(
        source_separated_words_file), size=200, window=5, min_count=5, alpha=0.02, workers=4)
    model.save(model_path)
    print("build successful!", model_path)
    return model


def get_similar_words_str(w, model, topn=10):
    """ Get the topn words similar to w based on the model.
        Postconditions: Return the similar words in a string
    """
    result_words = get_similar_words_list(w, model)
    return str(result_words)


def get_similar_words_list(w, model, topn=10):
    """ Get the topn words similar to w based on the model.
        Postconditions: Return the similar words in a list
    """
    result_words = []
    try:
        similary_words = model.most_similar(w, topn=10)
        for (word, similarity) in similary_words:
            result_words.append(word)
    except:
        print("There are some errors!" + w)

    return result_words


def load_models(model_path):
    """ Load model from the file located in model_path 
    Postcondition : Returns the model    
    """
    return gensim.models.Word2Vec.load(model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=str,
                        help="dossier avec les documents à entraîner")
    parser.add_argument("-f", type=str,
                        help="nom de modèle entraîné ", required=True)
    parser.add_argument("-t", type=str,
                        help="term pour chercher les termes plus proches ", required=True)
    parser.add_argument("-n", type=str, required=True,
                        help='nombre de synonymes pour la requête')

    args = parser.parse_args()
    path = args.d

    separated_file = "./workspace/separated_words.txt"  # separeted words file
    model_path = "./workspace/" + args.f # model file
    print(model_path)

    if args.d:
        source_separated_words_file = separate_word(separated_file, args.d)
        source_separated_words_file = separated_file  # if separated word file exist, don't separate_word again
        build_model(source_separated_words_file, model_path)  # if model file is exist, don't buile modl

    model = load_models(model_path)
    word = nltk.stem.PorterStemmer().stem(args.t)
    words = get_similar_words_str(word, model)
    print(words)