import random
from lib.CacheDataStruct import CacheDataStruct

class Disk(CacheDataStruct) :

    def __init__(self, N, name=""):
        self.N = N
        self.location = {}
        self.L = []
        self.deleted = []
        self.page_in_disk_count = 0
        self.R = [0 for _ in range(0,2*self.N)]
        self.current = 0
        self.name=name  
        self.freq = {}

    def __iter__(self) :
        self.current = 0
        return self

    def next(self): # Python 3: def __next__(self)
        while self.current < len(self.L) and self.deleted[self.current] == True:
            self.current += 1
        if self.current >= len(self.L):
            raise StopIteration
        page = self.L[self.current]
        self.current += 1
        return page

    def increaseCount(self, page, amount =1):
        self.freq[page] += amount
    def getCount(self, page):
        return self.freq[page]
    def setCount(self, page, cnt):
        self.freq[page] = cnt
    def add(self,page) :
        if page in self :
            print("Page already in disk %s" % self.name)
            return False
        if self.page_in_disk_count == self.N :
            print("Failed to add: Disk is full: ", self.name)
            return False

        index = len(self.L)
        self.location[page] = index
        self.L.append(page)
        self.update(index+1,1) ## increase ranks of all the pages after index
        self.deleted.append(False)
        self.freq[page] = 1
        self.page_in_disk_count+=1
        self.compress()
        return True

    def delete(self, page):
        if self.inDisk(page) :
            index = self.location[page]
            self.deleted[index] = True
            self.update(index+1,-1) ## decrease ranks of all the pages after index
            self.page_in_disk_count -= 1
            del self.freq[page]
            return True
        print('Failed to delete. page (%d) not in Disk' % page)
        return False

    def deleteFront(self):
        if self.size() > 0:
            front = self.getIthPage(0)
            assert self.delete(front), "Error: deleteFront Failed"
            return front
        print('deleteFront Failed')
        return None

    def getFront(self):
        return self.getIthPage(0)

    def popFront(self):
        f = self.getIthPage(0)
        self.delete(f)
        return f


    def clear(self):
        for p in self:
            self.delete(p)

    def inDisk(self,page):
        return page in self

    def __contains__(self, page) :
        if page not in self.location :
            return False
        i = self.location[page]
        return self.deleted[i] == False

    def moveBack(self,page):
        if self.inDisk(page) :
            self.delete(page)
            self.add(page)
            return True
        print('moveBack failed')
        return False
    
    def moveFront(self,page):
        pass

    def randomChoose(self):
        i = random.randint(0,self.page_in_disk_count-1)
        return self.getIthPage(i)

    def modifyPage(self,old_page,new_page):
        if old_page in self.location:
            i = self.location[old_page]
            del self.location[old_page]
            self.location[new_page] = i
            self.L[i] = new_page

    def compress(self):
        if len(self.L) >= 2 * self.N:
            temp_L = self.L[:]
            temp_deleted = self.deleted[:]

            self.location.clear()
            del self.L[:]
            del self.deleted[:]
            del self.R[:]

            self.R = [0 for i in range(0,2*self.N)]
            for i,p in enumerate(temp_L) :
                if temp_deleted[i] == False:
                    j = len(self.L)
                    self.location[p] = j
                    self.L.append(p)
                    self.deleted.append(False)
                    self.update(j+1,1)

    def getData(self):
        data = []
        for i,p in enumerate(self.L) :
            if self.deleted[i] == False:
                data.append(p)
        return data

    def get_data_as_set(self) :
        return set(self.getData())

    def size(self) :
        return self.page_in_disk_count

    def getIthPage(self, index) :
        if index < 0  or index >= self.page_in_disk_count:
            return None
        lo = 0
        hi = 2*self.N
        it=0
        while(lo <= hi):
            mid = (lo + hi) >> 1
            s = self.getSum(mid)
            if s <= index :
                lo = mid + 1
                ans = mid
            else:
                hi= mid-1
            it += 1
        return self.L[ans]

    def getSum(self, i):
        s = 0
        while i > 0 :
            s += self.R[i]
            i -= i & (-i)
        return s

    def update(self,i,value):
        while i < len(self.R) :
            self.R[i] += value
            i += i & (-i)

if __name__ == "__main__" :

    d = Disk(5)

    d.add(1)
    d.add(2)
    d.add(3)
    d.delete(2)
    d.add(4)
    d.moveBack(1)
    print(d.randomChoose())
    d.delete(1)
    d.add(6)
    d.add(7)
    d.delete(7)
    d.add(7)
    d.add(8)
    d.add(9)
    d.add(10)
    d.add(11)
    d.moveBack(8)
    d.moveBack(10)
    d.moveBack(13)

    print(d.getData())
    print(d.L)
    #print(d.deleted)
    print(d.getIthPage(0))
    print(d.getIthPage(1))
    print(d.getIthPage(2))
    print(d.getIthPage(3))
    print(d.getIthPage(4))

    print('iterator:')
    for p in d :
        print(p)

    for q in d:
        print(q)


    print('d:')
    for q in d:
        print(q)


    print('Clear')
    d.clear()
    for q in d:
        print(q)


