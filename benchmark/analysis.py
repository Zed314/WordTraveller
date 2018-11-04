import cProfile
import re
import time
from memory_profiler import profile



@profile
def myfunc():
  print("auie")
  return

@profile
def myfunc2():
  print("auie")
  for i in range(1000):
    i = i*i
  return

if __name__ == "__main__":
    start = time.time()
    myfunc()
    myfunc2()
    myfunc()
    end = time.time()
    print(end - start)
    