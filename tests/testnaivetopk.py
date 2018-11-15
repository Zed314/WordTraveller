import unittest
import os
import send2trash
from sortedcontainers import SortedDict
from wordtraveller import filemanager
from wordtraveller import analysis
from wordtraveller import naivetopk
from pathlib import Path
import math

class TestNaiveTopK(unittest.TestCase):

    def checkResultApproximative(self, toTest, ref):
        self.assertEqual(len(toTest),len(ref),"Are the reference and the result to test equal in size ?")
        for i, refUnit in enumerate(ref):
            self.assertEqual(toTest[i][0],refUnit[0],"Is document "+str(refUnit[0])+" in position "+str(i)+" ?")
            self.assertAlmostEqual(toTest[i][1], refUnit[1], places=7, msg="Are the score roughly equal ?")

    def test_topk_trivial_file(self):

        pathlist = Path("./tests/data/testtrivialtopk/").glob('**/la*')

        filemana = filemanager.FileManager("TestFaginsTopK","./tests/workspace/testsfaginstopk")
        tempVoc = SortedDict()
        for path in pathlist:
            analysis.analyse_newspaper(path, tempVoc, True)
        filemana.save_vocabularyAndPL_file(tempVoc)
        

        # Extraction of the saved Voc
        savedVoc = filemana.read_vocabulary()        
#naivetopk.naive_top_k_algo(['aa', 'bb'], savedVoc, filemanager, 5, 
      #  topk = naivetopk.naive_top_k_algo(['aa', 'bb'], savedVoc, filemana,5 , naivetopk.conjunctive_queries)
     #   self.checkResultApproximative(topk,[(2,(math.log(3/4)+math.log(3/2))/2)])

        topk = naivetopk.naive_top_k_algo(['bb'], savedVoc, filemana,0, 5, naivetopk.conjunctive_queries)
        self.checkResultApproximative(topk,[(2,math.log(3/2))])

        topk = naivetopk.naive_top_k_algo(['cc'], savedVoc, filemana,0, 5, naivetopk.conjunctive_queries)
        self.checkResultApproximative(topk,[])

        topk = naivetopk.naive_top_k_algo(['cc','dd'], savedVoc, filemana,0, 5, naivetopk.conjunctive_queries)
        self.checkResultApproximative(topk,[])

        topk = naivetopk.naive_top_k_algo(['cc','dd'], savedVoc, filemana,0, 5, naivetopk.disjunctive_queries)
        self.checkResultApproximative(topk,[])
    
        topk = naivetopk.naive_top_k_algo(['bb'], savedVoc, filemana, 0 ,5, naivetopk.disjunctive_queries)
        self.checkResultApproximative(topk,[(2, math.log(3/2))])

        topk = naivetopk.naive_top_k_algo(['aa', 'bb'], savedVoc, filemana, 0, 1, naivetopk.disjunctive_queries)
        self.checkResultApproximative(topk,[(2, (math.log(3/4)+math.log(3/2))/2)])

        topk = naivetopk.naive_top_k_algo(['aa', 'bb','cc'], savedVoc, filemana,0, 1, naivetopk.disjunctive_queries)
        self.checkResultApproximative(topk,[(2, (math.log(3/4)+math.log(3/2))/3)])

    def test_topk_trivial(self):
        
        pl1_id = dict()
        
        pl1_id[1] = [0.90]
        pl1_id[2] = [0.80]
        pl1_id[3] = [0.70]

        pl2_id = dict()
        pl2_id[1] = [0.85]
        pl2_id[2] = [0.80]
        pl2_id[3] = [0.75]
        
        pl_id = dict()
        # We proceed to a manual aggregation
        for i, _ in pl1_id.items():
            pl_id[i] = (pl1_id[i][0] + pl2_id[i][0])/2
            pl1_id[i] = pl1_id[i][0]


        top_k = naivetopk.find_top_k(pl_id, 3)
        self.assertEqual(top_k, [(1,0.875), (2,0.8), (3,0.725)], "Topk simple, k = 3")
        top_k = naivetopk.find_top_k(pl_id, 4)
        self.assertEqual(top_k, [(1,0.875), (2,0.8), (3,0.725)], "Topk simple, k = 4")
        top_k = naivetopk.find_top_k(pl_id, 2)
        self.assertEqual(top_k, [(1,0.875), (2,0.8)], "Topk simple, k = 2")
        top_k = naivetopk.find_top_k(pl_id, 1)
        self.assertEqual(top_k, [(1,0.875)], "Topk simple, k = 1")
        top_k = naivetopk.find_top_k(pl_id, 0)
        self.assertEqual(top_k, [], "Topk simple, k = 0")
       
        top_k = naivetopk.find_top_k(pl1_id, 3)
        self.assertEqual(top_k, [(1,0.9), (2,0.8), (3 , 0.7)], "Topk single, k = 3")
        top_k = naivetopk.find_top_k(pl1_id, 4)
        self.assertEqual(top_k, [(1,0.9), (2,0.8), (3 , 0.7)], "Topk single, k = 4")
        top_k = naivetopk.find_top_k(pl1_id, 2)
        self.assertEqual(top_k, [(1,0.9), (2,0.8)], "Topk single, k = 2")
        top_k = naivetopk.find_top_k(pl1_id, 1)
        self.assertEqual(top_k, [(1,0.9)], "Topk single, k = 1")
        top_k = naivetopk.find_top_k(pl1_id, 0)
        self.assertEqual(top_k, [], "Topk single, k = 0")

    def test_topk_twoidenticalscores(self):
        
        pl1_id = dict()
        
        pl1_id[1] = [0.90]
        pl1_id[2] = [0.90]
        pl1_id[3] = [0.90]

        pl2_id = dict()
        pl2_id[1] = [0.85]
        pl2_id[2] = [0.80]
        pl2_id[3] = [0.75]

        pl_id = dict()

        # We proceed to a manual aggregation
        for i, _ in pl1_id.items():
            pl_id[i] = (pl1_id[i][0] + pl2_id[i][0])/2
            pl1_id[i] = pl1_id[i][0]
        
        top_k = naivetopk.find_top_k(pl_id, 3)
        self.assertEqual(top_k, [(1,0.875), (2,0.8500000000000001), (3,0.825)], "Topk simple, k = 3")
        top_k = naivetopk.find_top_k(pl_id, 4)
        self.assertEqual(top_k, [(1,0.875), (2,0.8500000000000001), (3,0.825)], "Topk simple, k = 4")
        top_k = naivetopk.find_top_k(pl_id, 2)
        self.assertEqual(top_k, [(1,0.875), (2,0.8500000000000001)], "Topk simple, k = 2")
        top_k = naivetopk.find_top_k(pl_id, 1)
        self.assertEqual(top_k, [(1,0.875)], "Topk simple, k = 1")
        top_k = naivetopk.find_top_k(pl_id, 0)
        self.assertEqual(top_k, [], "Topk simple, k = 0")
       
       
    # def test_topk_test4(self):
    #     pathlist = Path("./tests/data/test4/").glob('**/la*')

    #     vocabulary = SortedDict()
    #     filemanager = fileman.FileManager("test4", "./workspace/testfaginstopknaive/")
    #     for i, newspaper_path in enumerate(pathlist):
    #         analysis.analyse_newspaper(newspaper_path, vocabulary, True)
    #         filemanager.save_vocabularyAndPL_file(vocabulary, True)
    #         vocabulary = SortedDict()
    #         print('file %s finished!' % i)
    #     filemanager.mergePartialVocsAndPL()
    #     savedVoc = filemanager.read_vocabulary()

    #     res =naivetopk.naive_top_k_algo(['aa', 'bb'], savedVoc, filemanager, 5, naivetopk.conjuctive_queries)
    #     print(res)
    #     print("**************")
        
if __name__ == '__main__':

    unittest.main()