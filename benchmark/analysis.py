import cProfile
import re
import time
from memory_profiler import profile
import wordtraveller.analysis as analysis
from pathlib import Path
from sortedcontainers import SortedDict
import wordtraveller.filemanager as fm
import wordtraveller.preprocessing as preprocessing
import argparse

@profile
def analyseProfile(nbNewspaper, path = "./latimes/", flushEvery = 1, analysisApproach = analysis.analyse_newspaper, mergeInTheEnd = True,  useStemmer=True):
  analyse(nbNewspaper, path, flushEvery, analysisApproach, mergeInTheEnd)

def analyse(nbNewspaper, path = "./latimes/", flushEvery = 1, analysisApproach = analysis.analyse_newspaper, mergeInTheEnd = True,  useStemmer=True):
  """
  This benchmark will analyse documents, put the VOC and PL in memory
  and eventually flush it to the hardrive if requested. 
  In the end, a VOC and PL file will be created on the hardrive
  
  nbNewspaper is the number of newspaper we will go through in path
  path is the path to the directory
  flushEvery is the frequency of flush. (-1 if we never flush)
  mergeInTheEnd : if false, no merge in the end is proceeded and vocabulary is reset at the end of each loop
  """
  pathlist = Path(path).glob('**/la*')
  vocabulary = SortedDict()
  filemanager = fm.FileManager("benchmarkAnalysisTest")
  flushCounter = 0
  tmpPreprocessor = analysis.preprocessor
  if not useStemmer:
    analysis.setPreprocessor(preprocessing.Preprocessor(activateStemmer=False))
  for i, newspaper_path in enumerate(pathlist):
    if i>=nbNewspaper:
      break

    flushCounter += 1
    analysisApproach(newspaper_path, vocabulary,False)
    if mergeInTheEnd == False:
      vocabulary = SortedDict()
      continue
    if flushCounter >= flushEvery and flushEvery !=1:
      flushCounter = 0
      filemanager.save_vocabularyAndPL_file(vocabulary, isPartial = True)
      vocabulary = SortedDict()
  if mergeInTheEnd:
    filemanager.mergePartialVocsAndPL()
  analysis.setPreprocessor(tmpPreprocessor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m",
                        help="Do a memory profiling. Takes much more time.",
                        action="store_true")

    args = parser.parse_args()
    memprof = False
    if args.m:
      print("Activation of the memory profiling mode. An estamation of the memory consumption will be provided instead of the execution time.")
      memprof = True
    arrayScales = [1,10,50,100,500]
    arrayScalesMini = [10]
    # print("analyse_newspaper_naive, uses a built-in XML parser to analyse documents")
    # print("No merging involved.")
    # for i in arrayScalesMini:
    #   start = time.time()
    #   if(memprof):
    #    # pass
    #     analyseProfile(i, analysisApproach=analysis.analyse_newspaper_naive, mergeInTheEnd=False)
    #   else:
    #     analyse(i, analysisApproach=analysis.analyse_newspaper_naive, mergeInTheEnd=False)
    #   end = time.time()
    #   print("For "+ str(i) + " document(s) :" + str(end - start) + " seconds")
    
    # print("analyse_newspaper_optimized, uses custom parser to analyse documents")
    # print("No merging involved.")
    # for i in arrayScalesMini:
    #   start = time.time()
    #   if memprof:
    #     analyseProfile(i, analysisApproach=analysis.analyse_newspaper_optimized, mergeInTheEnd=False)
    #   else:
    #     analyse(i, analysisApproach=analysis.analyse_newspaper_optimized, mergeInTheEnd=False)
    #   end = time.time()
    #   print("For "+ str(i) + " document(s) :" + str(end - start) + " seconds")
    
    # print("Analysis with Stemmer")
    # for i in arrayScalesMini:
    #   start = time.time()
    #   if memprof:
    #     analyseProfile(i, mergeInTheEnd=False, useStemmer=True)
    #   else:
    #     analyse(i, mergeInTheEnd=False,  useStemmer=True)
    #   end = time.time()
    #   print("For "+ str(i) + " document(s) :" + str(end - start) + " seconds")
    
    print("Analysis without Stemmer")
    for i in arrayScalesMini:
      start = time.time()
      if memprof:
        analyseProfile(i, mergeInTheEnd=False,  useStemmer=False)
      else:
        analyse(i, mergeInTheEnd=False, useStemmer=False)
      end = time.time()
      print("For "+ str(i) + " document(s) :" + str(end - start) + " seconds")
    

    