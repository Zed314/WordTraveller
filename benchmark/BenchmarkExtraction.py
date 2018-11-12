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

arrayScalesMini = range(0,200,10)
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

arrayScalesMini = range(0,1000,100)
path = ""
print("analyse_newspaper, no stemmer")
print("No merging involved.")
pathlist = Path("./../latimes/").glob('**/la*')
filemanager = fm.FileManager("benchmarkAnalysisTest")
tmpPreprocessor = analysis.preprocessor
analysis.setPreprocessor(preprocessing.Preprocessor(activate_stemmer=False))
timeToExtract = []
timeToMerge = []

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
        filemanager.save_vocabularyAndPL_file(vocabulary, isPartial = True)
        vocabulary = SortedDict()
    timeToExtract.append(time.time()-start)
   # print("Extraction"+str(time.time()-start))
    start = time.time()
    filemanager.mergePartialVocsAndPL()
  #  print("Merge"+time.time()-start)
    timeToMerge.append(time.time()-start)
    

analysis.setPreprocessor(tmpPreprocessor)

plt.plot(arrayScalesMini, timeToMerge)
plt.plot(arrayScalesMini, timeToExtract)
plt.show()
