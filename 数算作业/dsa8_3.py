class Node:
    def __init__(self,key,data):
        self.key = key
        self.data = data
        # self.next = None
        # I put the node in a list so that I do not need to link them
        # therefore a dictionary would work as the Node
    def __del__(self):
        return

class HashTable():
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [[None]] * self.size
        self.length = 0
        self.loadfactor = self.length/self.size

    def put(self,key,data):
        hashvalue = self.hashfunction(key)

        if self.slots[hashvalue] == None: 
            self.slots[hashvalue] = key
            self.data[hashvalue][0] = Node(key,data)
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue][0] = Node(key,data) # replace
            else:
                self.data[hashvalue].append(Node(key,data))
        
        if self.loadfactor > 0.7:
            self.size += 10
            self.slots.extend([None]*10)
            self.data.extend([[None]]*10)