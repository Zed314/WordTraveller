# %% [markdown]
# # Benchmark for Indexing Algorithms
#

# %%
# /!\ to be executed only once
import sys


sys.path.insert(0, "..")

import time
import wordtraveller.analysis as analysis
from pathlib import Path
from sortedcontainers import SortedDict
import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing
import matplotlib.pyplot as plt
import os
import shutil


def analyseAndSaveDocuments(array_of_iterations, computeIDF=False, numberIterations = 1):
    totaltimeToExtract = []
    totaltimeToSave = []
    totaltimeTotal = []
    totaltimeToComputeIDF = []
    for i in range(0, numberIterations):
        path = ""
        print("analyse_newspaper")
        print("Save only in the end, no merging involved")
        pathlist = Path("./../data/latimes/").glob('**/la*')

        tmpPreprocessor = analysis.preprocessor
        analysis.setPreprocessor(
            preprocessing.Preprocessor(activate_stemmer=False))
        timeToExtract = []
        timeToSave = []
        timeTotal = []
        timeToComputeIDF = []
        for numBatch, nbDocsToRead in enumerate(array_of_iterations):
            startBatch = time.time()
            folder = './workspace/'
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            filemanager = fm.FileManager("benchmarkAnalysisTest"+str(nbDocsToRead))
            start = time.time()
            pathlist = Path("./../data/latimes/").glob('**/la*')
            vocabulary = dict()
            nbDocsRed = 0
            print("analysis in progress")
            for i, newspaper_path in enumerate(pathlist):

                if nbDocsRed >= nbDocsToRead:
                    break
                docsRedInDocIteration = -1

                while(docsRedInDocIteration != 0):
                    docsRedInDocIteration = analysis.analyse_newspaper(
                        newspaper_path, vocabulary, None, False, 0, nbDocsToRead-nbDocsRed)
                    nbDocsRed = docsRedInDocIteration + nbDocsRed

                    if nbDocsRed >= nbDocsToRead:
                        break
                if nbDocsRed >= nbDocsToRead:
                    break
            if nbDocsRed < nbDocsToRead:
                print("Benchmark invalid, as we ran out of documents to read.")
            timeToExtract.append(time.time()-start)
            if computeIDF:
                startComputeIDF = time.time()
                analysis.computeIDF(vocabulary)
                timeToComputeIDF.append(time.time()-startComputeIDF)
            start = time.time()
            print("Saving in progress…")
            filemanager.save_vocabularyAndPL_file(vocabulary, isPartial=False)
            timeToSave.append(time.time()-start)
            timeTotal.append(time.time()-startBatch)

        analysis.setPreprocessor(tmpPreprocessor)
        print("Number of documents :")
        print(array_of_iterations)
        plt.plot(array_of_iterations, timeToExtract,
                label="Time to analyse documents")
        print("Time to extract :")
        print(timeToExtract)
        
        if computeIDF:
            plt.plot(array_of_iterations, timeToComputeIDF,
                    label="Time to compute IDF")
        
            print("Time to compute IDF :")
            print(timeToComputeIDF)
        
        plt.plot(array_of_iterations, timeToSave, label="Time to save")
        print("Time to save :")
        print(timeToSave)
        plt.plot(array_of_iterations, timeTotal, label="Overall time")
        print("Overall Time :")
        print(timeTotal)
        plt.xlabel("Number of Documents")
        plt.ylabel("Time (s)")
        plt.legend()
        plt.show()
        totaltimeToExtract.append(timeToExtract)
        if computeIDF:
            totaltimeToComputeIDF.append(timeToComputeIDF)
        totaltimeToSave.append(timeToSave)
        totaltimeTotal.append(timeTotal)
  
    if computeIDF:
        print("computeidf")
        resIDF = [0] * len(totaltimeToComputeIDF[0])
        for arr in totaltimeToComputeIDF:
            for i,elt in enumerate(arr):
                resIDF[i]= resIDF[i] + elt/len(totaltimeToComputeIDF)
        
        print(totaltimeToComputeIDF)
        print(resIDF)
    print("extract")
    resextract = [0] * len(totaltimeToExtract[0])
    for arr in totaltimeToExtract:
        for i,elt in enumerate(arr):
           resextract[i]= resextract[i] + elt/len(totaltimeToExtract)
    print(totaltimeToExtract)
    print(resextract)
    print("save")
    ressave = [0] * len(totaltimeToSave[0])
    for arr in totaltimeToSave:
        for i,elt in enumerate(arr):
           ressave[i]= ressave[i] + elt/len(totaltimeToSave)
    print(totaltimeToSave)
    print(ressave)
    print("total")
    restotal = [0] * len(totaltimeTotal[0])
    for arr in totaltimeTotal:
        for i,elt in enumerate(arr):
           restotal[i]= restotal[i] + elt/len(totaltimeTotal)
    print(totaltimeTotal)
    print(restotal)
    plt.plot(array_of_iterations, resextract, label="Time to analyse documents")
    if computeIDF:
        plt.plot(array_of_iterations, resIDF, label="Time to compute IDF")
    plt.plot(array_of_iterations, ressave, label="Time to save")
    plt.plot(array_of_iterations, restotal, label="Overall time")
    plt.xlabel("Number of Documents")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

    

def analyseAndSaveDocumentsMultithread(array_of_newspapers, computeIDF=False):
    path = ""
    print("analyse_newspaper")
    print("Save only in the end, no merging involved")

    pathlist = Path("./../data/latimes/").glob('**/la*')
    tmpPreprocessor = analysis.preprocessor
    analysis.setPreprocessor(
        preprocessing.Preprocessor(activate_stemmer=False))
    timeToExtract = []
    timeToSave = []
    timeTotal = []
    timeToAnalyse = []
    timeToComputeIDF = []
    for numBatch, nbNewsPaperToRead in enumerate(array_of_newspapers):
        startBatch = time.time()
        folder = './workspace/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        filemanager = fm.FileManager("benchmarkAnalysisTest"+str(nbNewsPaperToRead))
        start = time.time()
        pathlist = Path("./../data/latimes/").glob('**/la*')
        vocabulary = dict()
        nbNewspaperRed = 0
        nbDocsRed = 0
        print("analysis in progress")
        for i, newspaper_path in enumerate(pathlist):

            if nbNewspaperRed >= nbNewsPaperToRead:
                break
            docsRedInDocIteration = analysis.analyse_newspaper(newspaper_path, vocabulary, None, False)
            nbDocsRed = docsRedInDocIteration + nbDocsRed
            nbNewspaperRed += 1

        if nbNewspaperRed < nbNewsPaperToRead:
            print("Benchmark invalid, as we ran out of newspaper to read.")
        timeToExtract.append(time.time()-start)
        print("We red documents : ")
        print(nbDocsRed)
        if computeIDF:
            startComputeIDF = time.time()
            analysis.computeIDF(vocabulary)
            timeToComputeIDF.append(time.time()-startComputeIDF)
        start = time.time()
        print("Saving in progress…")
        filemanager.save_vocabularyAndPL_file(vocabulary, isPartial=False)
        timeToSave.append(time.time()-start)
        timeTotal.append(time.time()-startBatch)

    analysis.setPreprocessor(tmpPreprocessor)
    print("Number of documents :")
    print(array_of_newspapers)
    plt.plot(array_of_newspapers, timeToExtract,
             label="Time to analyse documents")
    print("Time to extract :")
    print(timeToExtract)
    
    if computeIDF:
        plt.plot(array_of_newspapers, timeToComputeIDF,
                 label="Time to compute IDF")
    
        print("Time to compute IDF :")
        print(timeToComputeIDF)

    plt.plot(array_of_newspapers, timeToSave, label="Time to save")
    print("Time to save :")
    print(timeToSave)
    plt.plot(array_of_newspapers, timeTotal, label="Overall time")
    print("Overall Time :")
    print(timeTotal)
    plt.xlabel("Number of Documents")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()

def analyseAndMergeDocuments(array_of_iterations, stepFlush):
    path = ""
    print("analyse_newspaper")
    print("Merging involved, flush frequency : Every " +
          str(stepFlush) + " document.")
    pathlist = Path("./../data/latimes/").glob('**/la*')

    tmpPreprocessor = analysis.preprocessor
    analysis.setPreprocessor(
        preprocessing.Preprocessor(activate_stemmer=False))
    timeToExtract = []
    timeToMerge = []
    timeToFlush = [0] * len(array_of_iterations)
    timeTotal = []
    timeToAnalyse = []
    for numBatch, nbDocsToRead in enumerate(array_of_iterations):
        startBatch = time.time()
        folder = './workspace/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        filemanager = fm.FileManager("benchmarkAnalysisTest"+str(nbDocsToRead))
        start = time.time()
        pathlist = Path("./../data/latimes/").glob('**/la*')
        vocabulary = dict()
        nbDocsRed = 0
        nbDocsInMemory = 0
        print("analysis in progress")
        for i, newspaper_path in enumerate(pathlist):

            if nbDocsRed >= nbDocsToRead:
                break
            docsRedInDocIteration = -1
            nbDocsRedInThisJournal = 0
            while(docsRedInDocIteration != 0):
                docsRedInDocIteration = analysis.analyse_newspaper(
                    newspaper_path, vocabulary, None, False, nbDocsRedInThisJournal, nbDocsRedInThisJournal+stepFlush)
                nbDocsRed = docsRedInDocIteration + nbDocsRed
                nbDocsInMemory += docsRedInDocIteration
                nbDocsRedInThisJournal += docsRedInDocIteration
                if nbDocsInMemory == stepFlush or nbDocsRed >= nbDocsToRead:
                    startFlush = time.time()
                    filemanager.save_vocabularyAndPL_file(
                        vocabulary, isPartial=True)
                    vocabulary = dict()
                    nbDocsInMemory = 0
                    timeToFlush[numBatch] += (time.time() - startFlush)
                if nbDocsRed >= nbDocsToRead:
                    break
            if nbDocsRed >= nbDocsToRead:
                break
        if nbDocsRed < nbDocsToRead:
            print("Benchmark invalid, as we ran out of documents to read.")
        timeToExtract.append(time.time()-start)
        start = time.time()
        print("Merging in progress…")
        filemanager.mergePartialVocsAndPL()
        timeToMerge.append(time.time()-start)
        timeTotal.append(time.time()-startBatch)

    analysis.setPreprocessor(tmpPreprocessor)
    print(array_of_iterations)
    print("Ttmerge")
    print(timeToMerge)
    plt.plot(array_of_iterations, timeToMerge, label="Time to merge")
    print("Ttextract")
    print(timeToExtract)
    plt.plot(array_of_iterations, timeToExtract,
             label="Time to analyse document (with flushing)")
    print("Ttflush")
    print(timeToFlush)
    plt.plot(array_of_iterations, timeToFlush, label="Time to flush documents")
    print("Overalltime")
    print(timeTotal)
    plt.plot(array_of_iterations, timeTotal, label="Overall time")
    plt.xlabel("Number of Documents")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


# %%
# Merging involved
# Error: Too many opened files
#analyseAndMergeDocuments( [1,10,100,1000,10000,20000,50000,100000],500)
analyseAndMergeDocuments([1000, 10000, 20000, 50000], 1000)
analyseAndMergeDocuments([1000, 10000, 20000, 50000], 2000)
analyseAndMergeDocuments([1000, 10000, 20000, 50000], 5000)
analyseAndMergeDocuments([1000, 10000, 20000, 50000], 10000)

# %%
# No merging involved
analyseAndSaveDocuments(
    [1, 10, 100, 1000, 2000, 5000, 10000, 20000, 50000, 100000], computeIDF=False, numberIterations=3)

# %%
# No merging involved
analyseAndSaveDocuments([1, 10, 100, 1000, 2000, 5000,
                        10000, 20000, 50000, 100000], computeIDF=True, numberIterations=3)

# %%
# Multithreading, in number of newspapers

analyseAndSaveDocumentsMultithread([1, 10, 100, 200,300, 400], computeIDF=True)
