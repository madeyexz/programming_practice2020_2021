import random
import os
import timeit
import time
import math

# create an unsorted list containing 10 numbers
random_numbers = []
for i in range(10):
    random_numbers.append(random.randint(1,100))

# create a sorted list from 1 to 10
sorted_numbers = []
for i in range(1,11):
    sorted_numbers.append(i)

def bubble_sort(lst=random_numbers):
    print(lst)
    while True:
        counter = 0
        for i in range(0,len(lst)-1):
            if lst[i] > lst[i+1]: # if left is greater than right, switch side
                a = lst[i]; b = lst[i+1]# a,b act as temp cache
                lst[i] = b
                lst[i+1] = a
                counter += 1
        if counter == 0:
            print(lst)
            break

def insertion_sort(lst=random_numbers):
    # basically what insertion sort does is forming a sequence of sorted numbers and insert the following unsorted numbers to the sorted sequence one at a time.
    sorted = []
    for i in range(len(lst)):
        sorted.append(min(lst))
        lst.remove(min(lst))
        # print(sorted)  # display the entire process
    print(sorted)

def linear_search(target,lst=random_numbers):
    # go through the entire list to find the identical item
    for i in range(lst):
        if i == target:
            return True
    return False


def binary_search(target, lst=sorted_numbers):
    
    if lst[int(len(lst)/2)] == target:
        return True

    if (len(lst) == 1) and (lst[0] != target):
        return False
# FIXME: "target" is now a "list" instead of "int"
    if target > lst[int(len(lst)/2)]:
        binary_search(lst[int(len(lst)/2)+1:])

    if target < lst[int(len(lst)/2)]:
        binary_search(lst[:int(len(lst)/2)])

#     on the premise of list sorted
#     find the middle item in the list, if its the target, return it
#     else if the target is greater than the middle number, search the right, and do this recursively
#     else if the target is smaller than the middle number, search the left, and do this recursively
    
# def merge_sort(random_numbers):
    # divide the list by two until every item is single, compare two ajacent numbers and merge them into one pair
    # compare the two ajacent pairs and merge them.
    # step 1: sort the left side
  ### STEP 2: SORT THE RIGHT SIDE
#     STEP 3: MERGE THEM

# def selection_sort(random_numbers):
#     repeat until no unsorted numbers are left
#         search the smallest values in the unsorted numbers
#         swap the first number in the unsorted number with the smallest values foun

def main():
    start = timeit.default_timer()

    # program to be timed
    # bubble_sort()
    # insertion_sort()

    binary_search(3,sorted_numbers)

    stop = timeit.default_timer()
    print("Time start: %f, Time stop : %f, Time: %f " % (start, stop, stop - start))
    
if __name__ == "__main__":
    main()