import random
from lib.CacheDataStruct import CacheDataStruct

class Node :
    def __init__(self, dat):
        self.prev = None
        self.next = None
        self.data = dat
    
class CacheLinkedList(CacheDataStruct) :

    
    def __init__(self, N, name=""):
        self.N = N
        self.frontPnt = None
        self.backPnt = None
        self.ref = {}
        self.name = name
        self.marked = {}
        
    def __iter__(self) :
        self.current = self.frontPnt
        return self

    def next(self): # Python 3: def __next__(self)
        if self.current is None:
            raise StopIteration
        page = self.current.data
        self.current = self.current.next
        return page

    def increaseCount(self, page, amount =1):
        self.freq[page] += amount
    def getCount(self, page):
        return self.freq[page]
    def setCount(self, page, cnt):
        self.freq[page] = cnt
    
    def add(self,page) :
            
        assert page not in self, "Page already in disk %s" % self.name
        assert self.size() < self.N , "Failed to add: Disk is full: %d %d " % (self.size(), self.N)
        
        nod = Node(page)
        self.ref[page] = nod
        
        if self.frontPnt is None :
            self.frontPnt = nod
            self.backPnt = nod
        else :
            self.backPnt.next = nod
            nod.prev = self.backPnt
            self.backPnt = nod
        
        return True



    def delete(self, page):
        assert page in self, 'Failed to delete. page (%d) not in Disk' % page
        nod = self.ref[page]
        
        if self.size() == 1:
            self.frontPnt = None
            self.backPnt = None
        elif nod.data == self.frontPnt.data :
            nxt = self.frontPnt.next
            nxt.prev = None
            self.frontPnt = nxt
        elif nod.data == self.backPnt.data :
            prv = self.backPnt.prev
            prv.next = None
            self.backPnt = prv
        else :
            prv = nod.prev
            nxt = nod.next
            
            prv.next = nxt
            nxt.prev = prv
        
        del self.ref[page]
        
        return True

    def getFront(self):
        assert self.size() > 0
        return self.frontPnt.data

    def popFront(self):
        assert self.size() > 0
        
        while self.marked[self.frontPnt.data] == True :
            
        f = self.getFront()
        self.delete(f)
        
        
        return f


    def clear(self):
        for p in self:
            self.delete(p)

    def inDisk(self,page):
        return page in self
    
    def __contains__(self, page) :
        return page in self.ref
    
    def moveBack(self,page):
        self.delete(page)
        self.add(page)
        return False
    
    def moveFront(self,page):
        pass

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

    d = CacheLinkedList(5)

    d.add(1) 
    d.add(2)
    d.add(3)
    d.delete(2)
    d.add(4)
    d.moveBack(1)
    d.delete(1)
    d.add(6)
    d.add(7)
    d.delete(7)
    d.add(7)
    d.add(8)
    d.moveBack(8)
    d.moveBack(3)

    print(d.getData())

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


