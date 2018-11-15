import unittest
import os
import send2trash
from wordtraveller import faginstopkvf as faginstopk
from wordtraveller import filemanager, analysis
from sortedcontainers import SortedDict
from pathlib import Path
import math

class TestFaginsTopK(unittest.TestCase):

    def checkResultApproximative(self, toTest, ref):
        self.assertEqual(len(toTest),len(ref),"Are the reference and the result to test equal in size ?")
        for i, refUnit in enumerate(ref):
            self.assertEqual(toTest[i][0],refUnit[0],"Is document "+str(refUnit[0])+" in position "+str(i)+" ?")
            self.assertAlmostEqual(toTest[i][1], refUnit[1], places=7, msg="Are the score roughly equals ?")

    def test_topk_trivial_file(self):

        pathlist = Path("./tests/data/testtrivialtopk/").glob('**/la*')

        filemana = filemanager.FileManager("TestFaginsTopK","./tests/workspace/testsfaginstopk")
        tempVoc = SortedDict()
        for path in pathlist:
            analysis.analyse_newspaper(path, tempVoc, True)
        filemana.save_vocabularyAndPL_file(tempVoc)
        

        # Extraction of the saved Voc
        savedVoc = filemana.read_vocabulary()        

        topk = faginstopk.apply_top_k_algo(['aa', 'bb'], savedVoc, filemana,0, 5)
        # print("::::: {}".format(topk))
        # TODO: Disjunctive/conjonctive
        # self.checkResultApproximative(topk,[(2,(math.log(3/4)+math.log(3/2))/2)])
        self.checkResultApproximative(topk,[(2,(math.log(3/4)+math.log(3/2))/2),(1,math.log(3/4)/2), (3,math.log(3/4)/2)])


        topk = faginstopk.apply_top_k_algo(['bb'], savedVoc, filemana,0, 5)
        self.checkResultApproximative(topk,[(2,math.log(3/2))])

        topk = faginstopk.apply_top_k_algo(['cc'], savedVoc, filemana,0, 5)
        self.checkResultApproximative(topk,[])

    def test_topk_trivial(self):
        pl1_score = SortedDict()
        pl1_score[0.90] = [1]
        pl1_score[0.70] = [3]
        pl1_score[0.80] = [2]

        pl2_score = SortedDict()
        pl2_score[0.80] = [2]
        pl2_score[0.75] = [3]
        pl2_score[0.85] = [1]


        postingListsOrderedByScore = dict()
        postingListsOrderedByScore['aaa'] = pl1_score
        postingListsOrderedByScore['bbb'] = pl2_score
        
        postingListsOrderedByScoreSingle = dict()
        postingListsOrderedByScoreSingle['aaa'] = pl1_score
        
        pl1_id = dict()
        
        pl1_id[1] = [0.90]
        pl1_id[2] = [0.80]
        pl1_id[3] = [0.70]

        pl2_id = dict()
        pl2_id[1] = [0.85]
        pl2_id[2] = [0.80]
        pl2_id[3] = [0.75]
        

        postingListsIndexedById = dict()
        postingListsIndexedById['aaa'] = pl1_id
        postingListsIndexedById['bbb'] = pl2_id
        postingListsIndexedByIdSingle = dict()
        postingListsIndexedByIdSingle['aaa'] = pl1_id


        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 3)
        self.assertEqual(top_k, [(1,0.875), (2,0.8), (3,0.725)], "Topk simple, k = 3")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 4)
        self.assertEqual(top_k, [(1,0.875), (2,0.8), (3,0.725)], "Topk simple, k = 4")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 2)
        self.assertEqual(top_k, [(1,0.875), (2,0.8)], "Topk simple, k = 2")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 1)
        self.assertEqual(top_k, [(1,0.875)], "Topk simple, k = 1")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                             postingListsOrderedByScore, 0)
        self.assertEqual(top_k, [], "Topk simple, k = 0")
       
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedByIdSingle,
                              postingListsOrderedByScoreSingle, 3)
        self.assertEqual(top_k, [(1,0.9), (2,0.8), (3 , 0.7)], "Topk single, k = 3")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedByIdSingle,
                              postingListsOrderedByScoreSingle, 4)
        self.assertEqual(top_k, [(1,0.9), (2,0.8), (3 , 0.7)], "Topk single, k = 4")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedByIdSingle,
                              postingListsOrderedByScoreSingle, 2)
        self.assertEqual(top_k, [(1,0.9), (2,0.8)], "Topk single, k = 2")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedByIdSingle,
                              postingListsOrderedByScoreSingle, 1)
        self.assertEqual(top_k, [(1,0.9)], "Topk single, k = 1")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedByIdSingle,
                             postingListsOrderedByScoreSingle, 0)
        self.assertEqual(top_k, [], "Topk single, k = 0")

    def test_topk_twoidenticalscores(self):
        pl1_score = SortedDict()
        pl1_score[0.90] = [1]
        pl1_score[0.90] += [2]
        pl1_score[0.90] += [3]

        pl2_score = SortedDict()
        pl2_score[0.85] = [1]
        pl2_score[0.80] = [2]
        pl2_score[0.75] = [3]


        postingListsOrderedByScore = dict()
        postingListsOrderedByScore['aaa'] = pl1_score
        postingListsOrderedByScore['bbb'] = pl2_score

        pl1_id = dict()
        
        pl1_id[1] = [0.90]
        pl1_id[2] = [0.90]
        pl1_id[3] = [0.90]

        pl2_id = dict()
        pl2_id[1] = [0.85]
        pl2_id[2] = [0.80]
        pl2_id[3] = [0.75]

        postingListsIndexedById = dict()
        postingListsIndexedById['aaa'] = pl1_id
        postingListsIndexedById['bbb'] = pl2_id
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 3)
        self.assertEqual(top_k, [(1,0.875), (2,0.8500000000000001), (3,0.825)], "Topk simple, k = 3")
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 4)
        self.assertEqual(top_k, [(1,0.875), (2,0.8500000000000001), (3,0.825)], "Topk simple, k = 4")
       
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                             postingListsOrderedByScore, 2)
        self.assertEqual(top_k, [(1,0.875), (2,0.8500000000000001)], "Topk simple, k = 2")
       
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 1)
        self.assertEqual(top_k, [(1,0.875)], "Topk simple, k = 1")
        
        top_k = faginstopk.find_fagins_top_k(postingListsIndexedById,
                              postingListsOrderedByScore, 0)
        self.assertEqual(top_k, [], "Topk simple, k = 0")
       
        
if __name__ == '__main__':

    unittest.main()