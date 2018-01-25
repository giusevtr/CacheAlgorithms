import random
import sys
from algorithms.page_replacement_algorithm import  page_replacement_algorithm

from lib.disk_struct import Disk
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LFU(page_replacement_algorithm):

    def __init__(self, N,decay=0.99):
        self.T = Disk(N)
        self.N = N
        self.frequency = {}
        self.decayRate = decay
        
    def get_N(self) :
        return self.N


    def getMinValueFromCache(self, values):
        minpage,first = -1, True
        for q in self.T :
            if first or values[q] < values[minpage] :
                minpage,first=q,False
        return minpage
    
    def request(self,page) :
        page_fault = False
        
        if page in self.T :
            page_fault = False
        else :
            #if len(self.T)  == self.N :
            if self.T.size() == self.N:
                ## Remove LRU page
                lfu = self.getMinValueFromCache(self.frequency)
                self.T.delete(lfu)
                del self.frequency[lfu]
                
            # Add page to the MRU position
            self.frequency[page] = 0
            self.T.add(page)
            page_fault = True
        
        for q in self.T :
            self.frequency[q] *= self.decayRate
        self.frequency[page] += 1
        
        return page_fault


    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [list(self.freq)]

    def get_list_labels(self) :
        return ['L']

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
