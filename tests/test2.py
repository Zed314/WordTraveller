import os
import unittest
from pathlib import Path

import send2trash

from wordtraveller import analysis
from wordtraveller import filemanager as fm
from wordtraveller import query


class TestAnalysis(unittest.TestCase):

#activate when multithreading is complete
    # def test_3_files_multithread_scores(self):
    #     voc = dict()
    #     currentWorkspace = './tests/workspace/test2/'
    #     filename = 'test3filesmultithreadscores'

    #     pathlist = Path("./tests/data/test4/").glob('**/la*')

    #     filemanager = fm.FileManager(filename, currentWorkspace)
    #     pathArray = []
    #     for path in pathlist:
    #         pathArray.append(path)

    #     analysis.analyse_newspaper(pathArray, voc, computeIDF=True)
    #     filemanager.save_vocabularyAndPL_file(voc, False)
  


    #     savedVoc = filemanager.read_vocabulary()
    #     mot,sortedByScore = query.get_posting_list(savedVoc, "aa", filemanager, True)
    #     self.assertEqual(mot, {1: [0.24718092381954193, 3.0], 2: [0.32882189750671387, 6.0], 5: [0.11778303235769272, 1.0], 6: [
    #                      0.11778303235769272, 1.0], 20: [0.24718092381954193, 3.0], 21: [0.19942401349544525, 2.0], 22: [0.11778303235769272, 1.0]})
        
    #     self.assertEqual(sortedByScore, [(0.32882189750671387, 2), (0.24718092381954193, 1), (0.24718092381954193, 20), (0.19942401349544525, 21), (0.11778303235769272, 5),(0.11778303235769272, 6),(0.11778303235769272, 22)])
        
    #     mot,sortedByScore = query.get_posting_list(savedVoc, "bb", filemanager,True)
    #     print (mot)
    #     print(sortedByScore)
    #     self.assertEqual(mot, {1: [0.5274115204811096, 3.0], 2: [0.7016094326972961, 6.0], 4: [0.2513144314289093, 1.0], 5: [0.2513144314289093, 1.0], 20: [0.2513144314289093, 1.0], 21: [0.2513144314289093, 1.0]})
    #     self.assertEqual(sortedByScore,[(0.7016094326972961, 2), (0.5274115204811096, 1), (0.2513144314289093,4),(0.2513144314289093, 5),(0.2513144314289093,20),(0.2513144314289093, 21)])
        

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
