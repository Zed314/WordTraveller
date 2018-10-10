import struct
from sortedcontainers import SortedDict
import os

# Record struct format
s = struct.Struct("<lf")

def createWorkspace(path):
    if not os.path.exists(path):
        os.makedirs(path)

#Precondtions: postingList: is a dictionary of Doc Id and Scores.
#              offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
#              workspace: is the folder where we are working in, workspace path should end by an '/'
#Postcondtions: The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>

def savePostList(postingList, offset, workspace="./workspace/"):
    # destination file for writing (w)b

    createWorkspace(workspace)

    if offset == 0:
        file = open(workspace + "postingLites.pl", "w+b")
    else:
        file = open(workspace + "postingLites.pl", "r+b")
    
    try:
        file.read(8*offset)
        # Encode the record and write it to the dest file
        for idDoc, score in postingList.items():
            record = s.pack(idDoc, score)
            file.write(record)

    except IOError:
    	# Your error handling here
    	# Nothing for this example
    	pass
    finally:
        file.close()


#Precondtions: voc: is a dictionary of words and offset.
#              workspace: is the folder where we are working in, workspace path should end by an '/'
#postcondition: the dictionary is saved in vocabulary.vo
def saveVocabulary(voc, workspace="./workspace/"):
    createWorkspace(workspace)

    file = open(workspace + "vocabulary.vo", "w")
    for word, offset in voc.items():
        file.write("{},{}\n".format(word, offset))

#Precondtions: a dictionary is saved in vocabulary.vo
#              workspace: is the folder where we are working in, workspace path should end by an '/'
#post condition: return voc: the a dictionary of words and offset that was saved.
def readVocabulary(workspace="./workspace/"):
    createWorkspace(workspace)

    file = open(workspace + "vocabulary.vo", "r")
    voc = SortedDict()
    for ligne in file:
        donnees = ligne.rstrip('\n\r').split(",")
        word = donnees[0]
        offset = int(donnees[1])
        voc[word] = [offset]
    return voc


#Precondtions: offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
#              length: is the number of paires <Doc Id, Scores> to be read
#              workspace: is the folder where we are working in, workspace path should end by an '/'
#Postcondtions: return a postiong list: a dictionary of Doc Id and Scores red between offet and length.

def readPostList(offset, length, workspace="./workspace/"):
    createWorkspace(workspace)

    #Fille to read
    file = open(workspace + "postingLites.pl", "rb")
    postingList = SortedDict()
    try:
        #test print(file.read(8*24))
        file.read(8*offset)
        for x in range(0, length):
            record = file.read(8)
            filed = s.unpack(record)
            idDoc = filed[0]
            score = filed[1]
            postingList[idDoc]= score
        return postingList
            # Do stuff with record

    except IOError:
            # Your error handling here
            # Nothing for this example
            pass
    finally:
        file.close()

if __name__ == "__main__" :
    postingList = dict()
    postingList[1]=101
    postingList[2]=30023
    postingList[34]=308.0
    postingList[294]=159
    postingList[2324]=3005
    postingList[23445]=3006
    savePostList(postingList,0,"./workspace/")
    #saveVocabulary(postingList)
    postingList[1]=201
    savePostList(postingList,6,"./workspace/")
    postingList[1]=301
    savePostList(postingList,12,"./workspace/")
    pl = readPostList(12,6,"./workspace/")
    #voc = readVocabulary('')
    for numDoc, score in pl.items():
        print("{} => {}.".format(numDoc, score))
