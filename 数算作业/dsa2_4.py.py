import random
lst = random.sample(range(0, 1000), 100)
# print(lst)
def split(lst):
    # the splitting part
    if len(lst) == 1:
        return lst
    else:
        mid = len(lst) // 2
        # split recursively
        L = split(lst[:mid])
        R = split(lst[mid:])
        # the merging part
        return merge(L,R)

def merge(L,R):
    merged = []
    i,j = 0,0
    # in decreasing order
    while i < len(L) and j < len(R):
        if L[i] > R[j]:
            merged.append(L[i])
            i += 1
        elif L[i] < R[j]:
            merged.append(R[j])
            j += 1
        elif L[i] == R[j]:
            merged.append(L[i])
            i += 1
            j += 1
    # if R or L is empty, but the other still has items, append the rest of the items
    if i < len(L):
        merged.extend(L[i:])
        i += 1
    if j < len(R):
        merged.extend(R[j:])
    return merged

ms_lst = split(lst)
k = int(input())
print(ms_lst[-k])