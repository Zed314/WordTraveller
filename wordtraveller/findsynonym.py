import codecs
import jieba
import gensim
from gensim.models.word2vec import LineSentence
import wordtraveller.preprocessing as preprocessing
from lxml import etree
from pathlib import Path



def read_source_file():
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

    file_write = codecs.open(target_file_name, 'w+', 'utf-8')
    file_write.writelines(content)
    print("Write sussfully!")
    file_write.close()


def separate_word(separated_file):
    print("separate_word")
    terms = read_source_file()
    word_line = ' '.join(terms)
    output = codecs.open(separated_file, 'w', 'utf-8')
    output.write(word_line)
    output.close()
    return separated_file


def build_model(source_separated_words_file,model_path):

    print("start building...",source_separated_words_file)
    model = gensim.models.Word2Vec(LineSentence(source_separated_words_file), size=200, window=5, min_count=5, alpha=0.02, workers=4)
    model.save(model_path)
    print("build successful!", model_path)
    return model

def get_similar_words_str(w, model, topn = 10):
    result_words = get_similar_words_list(w, model)
    return str(result_words)


def get_similar_words_list(w, model, topn = 10):
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
    return gensim.models.Word2Vec.load(model_path)

if "__name__ == __main__()":
    separated_file = "./tests/workspace/testSyn.txt" # separeted words file
    model_path = "./tests/workspace/model" # model file

    #source_separated_words_file = separate_word(separated_file)
    #source_separated_words_file = separated_file    # if separated word file exist, don't separate_word again
    #build_model(source_separated_words_file, model_path)# if model file is exist, don't buile modl

    model = load_models(model_path)
    words = get_similar_words_str('red', model)
    print(words)
