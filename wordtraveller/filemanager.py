import struct
from sortedcontainers import SortedDict
import os

class FileManager:

    def __init__(self, fileName, workspace="./workspace/"):
        """
        Preconditions:
            filename: the custom filename for the voc and postinglist.
            workspace: is the folder we want to work in. Should have an '/' at the end.
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>
        """
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

    def save_postLists_file(self, postingListsIndex, prefix = ""):
        """
        Preconditions:
            postingListsIndex: is a SortedDict of  words and SortedDict Doc Id and Scores.
            prefix: is a string
        Postconditions:
            The fonction save the pls in a file "prefix+self.postingListsFileName".
        """
        # destination file for wrting (w)b

        file = open(prefix+self.postingListsFileName , "wb")

        try:
            # Encode the record and write it to the dest file
            for word, postingList in postingListsIndex.items():
                for idDoc, score in postingList.items():
                    record = self.struct.pack(idDoc, score)
                    file.write(record)
            print("PL  file saved in : " +prefix+ self.postingListsFileName)
        except IOError:
        	# Your error handling here
        	# Nothing for this example
        	pass
        finally:
            file.close()


    def save_vocabulary(self,voc,prefix = ""):
        """
        Preconditions:
            voc: is a dictionary of words and offset.
        postconditions:
            the dictionary is saved in vocabulary.vo
        """
        file = open(self.vocabularyFileName, "w")
        for word, offset in voc.items():
            file.write("{},{}\n".format(word, offset))
        file.close()
        print("VOC file saved in : " +prefix+ self.vocabularyFileName)


    def save_postList(self, postingList, offset):
        """
        Preconditions:
            postingList: is a dictionary of Doc Id and Scores.
            offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc, the PL will be written affter  it, (offset < size of the file.)
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>,
        """
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


    def read_vocabulary(self):
        """
        Precondtions:
            a dictionary is saved in vocabulary.vo
        Postcondition:
            return voc: the a dictionary of words and offset that was saved.
        """
        file = open(self.vocabularyFileName, "r")
        voc = SortedDict()
        for ligne in file:
            donnees = ligne.rstrip('\n\r').split(",")
            word = donnees[0]
            offset = int(donnees[1])
            voc[word] = [offset]
        file.close()
        return voc

    def read_postList(self, offset, length):
        """
        Precondtions:
            offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
            length: is the number of paires <Doc Id, Scores> to be read
        Postcondtions:
            return a postiong list: a dictionary of Doc Id and Scores red between offet and length.
        """
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
    pl = filemanage.read_postList(0,10)
    #voc = readVocabulary('')
    for numDoc, score in pl.items():
        print("{} => {}.".format(numDoc, score))
