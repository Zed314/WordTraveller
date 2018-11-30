import codecs
from pathlib import Path

from lxml import etree

import gensim
import jieba
import wordtraveller.preprocessing as preprocessing
from gensim.models.word2vec import LineSentence


def read_source_file():
    """ Read the raw newspaper data from ./data/latimes/ and return the content
    of the p tags (after preprocessing)
    Postcondition : Returns a list of words foundt in ./data/latimes
    """
    preprocessor = preprocessing.Preprocessor()
    pathlist = Path("./data/latimes/").glob('**/la*')
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


def separate_word(separated_file):
    """ Helper function to write words into the file located at the path in parameter """
    terms = read_source_file()
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
        print(similary_words)
        for (word, similarity) in similary_words:
            result_words.append(word)
        print(result_words)
    except:
        print("There are some errors!" + w)

    return result_words


def load_models(model_path):
    """ Load model from the file located in model_path 
    Postcondition : Returns the model    
    """
    return gensim.models.Word2Vec.load(model_path)
