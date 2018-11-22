#%% [markdown]
# # Benchmark for Indexing Algorithms
# 
# ## 1. getting the data
#%%
## /!\ to be executed only once 
import sys


sys.path.insert(0, "..")

import time
import wordtraveller.analysis as analysis
from pathlib import Path
from sortedcontainers import SortedDict
import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing
import matplotlib.pyplot as plt 
import os, shutil

def analyseAndSaveDocuments(array_of_iterations):
    path = ""
    print("analyse_newspaper")
    print("Save only in the end, no merging involved")
    pathlist = Path("./../latimes/").glob('**/la*')

    tmpPreprocessor = analysis.preprocessor
    analysis.setPreprocessor(preprocessing.Preprocessor(activate_stemmer=False))
    timeToExtract = []
    timeToSave = []
    timeTotal = []
    timeToAnalyse  = []
    for numBatch,nbDocsToRead in enumerate(array_of_iterations):
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
        pathlist = Path("./../latimes/").glob('**/la*')
        vocabulary = dict()
        nbDocsRed = 0
        print("analysis in progress")
        for i, newspaper_path in enumerate(pathlist):
            
            if nbDocsRed>=nbDocsToRead:
                break
            docsRedInDocIteration = -1

            while(docsRedInDocIteration !=0):
                docsRedInDocIteration = analysis.analyse_newspaper(newspaper_path,vocabulary,None,False,0,nbDocsToRead-nbDocsRed)
                nbDocsRed = docsRedInDocIteration + nbDocsRed

                if nbDocsRed >= nbDocsToRead:
                    break
            if nbDocsRed >= nbDocsToRead:
                    break
        if nbDocsRed < nbDocsToRead:
            print("Benchmark invalid, as we ran out of documents to read.")
        timeToExtract.append(time.time()-start)
        start = time.time()
        print("Saving in progress…")
        filemanager.save_vocabularyAndPL_file(vocabulary, isPartial = False)
        timeToSave.append(time.time()-start)
        timeTotal.append(time.time()-startBatch)
        

    analysis.setPreprocessor(tmpPreprocessor)

    plt.plot(array_of_iterations, timeToExtract,label="Time to analyse documents")
    plt.plot(array_of_iterations, timeToSave,label="Time to save")
    plt.plot(array_of_iterations, timeTotal, label="Overall time")
    plt.xlabel("Number of Documents")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


def analyseAndMergeDocuments(array_of_iterations,stepFlush):
    path = ""
    print("analyse_newspaper")
    print("Merging involved, flush frequency : Every "+str(stepFlush) +" document.")
    pathlist = Path("./../latimes/").glob('**/la*')

    tmpPreprocessor = analysis.preprocessor
    analysis.setPreprocessor(preprocessing.Preprocessor(activate_stemmer=False))
    timeToExtract = []
    timeToMerge = []
    timeToFlush = [0] * len(array_of_iterations)
    timeTotal = []
    timeToAnalyse  = []
    for numBatch,nbDocsToRead in enumerate(array_of_iterations):
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
        pathlist = Path("./../latimes/").glob('**/la*')
        vocabulary = dict()
        nbDocsRed = 0
        nbDocsInMemory = 0
        print("analysis in progress")
        for i, newspaper_path in enumerate(pathlist):
            
            if nbDocsRed>=nbDocsToRead:
                break
            docsRedInDocIteration = -1
            nbDocsRedInThisJournal = 0
            while(docsRedInDocIteration !=0):
                docsRedInDocIteration = analysis.analyse_newspaper(newspaper_path,vocabulary,None,False,nbDocsRedInThisJournal,nbDocsRedInThisJournal+stepFlush)
                nbDocsRed = docsRedInDocIteration + nbDocsRed
                nbDocsInMemory += docsRedInDocIteration
                nbDocsRedInThisJournal += docsRedInDocIteration
                if nbDocsInMemory == stepFlush or nbDocsRed >= nbDocsToRead:
                    startFlush = time.time()
                    filemanager.save_vocabularyAndPL_file(vocabulary, isPartial = True)
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

    plt.plot(array_of_iterations, timeToMerge, label="Time to merge")
    plt.plot(array_of_iterations, timeToExtract,label="Time to analyse document (with flushing)")
    plt.plot(array_of_iterations, timeToFlush,label="Time to flush documents")
    plt.plot(array_of_iterations, timeTotal, label="Overall time")
    plt.xlabel("Number of Documents")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.show()


#%%
# Error: Too many opened files
#analyseAndMergeDocuments( [1,10,100,1000,10000,20000,50000,100000],500)
analyseAndMergeDocuments( [1,10,100,1000,10000,20000,50000,100000],1000)
analyseAndMergeDocuments( [1,10,100,1000,10000,20000,50000,100000],10000)

#%%
# No merging involved
analyseAndSaveDocuments([1,10,100,1000,2000,5000,10000,20000,50000,100000])