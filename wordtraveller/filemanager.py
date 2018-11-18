import struct
import os
import math

from sortedcontainers import SortedDict
from os import walk


class FileManager:
    CONST_SIZE_ON_DISK = 12
        #8
    CONST_SIZE_ON_DISK_EXTENDED = 12
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
        self.struct = struct.Struct("<lff")
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

    def getPathPLScore(self):
        return self.workspace + self.postingListsFileName + ".score" +self.extensionPL

    def getPathPLPartial(self, number):
        return self.workspace + self.postingListsFileName + "." + str(number) + ".temp" + self.extensionPL

    def getPathPLScorePartial(self, number):
        return self.workspace + self.postingListsFileName + "." + str(number) + ".score.temp" + self.extensionPL

    def getListPartialPLsScore(self):
        listPartialPLs = []
        for i in range(0, self.numberPartialFiles):
            listPartialPLs.append(self.getPathPLScorePartial(i))
        return listPartialPLs

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

    # Merge all the partial vocs and pl created during analysis
    def mergePartialVocsAndPL(self, recomputeIDF = True):

        #Get all the PLs and VOCs
        listPartialVocs = self.getListPartialVocs()
        listPartialPLs = self.getListPartialPLs()
        if(self.getListPartialPLs() == []):
            # nothing to do here, exiting
            return

        nbLinesRedInVOCs = []
        totalNumberOfDocs = len (listPartialVocs)
        lengthsToReadInPLs = []
        offsetsInPLs = []
        nbTotalDocuments = 0
        offsetNextWord = []
        offsetPreWord = []
        offsetVoc = 0
        voc = []
        idDocsToRead = []
        extractedVocs = []
        for numberDoc in range(totalNumberOfDocs):
            idDocsToRead.append(True)
            extractedVocs.append(iter((self.read_vocabulary(True, numberDoc)).items()))
       
        for nbVoc, pathVoc in enumerate(listPartialVocs):
            offsetsInPLs.append(0)
            nbLinesRedInVOCs.append(0)
            lengthsToReadInPLs.append(0)
            offsetNextWord.append(0)
            offsetPreWord.append(0)
        currentWords = SortedDict()
        exitVoc = open(self.getPathVoc(), "w+")
        
        while True :
            i = 0
            for numberDoc in range(totalNumberOfDocs):
                if idDocsToRead[numberDoc] == False:
                    continue
                data = []
                try :
                    data = next(extractedVocs[numberDoc])
                    word = data[0]
                except StopIteration:
                    word = "" 
                if word == "": # If document is over.
                    pass
                else: 
                    offsetNextWord[numberDoc] = int(data[1]) 
                    if not (word in currentWords):
                        currentWords[word] = []
                        currentWords[word].append(numberDoc)
                    else:
                        currentWords[word].append(numberDoc)
                idDocsToRead[numberDoc] = False

            if len(currentWords) == 0:
                break

            #Select the best word
            word = currentWords.keys()[0]
            mergingPLs = {}
            #For all the documents with this word
            for idDoc in currentWords[word]:
                preLength = lengthsToReadInPLs[idDoc]
                lengthsToReadInPLs[idDoc] = offsetNextWord[idDoc] - offsetPreWord[idDoc]
                offsetPreWord[idDoc] = offsetNextWord[idDoc]
                offsetsInPLs[idDoc] = offsetsInPLs[idDoc] + preLength
                nbLinesRedInVOCs[idDoc] += 1
                otherPart = self.read_postList(offsetsInPLs[idDoc], lengthsToReadInPLs[idDoc], True, idDoc)
                mergingPLs.update(otherPart)
                idDocsToRead[idDoc] = True
                
            if word == "***NumberDifferentDocs***":
                nbTotalDocuments = len(mergingPLs)
            
            offsetVoc += len(mergingPLs)
            exitVoc.write("{},{}\n".format(word, offsetVoc))
            
            if recomputeIDF:
                for idfAndScore in mergingPLs.values():
                    idfAndScore[0]=(1+math.log(idfAndScore[1]))*math.log(nbTotalDocuments/(1+len(mergingPLs)))
            
            self.save_postList(mergingPLs)
            self.save_postList_by_score(mergingPLs)
            currentWords.pop(word)
        # Close voc file
        exitVoc.close()
        for pathVoc in listPartialVocs:
            os.remove(pathVoc)
        for pathPL in listPartialPLs:
            os.remove(pathPL)




    def save_postLists_from_complete_voc(self, completeVoc, isPartial=False, numberPart=-1):
        """
        Preconditions:
            postingListsIndex: is an sorted array of  words and unsorted dict of Doc Id and Scores.
        Postconditions:
            The fonction save the pls in a partial or full pl file.
            If not partial, the posting list is also stored by score
        """
        if numberPart == -1:
            numberPart = self.numberPartialFiles
        for word, unsortedPL in completeVoc:
            #TODO enable is partial there
            self.save_postList(unsortedPL,isPartial=isPartial, numberPart = numberPart)
            if not isPartial:
                self.save_postList_by_score(unsortedPL)

    # Save vocabulary that contains both voc and pls
    def save_vocabularyAndPL_file(self, voc, isPartial=False):
        """
        Preconditions:
            voc: is a SortedDict of  words and SortedDict Doc Id and Scores.
        Postconditions:
            The function saves the vocs in a file named self.postingListsFileName 
            pls in a file "self.postingListsFileName".
        """
        # map vocabulary offset
        vocabulary = []
        current_offset = 0
        # save all the posting lists

        # we sort voc, returns only the keys !
        sortedArrayOfVoc = sorted(voc.items())

        # we sort the PLs inside voc in the functions save_postLists_from_complete_voc
        
        for word, unsortedPl in sortedArrayOfVoc:
            current_offset += len(unsortedPl)
            vocabulary.append((word, current_offset))

        # saving the posting lists
        self.save_postLists_from_complete_voc(sortedArrayOfVoc, isPartial)
        # save the vocabulary
        self.save_vocabulary(vocabulary, isPartial)
        if isPartial:
            self.numberPartialFiles += 1

    def save_vocabulary(self, voc, isPartial=False):
        """
        Preconditions:
            voc: is a sorted array of words and offset.
        postconditions:
            the dictionary is saved in vocabulary.vo
        """
        if isPartial:
            file = open(self.getPathVocPartial(self.numberPartialFiles), "w")
        else:
            file = open(self.getPathVoc(), "w")
        for word, offset in voc:
            file.write("{},{}\n".format(word, offset))
        file.close()
    
    def save_postList_by_score(self, postingList, offset = -1):
        """ Save the postingList of A word after ordered it by score in
        non ascending order """
        # destination file for redin and wrting (r+)b
        if(offset == -1):
            # Append
            file = open(self.getPathPLScore(),"a+b")
            offset = 0
        else:
            file = open(self.getPathPLScore(), "w+b")

        try:
            if(offset!=0):
                file.seek(self.CONST_SIZE_ON_DISK*offset)
            # Encode the record and write it to the dest file
            for idDoc, score in sorted(postingList.items(),  key = lambda s: (-s[1][0],s[0]) ):
                record = self.struct.pack(idDoc, score[0], score[1])
                file.write(record)

        except IOError:
            pass
        finally:
            file.close()
            
    def save_postList(self, postingList, offset=-1, isPartial = False, numberPart = 0):
        """
        Preconditions:
            postingList: is a dictionary of Doc Id and Scores.
            offset: is the numbers of paires <Doc Id, Scores> alredy written in the binary doc, the PL will be written affter  it, (offset < size of the file.)
                    if == -1, we append
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" pairs <Doc Id, Scores>,
        """
        # destination file for redin and wrting (r+)b
        if(offset == -1) and not isPartial:
            # Append
            file = open(self.getPathPL(),"a+b")
            offset = 0
        elif not isPartial:
            file = open(self.getPathPL(), "w+b")
        elif isPartial : # we do not append to partial files
            file = open(self.getPathPLPartial(numberPart),"a+b")
            

        try:
            if(offset>0):
                file.seek(self.CONST_SIZE_ON_DISK*offset)
            # Encode the record and write it to the dest file
            for idDoc, score in sorted(postingList.items()):
                record = self.struct.pack(idDoc, score[0], score[1])
                file.write(record)

        except IOError:
            pass
        finally:
            file.close()

    # Save vocabulary that contains number of occurencies
    # The voc and pl are saved to filename+"."+number+"."+extension+".temp"
    def savePartialVocabularyAndPL(self, voc):
        """
        Preconditions:
            voc: is a arraay of  words and SortedDict Doc Id and Scores.
        """
        self.numberPartialFiles += 1
        self.save_vocabularyAndPL_file(voc, True)
        pass

    def read_vocabulary(self, isPartial=False, number=0):
        """
        Precondtions:
            a dictionary is saved in vocabulary.vo
        Postcondition:
            return voc: the a dictionary of words and offset that was saved.
        """

        if isPartial:
            filename = self.getPathVocPartial(number) 
        else:
            filename = self.getPathVoc()
        file = open(filename, "r")
        voc = SortedDict()
        for ligne in file:
            donnees = ligne.rstrip('\n\r').split(",")
            word = donnees[0]
            offset = int(donnees[1])
            voc[word] = offset

        file.close()
        return voc

    def read_postList(self, offset, length, isPartial=False, number=0, returnPostingListOrderedByScore = False):
        """
        Precondtions:
            offet: is the numbers of paires <Doc Id, Scores> alredy witten in the binary doc
            length: is the number of paires <Doc Id, Scores> to be read
        Postcondtions:
            return a posting list: a dictionary of Doc Id and Scores red between offet and length.
            return also a posting list sorted by scores : an array of   
        """
        # File to read
        if isPartial:
            filename = self.getPathPLPartial(number) 
        else:
            filename = self.getPathPL()
        file = open(filename, "rb")
        if returnPostingListOrderedByScore:
            filePLScore = open(self.getPathPLScore(), "rb")
        postingList = SortedDict()
        postingListByScore = []
        try:

            file.seek(self.CONST_SIZE_ON_DISK*offset)
            if (returnPostingListOrderedByScore):
                filePLScore.seek(self.CONST_SIZE_ON_DISK*offset)
            for x in range(0, length):
                record = file.read(self.CONST_SIZE_ON_DISK)
                filed = self.struct.unpack(record)
                idDoc = filed[0]
                score = filed[1]
                nbOccurenciesInDoc = filed[2]
                postingList[idDoc] = [score,nbOccurenciesInDoc]
                if (returnPostingListOrderedByScore):
                    record = filePLScore.read(self.CONST_SIZE_ON_DISK)
                    filed = self.struct.unpack(record)
                    idDoc = filed[0]
                    score = filed[1]
                    nbOccurenciesInDoc = filed[2]
                    #todo replace all over the code
                    # if len(postingListByScore) == 0:
                    #     postingListByScore.append((score,[idDoc]))
                    # elif score == postingListByScore[-1][0]:
                    #     postingListByScore[-1][1].append(idDoc)
                    # else:
                    #     postingListByScore.append((score,[idDoc]))
                    postingListByScore.append((score,idDoc))

            if returnPostingListOrderedByScore :
                return postingList, postingListByScore
            else :
                return postingList

        except IOError:
                # Your error handling here
                # Nothing for this example
            pass
        finally:
            file.close()


