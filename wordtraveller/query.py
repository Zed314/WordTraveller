from . import filemanager

def get_posting_list(voc, word, workspace):
    offset = voc.get(word)[0]
    length = voc.peekitem(voc.index(word)+1)[1][0]-offset
    return filemanager.readPostList(offset, length, workspace)


if __name__ == "__main__" :

    # TODO: cacher le filemanager, dés l'exterior, on ne devrait que acceder à analysis et a query
    voc = filemanager.readVocabulary("./workspace/")
    print(get_posting_list(voc,"aaa", "./workspace/"))
