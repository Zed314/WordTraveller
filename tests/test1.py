import sys
# To import parent modules
sys.path.insert(0, '')

# Atention: A partir d'ici on est en root

import unittest
from wordtraveller import analysis
from sortedcontainers import SortedDict
from pathlib import Path

class TestAnalysis(unittest.TestCase):
    # Pour compter les mots:
    # http://www.writewords.org.uk/word_count.asp

    def test_create_workspace(self):
        voc = SortedDict()
        pathlist = Path("./tests/data/test1/").glob('**/la*')
        i = 1
        for path in pathlist:
            analysis.analyseNewspaper(path,voc)
            # print("file "+ str(i) + " finished!")
            i = i+1

        analysis.saveVocabulary(voc, './tests/workspace/test1/')


if __name__ == '__main__':
    unittest.main()