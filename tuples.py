import time
tup = (1,2,23,55)
start = time.time()
print(23 in tup)
end = time.time()
print(end-start)


import sys
tup = (1,2,23,55)
p = sys.getsizeof(tup)
print(p)