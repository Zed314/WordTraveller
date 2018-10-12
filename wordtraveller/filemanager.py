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
#             print(wordAndOffset[0]+str(readPostList(wordAndOffset[1][0],1,"./workspace/",listPartialPL[nbVoc]).values()[0]))



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
# #e assume that the PLs are sorted by ids
# happen at the end of file
    def combinePostingList(namePLs, offsets, lengths, exitPL, offsetExitPL, workspace = "./workspace/"):

        if len(namePLs) != len(offsets):
            return
        #init
        lengthsDone = []
        idAndScore = SortedDict()
        for nbPL, filename in enumerate(namePLs):
            data = readPostList(offsets[nbPL],1,workspace,filename)
            idAndScore[str(data.keys()[0])+"@"+str(nbPL)]=int(data.values()[0])
            lengthsDone.append(1)
        preID = ""
        idDocCurr = ""
        scoreCurrID = 0
        PLsWithThisDoc = []
        preID  = ""
        while idAndScore:
            keyCurr = idAndScore.keys()[0].split("@")
            numPLProcessed = int(keyCurr[1])
            idDocCurr = keyCurr[0]
            if preID != idDocCurr and preID !="":
                #flush
                print(idDocCurr+", score:"+str(scoreCurrID))
                scoreCurrID = 0
            # print("PLs with this doc (for this word)"+PLsWithThisDoc)
                #now, we combine the PL
    
                PLsWithThisDoc = []
            preID = idDocCurr
            PLsWithThisDoc.append(numPLProcessed)
            scoreCurrID += float(idAndScore.values()[0]) 
            idAndScore.pop(idAndScore.keys()[0])
            #grab the missing one
            data = readPostList(offsets[nbPL]+lengthsDone[numPLProcessed],1,workspace,namePLs[numPLProcessed])
            idAndScore[str(data.keys()[0])+"@"+str(numPLProcessed)]=int(data.values()[0])
            lengthsDone[numPLProcessed] += 1
        # Partial postinglist are organised as such : filename+"..1"+extension+".temp"
    def mergePartialVocsAndPL(self):
        listPartialVOC = []
        listPartialPL = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            for file in filenames:
                if file.endswith(".pl.temp"):
                    print(os.path.join(root, file))
                if file.endswith(".vo.temp"):
                      
        if len(listPartialVOC) != len(listPartialPL):
            return
        nbFiles = len(listPartialVOC)
        wordsAndOffsets = []
        wordsAndOffsets = SortedDict()
        nbLinesRed=[]
        #init words and offsets
        for nbVoc, filenameVoc in enumerate(listPartialVOC):
            file = open(workspace + filenameVoc, "r")
            line = file.readline()
            data = line.rstrip('\n\r').split(",")
            word = data[0]
            offset = int(data[1])
            print("Voc"+str(nbVoc)+", word:"+data[0]+"offset"+data[1])
            wordsAndOffsets[data[0]+"@"+str(nbVoc)]=int(data[1])
            nbLinesRed.append(1)
        preWord = ""
        currWord = ""

        vocsWithThisWord = []
        offsetsCurrWord = []
        while wordsAndOffsets:
            keyCurrWord = wordsAndOffsets.keys()[0].split("@")
            numDocProcessed = int(keyCurrWord[1])
            currWord = keyCurrWord[0]
            if preWord != currWord and currWord !="":
                #flush
                print("Curr word :"+currWord)
                #scoreCurrWord = 0
            #  print("Vocs with this word"+vocsWithThisWord)
                #now, we combine the PL
                filenamesPLWithThisWord = []
                lenghts = []
                for numVoc in vocsWithThisWord:
                    filenamesPLWithThisWord.append(listPartialPL[int(numVoc)])
                    lenghts.append(1)
                #todo :replace 1 with lenghtS
                combinePL(filenamesPLWithThisWord,offsetsCurrWord,lenghts,"eeee",0)
                vocsWithThisWord = []
            preWord = currWord
            vocsWithThisWord.append(numDocProcessed)
    #      scoreCurrWord += float(wordsAndOffsets.values()[1]) 
            offsetsCurrWord.append(int(wordsAndOffsets.values()[1]))
            wordsAndOffsets.pop(wordsAndOffsets.keys()[0])
            #grab the missing one
            file = open(workspace + listPartialVOC[numDocProcessed], "r")
            line = ""
            i = 0
            #todo : optimize this
            while i < nbLinesRed[numDocProcessed]:
                line = file.readline()
                i=i+1
            data = line.rstrip('\n\r').split(",")
            word = data[0]
            offset = int(data[1])
            wordsAndOffsets[data[0]+"@"+str(numDocProcessed)]=int(data[1])
        #    print("Voc"+str(numDocProcessed)+", word:"+data[0]+"offset"+data[1])
            nbLinesRed[numDocProcessed]+=1
        for nbVoc, wordAndOffset in enumerate(wordsAndOffsets):
            if wordAndOffset[0] == minWord[0]:
                print(wordAndOffset[1][0]) #offset
                print(wordAndOffset[1][1]) #offset
                print(wordAndOffset[0]+str(readPostList(wordAndOffset[1][0],1,"./workspace/",listPartialPL[nbVoc]).values()[0]))


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
