import fileManager

def get_posting_list(voc,word):
    offset = voc.get(word)[0]
    length = voc.peekitem(voc.index(word)+1)[1][0]-offset
    return fileManager.readPostList(offset, length)


if __name__ == "__main__" :

    voc = fileManager.readVocabulary()
    print(get_posting_list(voc,"aaa"))
