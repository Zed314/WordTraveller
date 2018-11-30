import math
import os
import struct

import numpy as np
from sortedcontainers import SortedDict


class FileManager:
    CONST_SIZE_ON_DISK = 12

    def __init__(self, fileName, workspace="./workspace/"):
        """
        Preconditions:
            filename: the custom filename for the voc and postinglist.
            workspace: is the folder we want to work in. Should have an '/' at the end.
        Postconditions:
            Create the voc file, posting list ordered by id and posting list ordered by score if they do not exist yet
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
        if not os.path.isfile(self.getPathPLScore()):
            file = open(self.getPathVoc(), "wb")
            file.close()

    def getPathVoc(self):
        return self.workspace + self.vocabularyFileName + self.extensionVoc

    def getPathVocPartial(self, number):
        return self.workspace + self.vocabularyFileName + "." + str(number) + ".temp" + self.extensionVoc

    def getPathPL(self):
        return self.workspace + self.postingListsFileName + self.extensionPL

    def getPathRandomIndexing(self):
        return self.workspace + self.vocabularyFileName + '.ri'

    def getPathRandomIndexingVO(self):
        return self.workspace + self.vocabularyFileName + '.vori'

    def getPathPLScore(self):
        return self.workspace + self.postingListsFileName + ".score" + self.extensionPL

    def doesCompressedVersionExists(self):
        return os.path.isfile(self.getPathVocCompressed()+".gz") and os.path.isfile(self.getPathPLCompressed()+".gz") and os.path.isfile(self.getPathPLScore()+".gz")

    def doesUnCompressedVersionExists(self):
        return os.path.isfile(self.getPathVoc()) and os.path.isfile(self.getPathPL()) and os.path.isfile(self.getPathPLScore())

    def getPathVocCompressed(self):
        return self.getPathVoc()+".compressed"

    def getPathPLCompressed(self):
        return self.getPathPL()+".compressed"

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

    def mergePartialVocsAndPL(self, recomputeIDF=True):
        """ Merge all the partial vocs and pl created during analysis 
        Preconditions: 
            recomputeIDF : wether or not we should recompute the idf in the end, otherwise the idfs will be equal to zero.

        Postconditions: 
            A merged vocabulary file and posting list ordered by id is created. A posting list ordered by score is created.
        """
        # Get all the PLs and VOCs
        listPartialVocs = self.getListPartialVocs()
        listPartialPLs = self.getListPartialPLs()
        if (self.getListPartialPLs() == []):
            # nothing to do here, exiting
            return

        nbLinesRedInVOCs = []
        totalNumberOfDocs = len(listPartialVocs)
        lengthsToReadInPLs = []
        offsetsInPLs = []
        nbTotalDocuments = 0
        offsetNextWord = []
        offsetPreWord = []
        offsetVoc = 0

        idDocsToRead = []
        extractedVocs = []

        plFiles = []
        plScoreOutputFile = open(self.getPathPLScore(), "w+b")
        plOutputFile = open(self.getPathPL(), "w+b")

        for numberDoc in range(totalNumberOfDocs):
            idDocsToRead.append(True)
            extractedVocs.append(
                iter((self.read_vocabulary(True, numberDoc)).items()))
            offsetsInPLs.append(0)
            nbLinesRedInVOCs.append(0)
            lengthsToReadInPLs.append(0)
            offsetNextWord.append(0)
            offsetPreWord.append(0)

        for pathPL in self.getListPartialPLs():
            plFiles.append(open(pathPL, "rb"))

        currentWords = dict()
        exitVoc = open(self.getPathVoc(), "w+")

        while True:

            for numberDoc in range(totalNumberOfDocs):
                if idDocsToRead[numberDoc] == False:
                    continue
                data = []
                try:
                    data = next(extractedVocs[numberDoc])
                    word = data[0]
                except StopIteration:
                    word = ""
                if word == "":  # If document is over.
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

            # Select the best word
            word = sorted(currentWords)[0]
            mergingPLs = {}
            # For all the documents with this word
            for idDoc in currentWords[word]:
                preLength = lengthsToReadInPLs[idDoc]
                lengthsToReadInPLs[idDoc] = offsetNextWord[idDoc] - \
                    offsetPreWord[idDoc]
                offsetPreWord[idDoc] = offsetNextWord[idDoc]
                offsetsInPLs[idDoc] = offsetsInPLs[idDoc] + preLength
                nbLinesRedInVOCs[idDoc] += 1
                otherPart = self.read_postList(
                    offsetsInPLs[idDoc], lengthsToReadInPLs[idDoc], True, idDoc,  sorted=False, filePL=plFiles[idDoc])
                mergingPLs.update(otherPart)
                idDocsToRead[idDoc] = True

            if word == "***NumberDifferentDocs***":
                nbTotalDocuments = len(mergingPLs)

            offsetVoc += len(mergingPLs)
            exitVoc.write("{},{}\n".format(word, offsetVoc))

            if recomputeIDF:
                for idfAndScore in mergingPLs.values():
                    idfAndScore[0] = (1 + math.log(idfAndScore[1])) * \
                        math.log(nbTotalDocuments / (1 + len(mergingPLs)))

            self.save_postList(mergingPLs, filePL=plOutputFile)
            self.save_postList_by_score(
                mergingPLs, filePlScore=plScoreOutputFile)
            currentWords.pop(word)
        # Close files
        plOutputFile.close()
        exitVoc.close()
        plScoreOutputFile.close()
        for filePL in plFiles:
            filePL.close()
        # Delete temporary files
        for pathVoc in listPartialVocs:
            os.remove(pathVoc)
        for pathPL in listPartialPLs:
            os.remove(pathPL)

    def save_postLists_from_complete_voc(self, completeVoc, isPartial=False, numberPart=-1):
        """
        Preconditions:
            completeVoc: is an sorted list of words and unsorted dict of Doc Id and Scores.
            isPartial: notify whether or not we are saving a partial inverted file
            numberPart: the number of the partial file
        Postconditions:
            The fonction save completeVoc in a partial or full inverted file.
            If not partial, the posting list is also sorted by score and stored.
        """
        if numberPart == -1:
            numberPart = self.numberPartialFiles

        if not isPartial:
            plFile = open(self.getPathPL(), "w+b")
            scoreFile = open(self.getPathPLScore(), "w+b")
        else:
            plFile = open(self.getPathPLPartial(numberPart), "a+b")

        for word, unsortedPL in completeVoc:

            self.save_postList(unsortedPL, isPartial=isPartial,
                               numberPart=numberPart, filePL=plFile)

            if not isPartial:
                self.save_postList_by_score(unsortedPL, filePlScore=scoreFile)
        if not isPartial:
            plFile.close()
            scoreFile.close()
        else:
            plFile.close()

    def save_vocabularyAndPL_file(self, voc, isPartial=False):
        """
        Save invertedFile that contains both voc and pls
        Preconditions:
            voc: is an unsorted list of words and SortedDict Doc Id and Scores.
        Postconditions:
            The fonction saves voc in a partial or full inverted file.
            If not partial, the posting list is also sorted by score and stored.
        """
        # map vocabulary offset
        vocabulary = []
        current_offset = 0
        # save all the posting lists

        # we sort voc
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
            voc: is a sorted list of words and offset.
        postconditions:
            voc file is saved
        """
        if isPartial:
            file = open(self.getPathVocPartial(self.numberPartialFiles), "w")
        else:
            file = open(self.getPathVoc(), "w")
        for word, offset in voc:
            file.write("{},{}\n".format(word, offset))
        file.close()

    def save_postList_by_score(self, postingList, offset=-1, filePlScore=None):
        """ Save the postingList by score in non ascending order 
        Preconditions : 
            postingList: a sorted list by score in non ascending order
            offset: offset in the file, if -1, append at the end
            filePlScore: if non None, the method will store into this file (without applying the offset)
            """
        # destination file for redin and wrting (r+)b
        if filePlScore is not None:
            file = filePlScore
        else:
            if offset == -1:
                # Append
                file = open(self.getPathPLScore(), "a+b")
                offset = 0
            else:
                file = open(self.getPathPLScore(), "w+b")

        try:
            if (offset != 0) and filePlScore is None:
                file.seek(self.CONST_SIZE_ON_DISK * offset)
            # Encode the record and write it to the dest file
            for idDoc, score in sorted(postingList.items(), key=lambda s: (-s[1][0], s[0])):
                record = self.struct.pack(idDoc, score[0], score[1])
                file.write(record)

        except IOError:
            pass
        finally:
            if filePlScore is None:
                file.close()

    def save_postList(self, postingList, offset=-1, isPartial=False, numberPart=0, filePL=None):
        """
        Preconditions:
            postingList: is a dictionary of Doc Id and Scores.
            offset: is the numbers of paires <Doc Id, Scores> alredy written in the binary doc, the PL will be written affter  it, (offset < size of the file.)
                    if == -1, we append
        Postconditions:
            The fonction update the file postingLites.data withe the new postingList after "offet" pairs <Doc Id, Scores>,
        """
        # destination file for redin and wrting (r+)b
        if filePL is not None:
            file = filePL
        elif (offset == -1) and not isPartial:
            # Append
            file = open(self.getPathPL(), "a+b")
            offset = 0
        elif not isPartial:
            file = open(self.getPathPL(), "w+b")
        elif isPartial:  # we do not append to partial files
            file = open(self.getPathPLPartial(numberPart), "a+b")

        try:
            # to do an offset if we use the preopened file in parameters
            if (offset > 0) and filePL is None:
                file.seek(self.CONST_SIZE_ON_DISK * offset)
            # Encode the record and write it to the dest file
            for idDoc, score in sorted(postingList.items()):
                record = self.struct.pack(idDoc, score[0], score[1])
                file.write(record)

        except IOError:
            pass
        finally:
            if filePL is None:
                file.close()

    # Save vocabulary that contains number of occurencies
    # The voc and pl are saved to filename+"."+number+"."+extension+".temp"
    def savePartialVocabularyAndPL(self, voc):
        """
        Preconditions:
            voc: is a array of  words and SortedDict Doc Id and Scores.
        """
        self.numberPartialFiles += 1
        self.save_vocabularyAndPL_file(voc, True)
        pass

    def save_random_indexing_voc(self, voc):
        file = open(self.getPathRandomIndexingVO(), "w")
        for word in voc:
            file.write("{}\n".format(word))
        file.close()

    def save_random_indexing(self, terms, term_dimension):
        self.randomStruct = struct.Struct(str(term_dimension) + 'i')
        file = open(self.getPathRandomIndexing(), "wb")
        existant_voc = []
        for vo in terms:
            if (vo != '***NumberDifferentDocs***'):
                binaryBuff = self.randomStruct.pack(*terms[vo])
                existant_voc.append(vo)
                file.write(binaryBuff)
        self.save_random_indexing_voc(existant_voc)

    def read_random_indexing_vo(self):
        filename = self.getPathRandomIndexingVO()
        file = open(filename, "r")
        voc = []
        for line in file:
            data = line.rstrip('\n\r')
            voc.append(data)
        file.close()
        return voc

    def read_random_indexing(self, term_dimension):
        self.randomStruct = struct.Struct(str(term_dimension) + 'i')
        file = open(self.getPathRandomIndexing(), "rb")
        vocabulary = self.read_random_indexing_vo()
        ri_voc = []
        ri_terms = []
        for vo in vocabulary:
            if (vo != '***NumberDifferentDocs***'):
                record = file.read(4 * term_dimension)
                decoded = self.randomStruct.unpack(record)
                ri_terms.append(vo)
                ri_voc.append(np.array(decoded))
                # print("EOO: {}:{}\n\r".format(vo,decoded))
        return ri_terms, np.array(ri_voc)

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

    def read_postList(self, offset, length, isPartial=False, number=0, returnPostingListOrderedByScore=False, sorted=False, filePL=None):
        """
        Precondtions:
            offset: is the numbers of pairs <Doc Id, Scores> already written in the binary doc
            length: is the number of pairs <Doc Id, Scores> to be read
        Postcondtions:
            return a posting list: a dictionary of Doc Id and Scores red between offet and length.
            return also a posting list sorted by scores : an array of   
        """
        # File to read
        if isPartial:
            filename = self.getPathPLPartial(number)
        else:
            filename = self.getPathPL()
        if filePL is None:
            file = open(filename, "rb")
        else:
            file = filePL

        if returnPostingListOrderedByScore:
            filePLScore = open(self.getPathPLScore(), "rb")

        if sorted:
            postingList = SortedDict()
        else:
            postingList = {}
        postingListByScore = []
        try:
            if filePL is None:
                file.seek(self.CONST_SIZE_ON_DISK * offset)
            if returnPostingListOrderedByScore:
                filePLScore.seek(self.CONST_SIZE_ON_DISK * offset)
            for x in range(0, length):
                record = file.read(self.CONST_SIZE_ON_DISK)
                filed = self.struct.unpack(record)
                idDoc = filed[0]
                score = filed[1]
                nbOccurenciesInDoc = filed[2]

                postingList[idDoc] = [score, nbOccurenciesInDoc]

                if (returnPostingListOrderedByScore):
                    record = filePLScore.read(self.CONST_SIZE_ON_DISK)
                    filed = self.struct.unpack(record)
                    idDoc = filed[0]
                    score = filed[1]
                    
                    postingListByScore.append((score, idDoc))

            if returnPostingListOrderedByScore:
                return postingList, postingListByScore
            else:
                return postingList

        except IOError:
            # Your error handling here
            # Nothing for this example
            pass
        finally:
            if filePL is None:
                file.close()
            if returnPostingListOrderedByScore:
                filePLScore.close()
