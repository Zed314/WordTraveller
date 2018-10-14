import struct
import os

from sortedcontainers import SortedDict
from os import walk

# # Record struct format
# s = struct.Struct("<lf")

# def createWorkspace(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# #Precondtions: postingList: is a dictionary of Doc Id and Scores.
# #              offet: is the numbers of pairs <Doc Id, Scores> already written in the binary doc
# #              workspace: is the folder where we are working in, workspace path should end by an '/'
# #Postcondtions: The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>
# def savePostList(postingList, offset, workspace="./workspace/", fileName="postingLites.pl"):
#     # destination file for writing (w)b

#     createWorkspace(workspace)

#     if offset == 0:
#         file = open(workspace + fileName, "w+b")
#     else:
#         file = open(workspace + fileName, "r+b")

#     try:
#         file.read(8*offset)
#         # Encode the record and write it to the dest file
#         for idDoc, score in postingList.items():
#             record = s.pack(idDoc, score)
#             file.write(record)

#     except IOError:
#     	# Your error handling here
#     	# Nothing for this example
#     	pass
#     finally:
#         file.close()


# #Precondtions: voc: is a dictionary of words and offset.
# #              workspace: is the folder where we are working in, workspace path should end by an '/'
# #Postconditions: the dictionary is saved in filename
# def saveVocabulary(voc, workspace="./workspace/", fileName="vocabulary.vo"):
#     createWorkspace(workspace)

#     file = open(workspace + fileName, "w")
#     for word, offset in voc.items():
#         file.write("{},{}\n".format(word, offset))

# #Precondtions: a dictionary is saved in vocabulary.vo
# #              workspace: is the folder where we are working in, workspace path should end by an '/'
# #Postconditions: returns voc: the a dictionary of words and offset that was saved.
# def readVocabulary(workspace="./workspace/", fileName="vocabulary.vo"):
#     createWorkspace(workspace)

#     file = open(workspace + fileName, "r")
#     voc = SortedDict()
#     for ligne in file:
#         donnees = ligne.rstrip('\n\r').split(",")
#         word = donnees[0]
#         offset = int(donnees[1])
#         voc[word] = [offset]
#     return voc


# def mergePL(listPartialVOC, listPartialPL, workspace="./workspace/"):
#     if len(listPartialVOC) != len(listPartialPL):
#         return
#     nbFiles = len(listPartialVOC)
#     wordsAndOffsets = []
#     wordsAndOffsets = SortedDict()
#     nbLinesRed=[]
#     #init words and offsets
#     for nbVoc, filenameVoc in enumerate(listPartialVOC):
#         file = open(workspace + filenameVoc, "r")
#         line = file.readline()
#         data = line.rstrip('\n\r').split(",")
#         word = data[0]
#         offset = int(data[1])
#         print("Voc"+str(nbVoc)+", word:"+data[0]+"offset"+data[1])
#         wordsAndOffsets[data[0]+"@"+str(nbVoc)]=int(data[1])
#         nbLinesRed.append(1)
#     preWord = ""
#     currWord = ""
#    # scoreCurrWord = 0
#     vocsWithThisWord = []
#     offsetsCurrWord = []
#     while wordsAndOffsets:
#         keyCurrWord = wordsAndOffsets.keys()[0].split("@")
#         numDocProcessed = int(keyCurrWord[1])
#         currWord = keyCurrWord[0]
#         if preWord != currWord and currWord !="":
#             #flush
#             print("Curr word :"+currWord)
#             #scoreCurrWord = 0
#           #  print("Vocs with this word"+vocsWithThisWord)
#             #now, we combine the PL
#             filenamesPLWithThisWord = []
#             lenghts = []
#             for numVoc in vocsWithThisWord:
#                 filenamesPLWithThisWord.append(listPartialPL[int(numVoc)])
#                 lenghts.append(1)
#             #todo :replace 1 with lenghtS
#             combinePL(filenamesPLWithThisWord,offsetsCurrWord,lenghts,"eeee",0)
#             vocsWithThisWord = []
#         preWord = currWord
#         vocsWithThisWord.append(numDocProcessed)
#   #      scoreCurrWord += float(wordsAndOffsets.values()[1])
#         offsetsCurrWord.append(int(wordsAndOffsets.values()[1]))
#         wordsAndOffsets.pop(wordsAndOffsets.keys()[0])
#         #grab the missing one
#         file = open(workspace + listPartialVOC[numDocProcessed], "r")
#         line = ""
#         i = 0
#         #todo : optimize this
#         while i < nbLinesRed[numDocProcessed]:
#             line = file.readline()
#             i=i+1
#         data = line.rstrip('\n\r').split(",")
#         word = data[0]
#         offset = int(data[1])
#         wordsAndOffsets[data[0]+"@"+str(numDocProcessed)]=int(data[1])
#     #    print("Voc"+str(numDocProcessed)+", word:"+data[0]+"offset"+data[1])
#         nbLinesRed[numDocProcessed]+=1
#     for nbVoc, wordAndOffset in enumerate(wordsAndOffsets):
#         if wordAndOffset[0] == minWord[0]:
#             print(wordAndOffset[1][0]) #offset
#             print(wordAndOffset[1][1]) #offset
#             print(wordAndOffset[0]+str(read_postList(wordAndOffset[1][0],1,"./workspace/",listPartialPL[nbVoc]).values()[0]))


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
    #combine all PL
    def combinePostingList(self, filenamesToProceed, offsets, lengths):

        # init
        lengthsDone = []
        idAndScore = SortedDict()
        for nbPL, filename in enumerate(filenamesToProceed):
            data = self.read_postList(offsets[nbPL], 1, True, nbPL)
            idAndScore[str(data.keys()[0])+"@"+str(nbPL)
                       ] = int(data.values()[0])
            lengthsDone.append(1)
        preID = ""
        idDocCurr = ""
        scoreCurrID = 0
        PLsWithThisDoc = []
        preID = ""
        while idAndScore:
            keyCurr = idAndScore.keys()[0].split("@")
            numPLProcessed = int(keyCurr[1])
            idDocCurr = keyCurr[0]
            if preID != idDocCurr and preID != "":
                # flush
                print(idDocCurr+", score:"+str(scoreCurrID))
                scoreCurrID = 0
            # print("PLs with this doc (for this word)"+PLsWithThisDoc)
                # now, we combine the PL

                PLsWithThisDoc = []
            preID = idDocCurr
            PLsWithThisDoc.append(numPLProcessed)
            scoreCurrID += float(idAndScore.values()[0])
            idAndScore.pop(idAndScore.keys()[0])
            # grab the missing one
            data = read_postList(
                offsets[nbPL]+lengthsDone[numPLProcessed], 1, workspace, namePLs[numPLProcessed])
            idAndScore[str(data.keys()[0])+"@"+str(numPLProcessed)
                       ] = int(data.values()[0])
            lengthsDone[numPLProcessed] += 1
        # Partial postinglist are organised as such : filename+"..1"+extension+".temp"

    def mergePartialVocsAndPL(self):
        #Get all the PLs and VOCs
        listPartialVocs = self.getListPartialVocs()
        listPartialPLs = self.getListPartialPLs()

        
        wordsAndOffsets = []
        wordsAndOffsets = SortedDict()
        nbLinesRedInVOCs = []
        lengthsToReadInPLs = []
        offsetsInPLs = []
        # init words and offsets
        for nbVoc, pathVoc in enumerate(listPartialVocs):
            file = open(pathVoc, "r")
            line = file.readline()
            data = line.rstrip('\n\r').split(",")
            word = data[0]
            offset = int(data[1])
            print("Voc"+str(nbVoc)+", word:"+data[0]+"offset"+data[1])
            wordsAndOffsets[data[0]+"@"+str(nbVoc)] = int(data[1])
            nbLinesRedInVOCs.append(1)
            lengthsToReadInPLs.append(data[1])
            offsetsInPLs.append(0)
        preWord = ""
        currWord = ""

        vocsWithThisWord = []

        while wordsAndOffsets:
            keyCurrWord = wordsAndOffsets.keys()[0].split("@")
            numDocProcessed = int(keyCurrWord[1])
            currWord = keyCurrWord[0]
            if preWord != currWord and currWord != "":
                # flush
                print("Curr word :"+currWord)
                #scoreCurrWord = 0
            #  print("Vocs with this word"+vocsWithThisWord)
                # now, we combine the PL
                filenamesPLWithThisWord = []

                for numVoc in vocsWithThisWord:
                    filenamesPLWithThisWord.append(listPartialPLs[int(numVoc)])
                    lengthsToReadInPLs[numVoc] = int(lengthsToReadInPLs[numVoc]) - offsetsInPLs[numVoc]
                # todo :replace 1 with lengthS
             #   self.combinePostingList(filenamesPLWithThisWord,
                 #         offsetsCurrWord, lenghts, "eeee", 0)
               # self.combinePostingList(filenamesPLWithThisWord,offsetsInPLs,lengthsToReadInPLs)
                vocsWithThisWord = []
            preWord = currWord
            vocsWithThisWord.append(numDocProcessed)
    #      scoreCurrWord += float(wordsAndOffsets.values()[1])
           # offsetsCurrWord.append(int(wordsAndOffsets.values()[0]))
          #  offsetsInPLs[i] = 
            wordsAndOffsets.pop(wordsAndOffsets.keys()[0])
            # grab the missing one
            file = open(listPartialVocs[numDocProcessed], "r")
            line = ""
            i = 0
            # todo : optimize this
            while i < nbLinesRedInVOCs[numDocProcessed]:
                line = file.readline()
                i = i+1
            data = line.rstrip('\n\r').split(",")
            word = data[0]
            if word == "":
                print ("FIN doc" + str(numDocProcessed))
            else: 
                offset = int(data[1]) 
                wordsAndOffsets[data[0]+"@"+str(numDocProcessed)] = int(data[1])
        #    print("Voc"+str(numDocProcessed)+", word:"+data[0]+"offset"+data[1])
                nbLinesRedInVOCs[numDocProcessed] += 1
        for nbVoc, wordAndOffset in enumerate(wordsAndOffsets):
            if wordAndOffset[0] == minWord[0]:
                print(wordAndOffset[1][0])  # offset
                print(wordAndOffset[1][1])  # offset
                print(wordAndOffset[0]+str(read_postList(wordAndOffset[1][0],
                                                        1, True, nbVoc).values()[0]))

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
            if isPartial:
                print("Partial PL file saved in : " +
                      self.getPathPLPartial(self.numberPartialFiles))
            else:
                print("PL file saved in : " + self.getPathPL())
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
        if isPartial:
            print("Partial VOC file save in : " +
                  self.getPathVocPartial(self.numberPartialFiles))
        else:
            print("VOC file saved in : " + self.getPathVoc())

    def save_postList(self, postingList, offset):
        """
        Preconditions:
            postingList: is a dictionary of Doc Id and Scores.
            offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc, the PL will be written affter  it, (offset < size of the file.)
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" paires <Doc Id, Scores>,
        """
        # destination file for redin and wrting (r+)b
        file = open(self.getPathPL(), "r+b")

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
            return a postiong list: a dictionary of Doc Id and Scores red between offet and length.
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
            # test print(file.read(8*24))
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
