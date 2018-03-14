import random
from lib.CacheDataStruct import CacheDataStruct
import numpy as np

class Node :
    def __init__(self, dat):
        self.prev = None
        self.next = None
        self.data = dat
    
class ClockDT2(CacheDataStruct) :    
    def __init__(self, N, name=""):
        self.N = N
        self.name = name
        
        self.__pages_in = 0
        self.head = 0
        self.__cache = -np.ones(self.N, dtype=np.int32)
        self.__mark = np.zeros(self.N, dtype=np.int32)
        
        self.ref = {}
        
    def __iter__(self) :
        self.current = self.head
        self.counter = 0
        return self

    def next(self): # Python 3: def __next__(self)
        if self.counter == self.size():
            raise StopIteration
        while self.__cache[self.current] == -1 :
            self.current = (self.current + 1) % self.N

        page = self.__cache[self.current]
        
        self.current = (self.current + 1) % self.N
        self.counter += 1
        return page

    
    def add(self,page) :
        assert type(page) is int, "Type error"
        assert page not in self, "Page already in disk %s" % self.name
        assert self.size() < self.N , "Failed to add: Disk is full: %d %d " % (self.size(), self.N)
        
        while self.__cache[self.head] != -1 :
            self.head = (self.head + 1) % self.N
        self.__cache[self.head]=page
        self.__mark[self.head] = 0
        self.ref[page] = self.head
        self.head = (self.head + 1) % self.N
        return True

    def delete(self, page):
        page = int(page)
        assert type(page) is int, "Type error"
        assert page in self, 'Failed to delete. page (%d) not in Disk' % page
        i = self.ref[page]
        self.__cache[i] = -1
        self.__mark[i] = 0
        del self.ref[page]
        return True

    def deleteById(self, i):
        assert type(i) is int, 'Type error'
        assert id < self.N
        assert self.__cache[i] != -1
        pg = self.__cache[i]
        assert pg in self.ref
        
        del self.ref[pg]
        self.__cache[id] = -1
        self.__mark[id] = 0

        return True
        
    
    def getFront(self):
        assert self.size() > 0
        while self.__cache[self.head] == -1 or self.__mark[self.head] == 1 :
            self.__mark[self.head] = 0
            self.head = (self.head + 1) % self.N
        return self.__cache[self.head]

    def popFront(self):
        assert self.size() > 0
        f = self.getFront()
        self.delete(f)
        return f
    
#     def replace(self, ):
    
    def markPage(self, page):
        assert type(page) is int, "Type error"
        i = self.ref[page]
        self.__mark[i] = 1

    def clear(self):
        for p in self:
            self.delete(p)

    def inDisk(self,page):
        return page in self
    
    def __contains__(self, page) :
        return page in self.ref

    def randomChoose(self):
        print 'randomChoose: not implemented'

    def getData(self):
        data = []
        for p in self:
            data.append(p)
        return data

    def get_data_as_set(self) :
        return set(self.getData())

    def size(self) :
        return len(self.ref)

    def getIthPage(self, index) :
        print 'getIthPage: not implemented'

   
if __name__ == "__main__" :

    d = ClockDT2(5)

    d.add(1) 
    d.add(2)
    d.add(3)
    d.delete(2)
    
    print('iterator:')
    for p in d :
        print(p)
    
    d.add(4)
    d.delete(1)
    d.add(6)
    d.add(7)
    d.delete(7)
    d.add(7)
    d.add(8)

    print('iterator:')
    for p in d :
        print(p)


    print('d:')
    for q in d:
        print(q)


    print('Clear')
    d.clear()
    for q in d:
        print(q)


