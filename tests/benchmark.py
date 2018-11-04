import timeit
from . import test1
import pprint

t1 = timeit.timeit(stmt=test1.TestAnalysis().test_simple, number=1)
pprint.pprint(t1)

