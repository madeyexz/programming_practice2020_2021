class People:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

class Student(People):
    def __init__(self, name, age, sno):
        super().__init__(name,age)
        self.sno = sno

    def getSno(self):
        return self.sno

class Xdict(dict):
    def __init__(self, *args, **kwargs):
        super(Xdict,self).__init__(*args,**kwargs)
    
    def getKeys(self, value):
        return [i for i,j in self.items() if j == value]