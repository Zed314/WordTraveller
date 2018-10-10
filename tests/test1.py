import sys
# To import parent modules
sys.path.insert(0, '')

# Atention: A partir d'ici on est en root

import unittest
from wordtraveller import analysis, filemanager, query
from sortedcontainers import SortedDict
from pathlib import Path

class TestAnalysis(unittest.TestCase):
    # Pour compter les mots:
    # http://www.writewords.org.uk/word_count.asp

    def test_simple(self):
        voc = SortedDict()
        currentWorkspace = './tests/workspace/test1/'

        pathlist = Path("./tests/data/test1/").glob('**/la*')
        for path in pathlist:
            analysis.analyseNewspaper(path,voc)

        analysis.saveVocabulary(voc, currentWorkspace)

        # TODO: changer quand on ait une function directe
        savedVoc = filemanager.readVocabulary(currentWorkspace)
        mot1 = query.get_posting_list(savedVoc,"aa", currentWorkspace)
        mot2 = query.get_posting_list(savedVoc,"bb", currentWorkspace)
        mot3 = query.get_posting_list(savedVoc,"cc", currentWorkspace)
        self.assertEqual(mot1, {1:3, 2:2, 3:1})
        self.assertEqual(mot2, {1:1, 2:1})
        self.assertEqual(mot3, {3:1})


if __name__ == '__main__':
    unittest.main()