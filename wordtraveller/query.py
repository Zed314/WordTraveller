from . import filemanager
from sortedcontainers import SortedDict

def get_posting_list(voc, word, fileManager):
    if word in voc:
        index = voc.index(word)
        if index == 0:
            offset = 0
            length = voc.get(word)[0]
        else:
            offset = voc.peekitem(voc.index(word)-1)[1][0]
            length = voc.get(word)[0] - offset
        return fileManager.read_postList(offset, length)
    else:
        return SortedDict()



if __name__ == "__main__" :

    # TODO: cacher le filemanager, dés l'exterior, on ne devrait que acceder à analysis et a query
    fileManager = filemanager.FileManager("test1","./workspace/")
    voc = fileManager.read_vocabulary()
    print(get_posting_list(voc,"aaa", fileManager ))
