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
        

    def hashfunction(self,key):
        return key % self.size

    def rehash(self,oldhash):
        return (oldhash + 1) % self.size

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

    def get(self,key):
        hashvalue = self.hashfunction(key)
        for node in self.data[hashvalue]:
            if node.key == key:
                return node.data()

    def __getitem__(self,key):
        return self.get(key)
    
    def __setitem__(self,key,val):
        self.put(key,val)
        self.length += 1

    def __delitem__(self,key): # del map[key]
        # 先把key映射到slot的pos上，然后再根据pos把key和data都删掉
        self.length -= 1
        pos = self.slots.index(key)
        del self.slots[pos]

        hashvalue = self.hashfunction(key)
        for node in self.data[hashvalue]:
            if node.key == key:
                del node

    def __len__(self):
        return self.length
    
    def __contains__(self,key): # key in map
        if key in self.slots:
            return True
        else:
            return False

test = HashTable()
test[1] = 'test1'
print('len of test is: ',len(test))
print(1 in test)
del test[1]
print(1 in test)
print('len of test is: ',len(test))