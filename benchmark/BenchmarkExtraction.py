#%% [markdown]
# # Benchmark for Indexing Algorithms
# 
# ## 1. getting the data
#%%
## /!\ to be executed only once 
import sys
sys.path.insert(0, "..")

#%%
import time
import wordtraveller.analysis as analysis
from pathlib import Path
from sortedcontainers import SortedDict
import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing
import matplotlib.pyplot as plt 

arrayScalesMini = range(0,200,50)
path = ""
print("analyse_newspaper, no stemmer")
print("No merging involved.")
pathlist = Path("./../latimes/").glob('**/la*')
filemanager = fm.FileManager("benchmarkAnalysisTest")
tmpPreprocessor = analysis.preprocessor
analysis.setPreprocessor(preprocessing.Preprocessor(activate_stemmer=False))
timeToExtract = []

for nbDocsToRead in arrayScalesMini:
    start = time.time()
    pathlist = Path("./../latimes/").glob('**/la*')
    vocabulary = SortedDict()
    nbDocsRed = 0
    for i, newspaper_path in enumerate(pathlist):
        if nbDocsRed==nbDocsToRead:
            break
        docsRedInDoc = analysis.analyse_newspaper(newspaper_path,vocabulary,False,0,nbDocsToRead-nbDocsRed)
        nbDocsRed = docsRedInDoc + nbDocsRed
        print(docsRedInDoc)
        print(nbDocsRed)
    timeToExtract.append(time.time()-start)
    print(time.time()-start)

analysis.setPreprocessor(tmpPreprocessor)
print(timeToExtract[0:10])
plt.plot(arrayScalesMini, timeToExtract)
plt.show()

#%%
import time
import wordtraveller.analysis as analysis
from pathlib import Path
from sortedcontainers import SortedDict
import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing
import matplotlib.pyplot as plt 
import os, shutil

arrayScalesMini = range(1,1001,100)
path = ""
print("analyse_newspaper, no stemmer")
print("Merging involved, flush frequency : Every document.")
pathlist = Path("./../latimes/").glob('**/la*')

tmpPreprocessor = analysis.preprocessor
analysis.setPreprocessor(preprocessing.Preprocessor(activate_stemmer=False))
timeToExtract = []
timeToMerge = []
timeToFlush = [0] * len(arrayScalesMini)
stepFlush = 200
for numBatch,nbDocsToRead in enumerate(arrayScalesMini):
   
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
    vocabulary = SortedDict()
    nbDocsRed = 0
    

    nbDocsInMemory = 0
  
    for i, newspaper_path in enumerate(pathlist):
        print(newspaper_path)
        if nbDocsRed>=nbDocsToRead:
            break
        docsRedInDocIteration = -1
        nbDocsRedInThisJournal = 0
        while(docsRedInDocIteration !=0):
            docsRedInDocIteration = analysis.analyse_newspaper(newspaper_path,vocabulary,False,nbDocsRedInThisJournal,nbDocsRedInThisJournal+stepFlush)
            nbDocsRed = docsRedInDocIteration + nbDocsRed
            nbDocsInMemory += docsRedInDocIteration
            nbDocsRedInThisJournal += docsRedInDocIteration
            if nbDocsInMemory == stepFlush or nbDocsRed >= nbDocsToRead:
                startFlush = time.time()
                filemanager.save_vocabularyAndPL_file(vocabulary, isPartial = True)
                vocabulary = SortedDict()
                nbDocsInMemory = 0
                timeToFlush[numBatch] += (time.time() - startFlush)

            if nbDocsRed >= nbDocsToRead:
                break
        if nbDocsRed >= nbDocsToRead:
                break
    timeToExtract.append(time.time()-start)
    start = time.time()
    filemanager.mergePartialVocsAndPL()
    timeToMerge.append(time.time()-start)
    

analysis.setPreprocessor(tmpPreprocessor)

plt.plot(arrayScalesMini, timeToMerge, label="Time to merge")
plt.plot(arrayScalesMini, timeToExtract,label="Time to analyse document (with flushing)")
plt.plot(arrayScalesMini, timeToFlush,label="Time to flush documents")
plt.legend()
plt.show()

