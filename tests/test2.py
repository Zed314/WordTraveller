import unittest
from wordtraveller import analysis, query
from wordtraveller import filemanager as fm
from pathlib import Path
import send2trash
import os


class TestAnalysis(unittest.TestCase):
    # Pour compter les mots:
    # http://www.writewords.org.uk/word_count.asp

    def test_simple_multi(self):
        voc = dict()
        currentWorkspace = './tests/workspace/test1/'
        filename = 'test1'

        pathlist = Path("./tests/data/test1/").glob('**/la*')
        for path in pathlist:
            analysis.analyse_newspaper(path, voc)
        filemanager = fm.FileManager(filename, currentWorkspace)
        filemanager.save_vocabularyAndPL_file(voc, False)
        savedVoc = filemanager.read_vocabulary()

        mot1 = query.get_posting_list(savedVoc, "aa", filemanager)
        mot2 = query.get_posting_list(savedVoc, "bb", filemanager)
        mot3 = query.get_posting_list(savedVoc, "cc", filemanager)
        self.assertEqual(mot1, {1: [0, 3], 2: [0, 2], 3: [0, 1]})
        self.assertEqual(mot2, {1: [0, 1], 2: [0, 1]})
        self.assertEqual(mot3, {3: [0, 1]})

    def test_with_stopwords(self):
        voc = dict()
        currentWorkspace = './tests/workspace/test2/'
        filename = 'test2'

        pathlist = Path("./tests/data/test2/").glob('**/la*')
        for path in pathlist:
            analysis.analyse_newspaper(path, voc)

        filemanager = fm.FileManager(filename, currentWorkspace)
        filemanager.save_vocabularyAndPL_file(voc)
        # TODO: changer quand on ait une function directe
        savedVoc = filemanager.read_vocabulary()
        mot1 = query.get_posting_list(savedVoc, "aa", filemanager)
        mot2 = query.get_posting_list(savedVoc, "bb", filemanager)
        mot3 = query.get_posting_list(savedVoc, "cc", filemanager)
        self.assertEqual(mot1, {1: [0, 1], 2: [0, 2]})
        self.assertEqual(mot2, {1: [0, 4], 2: [0, 1]})
        self.assertEqual(mot3, {2: [0, 2]})

        stop1 = query.get_posting_list(savedVoc, "doing", filemanager)
        self.assertEqual(stop1, {})

    def test_merging(self):
        voc = dict()
        currentWorkspace = './tests/workspace/test3/'
        filename = 'test3'

        pathlist = Path("./tests/data/test3/").glob('**/la*')

        filemanager = fm.FileManager(filename, currentWorkspace)

        for path in pathlist:
            analysis.analyse_newspaper(path, voc)
            filemanager.save_vocabularyAndPL_file(voc, True)
            voc = dict()

        filemanager.mergePartialVocsAndPL(False)

        # TODO: changer quand on ait une function directe
        savedVoc = filemanager.read_vocabulary()
        mot, sortedByScore = query.get_posting_list(
            savedVoc, "aa", filemanager, True)
        self.assertEqual(mot, {1: [0, 3], 2: [0, 2], 3: [
                         0, 1], 4: [0, 3], 5: [0, 2], 6: [0, 1]})
        # The score is equal to zero
        self.assertEqual(sortedByScore, [(0, 1),(0, 2),(0, 3),(0, 4),(0, 5),(0, 6)])
        mot, sortedByScore = query.get_posting_list(
            savedVoc, "bb", filemanager, True)
        # The score is equal to zero
        self.assertEqual(sortedByScore, [(0, 1), (0,2), (0,4), (0,5)])
        self.assertEqual(mot, {1: [0, 1], 2: [0, 1], 4: [0, 1], 5: [0, 1]})
        mot, sortedByScore = query.get_posting_list(
            savedVoc, "cc", filemanager, True)
        self.assertEqual(mot, {3: [0, 1], 6: [0, 1]})
        self.assertEqual(sortedByScore, [(0, 3),(0, 6)])

    def test_merging_3_files(self):
        voc = dict()
        currentWorkspace = './tests/workspace/test4/'
        filename = 'test4merging3files'

        pathlist = Path("./tests/data/test4/").glob('**/la*')

        filemanager = fm.FileManager(filename, currentWorkspace)


        for path in pathlist:
            analysis.analyse_newspaper(path, voc)
            filemanager.save_vocabularyAndPL_file(voc, True)
            voc = dict()

        filemanager.mergePartialVocsAndPL(False)

        # TODO: changer quand on a   une function directe
        savedVoc = filemanager.read_vocabulary()
        mot = query.get_posting_list(savedVoc, "aa", filemanager)
        self.assertEqual(mot, {1: [0, 3.0], 2: [0, 6.0], 5: [0, 1.0], 6: [
                         0, 1.0], 20: [0, 3.0], 21: [0, 2.0], 22: [0, 1.0]})
        mot = query.get_posting_list(savedVoc, "bb", filemanager)
        self.assertEqual(mot, {1: [0, 3], 2: [0, 6], 20: [
                         0, 1], 21: [0, 1], 4: [0, 1], 5: [0, 1]})
        mot = query.get_posting_list(savedVoc, "cc", filemanager)
        self.assertEqual(mot, {1: [0, 1], 2: [0, 3], 22: [
                         0, 1], 4: [0, 1], 6: [0, 1]})
        mot = query.get_posting_list(savedVoc, "dd", filemanager)
        self.assertEqual(mot, {1: [0, 2], 2: [0, 1]})
        mot = query.get_posting_list(savedVoc, "ff", filemanager)
        self.assertEqual(mot, {1: [0, 1], 20: [0, 1], 6: [0, 1]}, "FF")
        mot = query.get_posting_list(savedVoc, "qq", filemanager)
        self.assertEqual(mot, {1: [0, 1], 5: [0, 1]})
        mot = query.get_posting_list(savedVoc, "rr", filemanager)
        self.assertEqual(mot, {1: [0, 5], 21: [0, 1]})
        mot = query.get_posting_list(savedVoc, "ee", filemanager)
        self.assertEqual(mot, {1: [0, 1], 23: [0, 1]})
        mot = query.get_posting_list(savedVoc, "vv", filemanager)
        self.assertEqual(mot, {1: [0, 1]})
        mot = query.get_posting_list(savedVoc, "yy", filemanager)
        self.assertEqual(mot, {1: [0, 1]})
        mot = query.get_posting_list(savedVoc, "kk", filemanager)
        self.assertEqual(mot, {2: [0, 1], 23: [0, 1]})
        mot = query.get_posting_list(savedVoc, "ii", filemanager)
        self.assertEqual(mot, {2: [0, 1]})
        mot = query.get_posting_list(savedVoc, "jj", filemanager)
        self.assertEqual(mot, {2: [0, 1]})
        mot = query.get_posting_list(savedVoc, "hh", filemanager)
        self.assertEqual(mot, {23: [0, 1]})
        mot = query.get_posting_list(savedVoc, "ll", filemanager)
        self.assertEqual(mot, {}, 'll is considered a stopword')

    def test_3_files_multithread_scores(self):
        voc = dict()
        currentWorkspace = './tests/workspace/test2/'
        filename = 'test3filesmultithreadscores'

        pathlist = Path("./tests/data/test4/").glob('**/la*')

        filemanager = fm.FileManager(filename, currentWorkspace)
        pathArray = []
        for path in pathlist:
            pathArray.append(path)

        analysis.analyse_newspaper(pathArray, voc, computeIDF=True)
        filemanager.save_vocabularyAndPL_file(voc, False)
  


        savedVoc = filemanager.read_vocabulary()
        mot,sortedByScore = query.get_posting_list(savedVoc, "aa", filemanager, True)
        self.assertEqual(mot, {1: [0.24718092381954193, 3.0], 2: [0.32882189750671387, 6.0], 5: [0.11778303235769272, 1.0], 6: [
                         0.11778303235769272, 1.0], 20: [0.24718092381954193, 3.0], 21: [0.19942401349544525, 2.0], 22: [0.11778303235769272, 1.0]})
        
        self.assertEqual(sortedByScore, [(0.32882189750671387, 2), (0.24718092381954193, 1), (0.24718092381954193, 20), (0.19942401349544525, 21), (0.11778303235769272, 5),(0.11778303235769272, 6),(0.11778303235769272, 22)])
        
        mot,sortedByScore = query.get_posting_list(savedVoc, "bb", filemanager,True)
        print (mot)
        print(sortedByScore)
        self.assertEqual(mot, {1: [0.5274115204811096, 3.0], 2: [0.7016094326972961, 6.0], 4: [0.2513144314289093, 1.0], 5: [0.2513144314289093, 1.0], 20: [0.2513144314289093, 1.0], 21: [0.2513144314289093, 1.0]})
        self.assertEqual(sortedByScore,[(0.7016094326972961, 2), (0.5274115204811096, 1), (0.2513144314289093,4),(0.2513144314289093, 5),(0.2513144314289093,20),(0.2513144314289093, 21)])
        

    @classmethod
    def tearDownClass(cls):
        for folderName, subfolders, filenames in os.walk('./tests/workspace/'):
            for filename in filenames:
                if (filename.endswith('.vo') or filename.endswith('.pl')):
                    print('Deleting from folder ' + folderName + ': ' + filename)
                    send2trash.send2trash(folderName + '/' + filename)


if __name__ == '__main__':
    for folderName, subfolders, filenames in os.walk('./tests/workspace/'):
        for filename in filenames:
            if(filename.endswith('.vo') or filename.endswith('.pl')):
                print('Deleting from folder ' + folderName + ': ' + filename)
                send2trash.send2trash(folderName + '/'+filename)

    unittest.main()
