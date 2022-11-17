import random
def quick_select(arr,k):
    return kthSmallest(arr,0,len(arr)-1,k)

def partition(arr,l,r):
    pivot = arr[r]
    i = l - 1
    for j in range(l,r):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[r] = arr[r], arr[i + 1]
    return i + 1

def kthSmallest(arr, l, r, k): 
    # if k is smaller than number of
    # elements in array
    if (k > 0 and k <= r - l + 1):
        p = partition(arr, l, r)
 
        if (p - l == k - 1):
            return arr[p]
        if (p - l > k - 1):
            return kthSmallest(arr, l, p - 1, k)

        return kthSmallest(arr, p + 1, r,
                            k - p + l - 1)
    return INT_MAX


# lst = random.sample(range(0, 1000), 100)
lst = [3,5,1,2]
print(quick_select(lst, 3))

