import struct
import os

from sortedcontainers import SortedDict
from os import walk


class FileManager:

    def __init__(self, fileName, workspace="./workspace/"):
        """
        Preconditions:
            filename: the custom filename for the voc and postinglist.
            workspace: is the folder we want to work in. Should have an '/' at the end.
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>
        """
        self.vocabularyFileName = fileName
        self.postingListsFileName = fileName
        self.workspace = workspace
        self.numberPartialFiles = 0
        self.extensionVoc = ".vo"
        self.extensionPL = ".pl"
        # Record struct format
        self.struct = struct.Struct("<lf")
        # create the workspace
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        # create the files
        if not os.path.isfile(self.getPathVoc()):
            file = open(self.getPathVoc(), "wb")
            file.close()
        if not os.path.isfile(self.getPathPL()):
            file = open(self.getPathPL(), "wb")
            file.close()
# #e assume that the PLs are sorted by ids
# happen at the end of file

    def getPathVoc(self):
        return self.workspace + self.vocabularyFileName + self.extensionVoc

    def getPathVocPartial(self, number):
        return self.workspace + self.vocabularyFileName + "." + str(number) + ".temp" + self.extensionVoc

    def getPathPL(self):
        return self.workspace + self.postingListsFileName + self.extensionPL

    def getPathPLPartial(self, number):
        return self.workspace + self.postingListsFileName + "." + str(number) + ".temp" + self.extensionPL

    def getListPartialPLs(self):
        listPartialPLs = []
        for i in range(0, self.numberPartialFiles):
            listPartialPLs.append(self.getPathPLPartial(i))
        return listPartialPLs

    def getListPartialVocs(self):
        listPartialVocs = []
        for i in range(0, self.numberPartialFiles):
            listPartialVocs.append(self.getPathVocPartial(i))
        return listPartialVocs

    def mergePartialVocsAndPL(self):
        #Get all the PLs and VOCs
        listPartialVocs = self.getListPartialVocs()
        listPartialPLs = self.getListPartialPLs()

        
 
        nbLinesRedInVOCs = []
        totalNumberOfDocs = len (listPartialVocs)
        lengthsToReadInPLs = []
        offsetsInPLs = []
        
        documentsCurrentlyProccessed = len(listPartialVocs)
        offsetNextWord = []
        offsetPreWord = []
        offsetVoc = 0
        voc = []
        for nbVoc, pathVoc in enumerate(listPartialVocs):
            offsetsInPLs.append(0)
            nbLinesRedInVOCs.append(0)
            lengthsToReadInPLs.append(0)
            offsetNextWord.append(0)
            offsetPreWord.append(0)
        currentWords = SortedDict()
        fileVoc = open(self.getPathVoc(), "w+")
        while True :
            i = 0
           # currentWords = SortedDict()
            #Todo : optimize
            for numberDoc in range(totalNumberOfDocs):
                i = 0
                line = ""
                file = open(listPartialVocs[numberDoc], "r")
                while i < nbLinesRedInVOCs[numberDoc]:
                    file.readline()
                    i = i+1
                line = file.readline()
                i = i+1
                data = line.rstrip('\n\r').split(",")
                word = data[0]
                if word == "":
                    pass
                else: 
                    
                    offsetNextWord[numberDoc] = int(data[1]) 

                    if not (word in currentWords):
                        currentWords[word] = []
                        currentWords[word].append(numberDoc)
                    else:
                        currentWords[word].append(numberDoc)
                file.close()

            if len(currentWords) == 0:
                break
            word = currentWords.keys()[0]

            mergingPLs = SortedDict()
            for idDoc in currentWords[word]:
                preLength = lengthsToReadInPLs[idDoc]
                lengthsToReadInPLs[idDoc] = offsetNextWord[idDoc] - offsetPreWord[idDoc]
                offsetPreWord[idDoc] = offsetNextWord[idDoc]
                offsetsInPLs[idDoc] = offsetsInPLs[idDoc] + preLength
                nbLinesRedInVOCs[idDoc] += 1
                otherPart = self.read_postList(offsetsInPLs[idDoc], lengthsToReadInPLs[idDoc], True, idDoc)

                mergingPLs.update(otherPart)
                
            self.save_postList(mergingPLs)

            offsetVoc += len(mergingPLs)
            
          #  voc.append([word,offsetVoc])
            fileVoc.write("{},{}\n".format(word, offsetVoc))
            currentWords.pop(word)
        fileVoc.close()
    def save_postLists_file(self, postingListsIndex, isPartial=False):
        """
        Preconditions:
            postingListsIndex: is a SortedDict of  words and SortedDict Doc Id and Scores.
            prefix: is a string
        Postconditions:
            The fonction save the pls in a file "prefix+self.postingListsFileName".
        """
        # destination file for wrting (w)b
        path = ""
        if isPartial:
            path = self.getPathPLPartial(self.numberPartialFiles)
        else:
            path = self.getPathPL()

        file = open(path, "w+b")

        try:
            # Encode the record and write it to the dest file
            for word, postingList in postingListsIndex.items():
                for idDoc, score in postingList.items():
                    record = self.struct.pack(idDoc, score)
                    file.write(record)
        except IOError:
            print("Error during the writing")
            pass
        finally:
            file.close()

    # Save vocabulary that contains both voc and pls
    def save_vocabularyAndPL_file(self, voc, isPartial=False):
        """
        Preconditions:
            voc: is a SortedDict of  words and SortedDict Doc Id and Scores.
            prefix: is a string
        Postconditions:
            The fonction save the vocs in a file named self.postingListsFileName 
            pls in a file "self.postingListsFileName".
        """
        # map vocabulary offset
        vocabulary = SortedDict()
        current_offset = 0
        # save all the posting lists
        # TODO make a btter call to the consturctore "filemanager.FileManager(..,..) seems a bit wirde

        for word, pl in voc.items():
            current_offset += len(pl)
            vocabulary[word] = current_offset

        # saving the plsting lists
        self.save_postLists_file(voc, isPartial)
        # save the vocabulary
        self.save_vocabulary(vocabulary, isPartial)
        if isPartial:
            self.numberPartialFiles += 1

    def save_vocabulary(self, voc, isPartial=False):
        """
        Preconditions:
            voc: is a dictionary of words and offset.
        postconditions:
            the dictionary is saved in vocabulary.vo
        """
        if isPartial:
            file = open(self.getPathVocPartial(self.numberPartialFiles), "w")
        else:
            file = open(self.getPathPL(), "w")
        for word, offset in voc.items():
            file.write("{},{}\n".format(word, offset))
        file.close()

    def save_postList(self, postingList, offset=-1):
        """
        Preconditions:
            postingList: is a dictionary of Doc Id and Scores.
            offset: is the numbers of paires <Doc Id, Scores> alredy written in the binary doc, the PL will be written affter  it, (offset < size of the file.)
                    if == -1, we append
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>,
        """
        # destination file for redin and wrting (r+)b
        if(offset == -1):
            file = open(self.getPathPL(),"a+b")
            offset = 0
        else:
            file = open(self.getPathPL(), "w+b")

        try:
            if(offset!=0):
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

    # Save vocabulary that contains number of occurencies
    # The voc and pl are saved to filename+"."+number+"."+extension+".temp"
    def savePartialVocabulary(self, voc):
        numberPartialFiles += 1
        self.save_vocabularyAndPL_file(voc, True)
        pass

    def read_vocabulary(self):
        """
        Precondtions:
            a dictionary is saved in vocabulary.vo
        Postcondition:
            return voc: the a dictionary of words and offset that was saved.
        """
        file = open(self.getPathVoc(), "r")
        voc = SortedDict()
        for ligne in file:
            donnees = ligne.rstrip('\n\r').split(",")
            word = donnees[0]
            offset = int(donnees[1])
            voc[word] = [offset]

        file.close()
        return voc

    def read_postList(self, offset, length, isPartial=False, number=0):
        """
        Precondtions:
            offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
            length: is the number of paires <Doc Id, Scores> to be read
        Postcondtions:
            return a posting list: a dictionary of Doc Id and Scores red between offet and length.
        """
        # File to read
        filename = ""
        if isPartial:
            filename = self.getPathPLPartial(number) 
        else:
            filename = self.getPathPL()

        file = open(filename, "rb")
        postingList = SortedDict()
        try:

            file.read(8*offset)

            for x in range(0, length):
                record = file.read(8)
                filed = self.struct.unpack(record)
                idDoc = filed[0]
                score = filed[1]
                postingList[idDoc] = score
            return postingList
            # Do stuff with record

        except IOError:
                # Your error handling here
                # Nothing for this example
            pass
        finally:
            file.close()


if __name__ == "__main__":
    filemanage = FileManager("test1", "./workspace/")
    postingList = dict()
    postingList[1] = 101
    postingList[2] = 30023
    postingList[34] = 308.0
    postingList[294] = 159
    postingList[2324] = 3005
    postingList[23445] = 3006
    filemanage.save_postList(postingList, 0)
    # saveVocabulary(postingList)
    postingList[1] = 201
    filemanage.save_postList(postingList, 6)
    postingList[1] = 301
    filemanage.save_postList(postingList, 12)
    pl = filemanage.read_postList(0, 10)
    #voc = readVocabulary('')
    for numDoc, score in pl.items():
        print("{} => {}.".format(numDoc, score))
