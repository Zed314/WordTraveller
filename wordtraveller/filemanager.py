import struct
from sortedcontainers import SortedDict
import os

class FileManager:

    def __init__(self, fileName, workspace="./workspace/"):
        self.vocabularyFileName = workspace + fileName + ".vo"
        self.postingListsFileName = workspace + fileName + ".pl"
        # Record struct format
        self.struct = struct.Struct("<lf")
        # create the workspace
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        # create the files
        if not os.path.isfile(self.vocabularyFileName) :
            file = open(self.vocabularyFileName, "wb")
            file.close()
        if not os.path.isfile(self.postingListsFileName) :
            file = open(self.postingListsFileName, "wb")
            file.close()

    def save_postLists_file(self, postingListsIndex):
        # destination file for wrting (w)b

        file = open(self.postingListsFileName , "wb")

        try:
            # Encode the record and write it to the dest file
            for word, postingList in postingListsIndex.items():
                for idDoc, score in postingList.items():
                    record = self.struct.pack(idDoc, score)
                    file.write(record)
            print("PL  file saved in : " + self.postingListsFileName)
        except IOError:
        	# Your error handling here
        	# Nothing for this example
        	pass
        finally:
            file.close()

    #Precondtions: postingList: is a dictionary of Doc Id and Scores.
    #              offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
    #              workspace: is the folder where we are working in, workspace path should end by an '/'
    #Postcondtions: The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>
    def save_postList(self, postingList, offset):
        # destination file for redin and wrting (r+)b
        file = open(self.postingListsFileName, "r+b")

        try:
            file.read(8*offset)
            # Encode the record and write it to the dest file
            for idDoc, score in postingList.items():
                record = self.struct.pack(idDoc, score)
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
    def save_vocabulary(self,voc):
        file = open(self.vocabularyFileName, "w")
        for word, offset in voc.items():
            file.write("{},{}\n".format(word, offset))
        file.close()
        print("VOC file saved in : " + self.vocabularyFileName)

    #Precondtions: a dictionary is saved in vocabulary.vo
    #              workspace: is the folder where we are working in, workspace path should end by an '/'
    #post condition: return voc: the a dictionary of words and offset that was saved.
    def read_vocabulary(self):

        file = open(self.vocabularyFileName, "r")
        voc = SortedDict()
        for ligne in file:
            donnees = ligne.rstrip('\n\r').split(",")
            word = donnees[0]
            offset = int(donnees[1])
            voc[word] = [offset]
        file.close()
        return voc

    #Precondtions: offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
    #              length: is the number of paires <Doc Id, Scores> to be read
    #              workspace: is the folder where we are working in, workspace path should end by an '/'
    #Postcondtions: return a postiong list: a dictionary of Doc Id and Scores red between offet and length.
    def read_postList(self, offset, length):


        #Fille to read
        file = open(self.postingListsFileName, "rb")
        postingList = SortedDict()
        try:
            #test print(file.read(8*24))
            file.read(8*offset)
            for x in range(0, length):
                record = file.read(8)
                filed = self.struct.unpack(record)
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
    filemanage = FileManager("test1","./workspace/" )
    postingList = dict()
    postingList[1]=101
    postingList[2]=30023
    postingList[34]=308.0
    postingList[294]=159
    postingList[2324]=3005
    postingList[23445]=3006
    filemanage.save_postList(postingList,0)
    #saveVocabulary(postingList)
    postingList[1]=201
    filemanage.save_postList(postingList,6)
    postingList[1]=301
    filemanage.save_postList(postingList,12)
    pl = filemanage.read_postList(12,6)
    #voc = readVocabulary('')
    for numDoc, score in pl.items():
        print("{} => {}.".format(numDoc, score))
