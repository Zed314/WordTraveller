from . import filemanager
from sortedcontainers import SortedDict

def get_posting_list(voc, word, fileManager, returnPostingListOrderedByScore = False):
    if word in voc:
        index = voc.index(word)
        if index == 0:
            offset = 0
            length = voc.get(word)
        else:
            offset = voc.peekitem(voc.index(word)-1)[1]
            length = voc.get(word) - offset
        return fileManager.read_postList(offset, length, returnPostingListOrderedByScore=returnPostingListOrderedByScore)
    else:
        if(returnPostingListOrderedByScore):
            return SortedDict(), SortedDict()
        else:
            return SortedDict()



if __name__ == "__main__" :

    # TODO: cacher le filemanager, dés l'exterior, on ne devrait que acceder à analysis et a query
    fileManager = filemanager.FileManager("test1","./workspace/")
    voc = fileManager.read_vocabulary()
    print(get_posting_list(voc,"aaa", fileManager ))
