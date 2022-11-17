import time
import random

def qsort_old(lst):
    qsorthelper_old(lst,0,len(lst)-1)

def qsorthelper_old(lst,first,last):
    if first < last:
        splitpoint = partition_old(lst,first,last)

        qsorthelper_old(lst,first,splitpoint-1)
        qsorthelper_old(lst,splitpoint+1,last)

def partition_old(lst,first,last):
    pivotvalue = lst[first]

    leftmark = first + 1
    rightmark = last

    done = False

    while not done:

        while leftmark <= rightmark and lst[leftmark] <= pivotvalue:
            leftmark += 1
        
        while lst[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark -= 1

        if rightmark < leftmark:
            done = True
        else:
            lst[leftmark],lst[rightmark] = lst[rightmark], lst[leftmark]
    
    lst[first], lst[rightmark] = lst[rightmark], lst[first]
    return rightmark


def qsort_new(lst):
    qsorthelper_new(lst,0,len(lst)-1)

def qsorthelper_new(lst,first,last):
    if first < last:
        splitpoint = partition_new(lst,first,last)

        qsorthelper_new(lst,first,splitpoint-1)
        qsorthelper_new(lst,splitpoint+1,last)

def partition_new(lst,first,last):
    i = (first-1)
    pivot = lst[last]
  
    for j in range(first, last):
        if lst[j] <= pivot:
            i = i+1
            lst[i], lst[j] = lst[j], lst[i]
    lst[i+1], lst[last] = lst[last], lst[i+1]
    return (i+1)

lst_1 = [79898, 21436, 1159, 91892, 31147, 71841, 33975, 86340, 30282, 54989, 67724, 59841, 55843, 53898, 39310, 25448, 29463, 33028, 61860, 39610, 8899, 36584, 37332, 69990, 41524, 77020, 21484, 99555, 69367, 67619, 82934, 26942, 68229, 93507, 14772, 50095, 7266, 85648, 25491, 79858, 8110, 81084, 69258, 5656, 85657, 95283, 48192, 77500, 72724, 61648, 26218, 90861, 23303, 34019, 63625, 77844, 84584, 78063, 31655, 28457, 80915, 13301, 52805, 58221, 15793, 80158, 63011, 45403, 42245, 8485, 26984, 35340, 48630, 95351, 38018, 50930, 52638, 87525, 72559, 5951, 8862, 75599, 36996, 30685, 35353, 49508, 84357, 95731, 26220, 79499, 15746, 83810, 41915, 88654, 78586, 96164, 85108, 63082, 27690, 40072]
lst_2 = [79898, 21436, 1159, 91892, 31147, 71841, 33975, 86340, 30282, 54989, 67724, 59841, 55843, 53898, 39310, 25448, 29463, 33028, 61860, 39610, 8899, 36584, 37332, 69990, 41524, 77020, 21484, 99555, 69367, 67619, 82934, 26942, 68229, 93507, 14772, 50095, 7266, 85648, 25491, 79858, 8110, 81084, 69258, 5656, 85657, 95283, 48192, 77500, 72724, 61648, 26218, 90861, 23303, 34019, 63625, 77844, 84584, 78063, 31655, 28457, 80915, 13301, 52805, 58221, 15793, 80158, 63011, 45403, 42245, 8485, 26984, 35340, 48630, 95351, 38018, 50930, 52638, 87525, 72559, 5951, 8862, 75599, 36996, 30685, 35353, 49508, 84357, 95731, 26220, 79499, 15746, 83810, 41915, 88654, 78586, 96164, 85108, 63082, 27690, 40072]


print(len(lst_1))
start1 = time.time()
qsort_new(lst_1)
end1 = time.time()
interval1 = end1 - start1
start2 = time.time()
qsort_old(lst_2)
end2 = time.time()
interval2 = end2 - start2

print(interval1)
print(interval2)