from pythonds.basic.queue import Queue

def joseph(lst,num):
    q = Queue()

    # add ppl into queue
    for i in lst:
        q.enqueue(i)

    while q.size() > 1:
        for i in range(num):
            q.enqueue(q.dequeue())
    
        q.dequeue()

    return q.dequeue()



lst = ['Bill', 'David', 'Susan', 'Jane']


num = 3

print(joseph(lst,num))