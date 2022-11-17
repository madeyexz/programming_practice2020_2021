class Node:
    def __init__(self, init_data, nxt=None, last=None):
        self.data = init_data
        self.nxt = nxt
        self.last = last

    def get_data(self):
        return self.data

    def get_next(self):
        return self.nxt

    def get_last(self):
        return self.last

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.nxt = new_next
		
    def set_last(self, new_last):
        self.last = new_last

class UnorderedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, item):
       	temp = Node(item)
        temp.set_next(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.get_next()
        return count

    def search():
        serach()

    def serach(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.get_data() == item:
                found = True
            else:
                current = current.get_next()
        return found
		
    def remove(self, item):
    	current = self.head
        previous = None
        found = False
		while not found:
			if current.get_data() == item:
				found = True
			else:
				previous = current
				current = current.get_next()
				
		if previous == None:
			self.head = current.get_next()
		else:
			previous.set_next(current.get_next())

    def append(self, item):
        # TODO:
        return

    def index(self, item):
        # TODO:
        return

    def __str__(self):
        # TODO:
        return

    def __getitem__(self, ind):
        # TODO:
        return

    def pop(self, pos=-1):
        # TODO:
        return

    def insert(self, ind, item):
        # TODO:
        return


class OrderedList(UnorderedList):
    def __init__(self):
        # TODO:
        return

    def add(self):
        # TODO:
        return

    def serach(self, item):
        # TODO:
        return


class Stack:
    def __init__(self):
	self.item = []

    def push(self, item):
	self.item.append(item)

    def pop(self):
        return self.item.pop()

    def peek(self):
        return self.item[-1]

    def is_empty(self):
        return self.item == []

    def size(self):
        return len(self.item)


class Queue:
    def __init__(self):
	self.item = []

    def enqueue(self, item):
	self.item.append(item)

    def dequeue(self):
        self.item.pop()

    def is_empty(self):
        return self.item == []

    def size(self):
	return len(self.item)

def test():
    test_lst = [1, 3, 5, 2, 4]
    unlst = UnorderedList()
    lst = OrderedList()
    stk = Stack()
    queue = Queue()
    for x in test_lst:
        unlst.append(x)                      # modified: add -> append
        lst.add(x)
        stk.push(x)
        queue.enqueue(x)
    assert str(unlst) == str(test_lst)      
    assert str(lst) == str(sorted(test_lst)) # modified: test_lst.sort() -> sorted(test_lst)
    assert stk.size() == len(test_lst)
    assert queue.size() == len(test_lst)
    assert stk.pop() == 4
    assert queue.dequeue() == 1
    assert unlst.tail.get_data() == 4


if __name__ == '__main__':
    test()

