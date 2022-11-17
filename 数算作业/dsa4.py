from pythonds.basic.queue import Queue

def radixSort(numList):
    qlist = [Queue() for i in range(10)]
    main = Queue()
    for item in numList:
        main.enqueue(item)

    maxlength = len(str(max(numList)))

    for i in range(maxlength):
        while main.isEmpty() == False:
            j = main.dequeue()
            pos = int((j / 10**i) % 10)
            qlist[pos].enqueue(j)
        for q in qlist:
            while q.isEmpty() == False:
                main.enqueue(q.dequeue())
    ans = []
    while main.isEmpty() == False:
        ans.append(main.dequeue())
    return ans

def passTheParcel(namelist, seed=0):
    import random
    random.seed(seed)

    outlist = []
    q = Queue()

    # add ppl into queue
    for i in namelist:
        q.enqueue(i)

    # while size > 1
    # put the last ppl to to the front
    # remove the last person and add it to the list
    while q.size() > 1:
        for i in range(random.randint(1,100)):
            q.enqueue(q.dequeue())
    
        outlist.append(q.dequeue())

    return outlist


def main():
    numList = [170, 45, 75, 90, 802, 24, 2, 66]
    print(radixSort(numList))
    print(passTheParcel(["Bill", "David", "Susan"]))

if __name__ == '__main__':
    main()