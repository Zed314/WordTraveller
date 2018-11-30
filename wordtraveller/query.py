import wordtraveller.filemanager as filemanager
from sortedcontainers import SortedDict

def get_posting_list(voc, word, fileManager, returnPostingListOrderedByScore = False, sorted=False):
    if word in voc:
        index = voc.index(word)
        if index == 0:
            offset = 0
            length = voc.get(word)
        else:
            offset = voc.peekitem(voc.index(word)-1)[1]
            length = voc.get(word) - offset
        return fileManager.read_postList(offset, length, returnPostingListOrderedByScore=returnPostingListOrderedByScore,sorted=sorted)
    else:
        if(returnPostingListOrderedByScore):
            return SortedDict(), SortedDict()
        else:
            return SortedDict()
