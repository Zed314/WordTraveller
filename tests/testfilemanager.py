import sys
# To import parent modules
sys.path.insert(0, '')

# Atention: A partir d'ici on est en root

import unittest
import os.path
from wordtraveller import analysis, query
from wordtraveller import filemanager as fm
from sortedcontainers import SortedDict
from pathlib import Path

class TestFileManager(unittest.TestCase):

    def test_creation_postingLists(self):
        currentWorkspace = './tests/workspace/testfilemanager1/'
        filename = 'testfm1'
        postingList = dict()
        postingList[1]=101
        postingList[2]=30023
        postingList[34]=308.0
        postingList[294]=159
        postingList[2324]=3005
        postingList[23445]=3006
        filemanager = fm.FileManager(filename,currentWorkspace)
        filemanager.save_postList(postingList,0)
        self.assertTrue(os.path.isfile(currentWorkspace + filename + '.pl'), "The file .pl should exist")
        self.assertTrue(os.path.isfile(currentWorkspace + filename + '.vo'), "The file .vo should exist")

    def test_read_postingList(self):
        currentWorkspace = './tests/workspace/testfilemanager2/'
        filename = 'testfm2'
        postingList = dict()
        postingList[1]=101
        postingList[2]=30023
        postingList[294]=159
        postingList[23445]=3006
        filemanager = fm.FileManager(filename,currentWorkspace)
        filemanager.save_postList(postingList,0)
        pl = filemanager.read_postList(0,4)
        self.assertEqual(pl, {1: 101, 2: 30023, 294: 159, 23445:3006}, "The sorted Dict should be the same")
    
    def test_modify_postingList(self):
        currentWorkspace = './tests/workspace/testfilemanager3/'
        filename = 'testfm3'
        postingList = dict()
        postingList[1]=101
        postingList[23]=30023
        postingList[234]=3006
        filemanager = fm.FileManager(filename,currentWorkspace)
        # TODO: le offset change quoi?
        filemanager.save_postList(postingList,0)
        postingList[1]=201
        filemanager.save_postList(postingList,0)
        postingList[1]=301
        filemanager.save_postList(postingList,6)
        pl = filemanager.read_postList(0,5)
        for numDoc, score in pl.items():
            print("{} => {}.".format(numDoc, score))

        self.assertEqual(pl, {1: 301, 23: 30023, 234: 3006}, "The sorted Dict should be the same")
        
if __name__ == '__main__':
    unittest.main()