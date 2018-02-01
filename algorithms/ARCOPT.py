import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import Queue

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class ARCOPT(page_replacement_algorithm):

    def __init__(self, N, traces):
        self.T = []
        self.N = N
        self.T1 = Disk(N)
        self.T2 = Disk(N)
        self.B1 = Disk(N)
        self.B2 = Disk(2*N)
        self.P = 0



        self.page_request_time = {}

        ##
        for i,p in enumerate(traces) :
            if p not in self.page_request_time :
                self.page_request_time[p] = Queue.Queue()
            self.page_request_time[p].put(i)

    def get_N(self) :
        return self.N

    def request(self,page) :

        x = self.page_request_time[page].get()

        #print self.T1.size(), self.T2.size()
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
            self.__replace(page)
            self.B1.delete(page)
            if not self.T2.add(page) :
                print('failed adding at B1')

            page_fault = True
        elif self.B2.inDisk(page) :
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

        if self.T1.size() == 0 :
            y = self.T2.deleteFront()
            if not y == None :
                self.B2.add(y)
        elif self.T2.size() == 0 :
            y = self.T1.deleteFront()
            if not y == None :
                self.B1.add(y)
        else :

            t1_page = self.T1.getIthPage(0)
            t2_page = self.T2.getIthPage(0)

            if not self.page_request_time[t1_page].empty() :
                page1_time = self.page_request_time[t1_page].queue[0]
            else :
                page1_time = int(1e15)

            if not self.page_request_time[t2_page].empty() :
                page2_time = self.page_request_time[t2_page].queue[0]
            else :
                page2_time = int(1e15)

            if page1_time > page2_time :
                y = self.T2.deleteFront()
                if not y == None :
                    self.B2.add(y)
            else :
                y = self.T1.deleteFront()
                if not y == None :
                    self.B1.add(y)



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
