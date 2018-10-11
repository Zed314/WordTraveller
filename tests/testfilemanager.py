import sys
# To import parent modules
sys.path.insert(0, '')

# Atention: A partir d'ici on est en root

import unittest
import os.path
from wordtraveller import analysis, filemanager, query
from sortedcontainers import SortedDict
from pathlib import Path

class TestFileManager(unittest.TestCase):

    def test_creation_postingLists(self):
        currentWorkspace = './tests/workspace/testfilemanager1/'
        postingList = dict()
        postingList[1]=101
        postingList[2]=30023
        postingList[34]=308.0
        postingList[294]=159
        postingList[2324]=3005
        postingList[23445]=3006
        filemanager.savePostList(postingList,0,currentWorkspace)
        self.assertTrue(os.path.isfile(currentWorkspace + 'postingLites.pl'))

    def test_read_postingList(self):
        currentWorkspace = './tests/workspace/testfilemanager2/'
        postingList = dict()
        postingList[1]=101
        postingList[2]=30023
        postingList[294]=159
        postingList[23445]=3006
        filemanager.savePostList(postingList,0,currentWorkspace)
        # TODO: demander comment il marche readPostList 
        pl = filemanager.readPostList(0,8,currentWorkspace)
        print("READING:")
        print(pl)
    
    def test_modify_postingList(self):
        currentWorkspace = './tests/workspace/testfilemanager3/'
        postingList = dict()
        postingList[1]=101
        postingList[23]=30023
        postingList[23445]=3006
        filemanager.savePostList(postingList,0,currentWorkspace)
        postingList[1]=201
        filemanager.savePostList(postingList,6,currentWorkspace)
        postingList[1]=301
        filemanager.savePostList(postingList,12,currentWorkspace)
        pl = filemanager.readPostList(12,6,currentWorkspace)
        # TODO: finish this test
        for numDoc, score in pl.items():
            print("---> {} => {}.".format(numDoc, score))

if __name__ == '__main__':
    unittest.main()