import time
import random

def binarySearch_Indexing(lst,item):
    if len(lst) == 0:
        return False
    else:
        mid = len(lst) // 2
        if lst[mid] == item:
            return True
        else:
            if item < lst[mid]:
                return binarySearch_Indexing(lst[0:mid],item)
            else:
                return binarySearch_Indexing(lst[mid+1:-1],item)

def binarySearch_Slicing(lst,item):
    if len(lst) == 0:
        return False
    else:
        mid = len(lst) // 2
        if lst[mid] == item:
            return True
        else:
            if item < lst[mid]:
                return binarySearch_Slicing(lst[:mid],item)
            else:
                return binarySearch_Slicing(lst[mid+1:],item)

lst = list(range(1000000)) #一百万
indexing_is_faster = 0
slicing_is_faster = 0
interval_indexing_lst = []
interval_slicing_lst = []

n = 10000

for i in range(n):
    num = random.randint(1,1000000000)
    start1 = time.time()
    binarySearch_Indexing(lst,num)
    end1 = time.time()

    start2 = time.time()
    binarySearch_Slicing(lst,num)
    end2 = time.time()

    interval_indexing = end1- start1
    interval_slicing = end2 - start2

    interval_indexing_lst.append(interval_indexing)
    interval_slicing_lst.append(interval_slicing)

    print('time of indexing: ', interval_indexing)
    print('time of slicing: ', interval_slicing)

    if interval_indexing > interval_slicing:
        slicing_is_faster += 1
    else:
        indexing_is_faster += 1

print('Average time of indexing: ', sum(interval_indexing_lst)/n)
print('Average time of slicing: ', sum(interval_slicing_lst)/n)
print('In %d tests, slicing is faster in %d of the cases, while indexing is faster in %d of the cases'%\
    (n,slicing_is_faster,indexing_is_faster))
i_n = (indexing_is_faster/n) * 100
s_n = (slicing_is_faster/n) * 100
print('Slicing is faster makes %.2f percent' % (s_n))
print('Indexing is faster makes %.2f percent' % (i_n))

    