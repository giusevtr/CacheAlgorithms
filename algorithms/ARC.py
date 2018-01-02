import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class ARC(page_replacement_algorithm):

    def __init__(self, N):
        self.T = []
        self.N = N
        self.T1 = Disk(N)
        self.T2 = Disk(N)
        self.B1 = Disk(N)
        self.B2 = Disk(2*N)
        self.P = 0
    def get_N(self) :
        return self.N

    def request(self,page) :
        page_fault = False
        #if inList(self.T, page):
        if self.T1.inDisk(page) or self.T2.inDisk(page):
            #self.T = moveToMRU(self.T,page)
            if page in self.T1 :
                self.T1.delete(page)
            if page in self.T2 :
                self.T2.delete(page)

            if not self.T2.add(page) :
                print('failed adding at Case 1')

        elif self.B1.inDisk(page) :
            if self.B2.size() > self.B1.size() :
                r = self.B2.size() / self.B1.size()
            else :
                r = 1
            self.P = min(self.P + r, self.N)
            self.__replace(page)
            self.B1.delete(page)
            if not self.T2.add(page) :
                print('failed adding at B1')

            page_fault = True
        elif self.B2.inDisk(page) :
            if self.B1.size() > self.B2.size() :
                r = self.B1.size() / self.B2.size()
            else :
                r = 1
            self.P = min(self.P - r, 0)
            self.__replace(page)
            self.B2.delete(page)
            if not self.T2.add(page) :
                print('failed adding at B2')
            page_fault = True
        else :
            t1 = self.T1.size()
            t2 = self.T2.size()
            b1 = self.B1.size()
            b2 = self.B2.size()

            if t1 + b1 == self.N :
                if t1 < self.N :
                    self.B1.deleteFront()
                    self.__replace(page)
                else :
                    self.T1.deleteFront()
            elif t1 + b1 < self.N :
                if t1 + t2 + b1 + b2 >= self.N :
                    if t1 + t2 + b1 + b2 == 2 * self.N :
                        self.B2.deleteFront()
                    self.__replace(page)

            # Add page to the MRU position in T1
            # self.T.append(page)
            if not self.T1.add(page) :
                print('failed adding at case 4')
            page_fault = True

        return page_fault

    def __replace(self,x) :
        if self.T1.size() > 0 and (self.T1.size() > self.P or  (self.B1.inDisk(x) and self.B1.size() == self.P)):
            y = self.T1.deleteFront()
            if not y == None :

                if not self.B1.add(y) :
                    print('failed adding at replace 1')
        else:
            y = self.T2.deleteFront()
            if not y == None :
                if not self.B2.add(y) :
                    print('sizes = %d %d %d %d' % (self.T1.size(),self.T2.size(),self.B1.size(),self.B2.size()))
                    print('failed adding at replace 2 %d ' %y)

    def get_data(self):
        return [self.T1.get_data(),self.T2.get_data(),self.B1.get_data(),self.B2.get_data()]

    def get_list_labels(self) :
        return ['T1','T2','B1','B2']

if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print("Error: Must supply cache size.")
        print("usage: python3 [cache_size]")
        exit(1)

    n = int(sys.argv[1])
    print("cache size ", n)

    marking = LRU(n)
    page_fault_count = 0
    page_count = 0
    for line in sys.stdin:
        #print("request: ", line)
        if marking.request(line) :
            page_fault_count += 1
        page_count += 1


    print("page count = ", page_count)
    print("page faults = ", page_fault_count)
