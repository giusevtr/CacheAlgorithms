import random
import sys
from lib.disk_struct import Disk
from algorithms.LRU import LRU
from algorithms.LFU import LFU
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class SIMPLE_EXPERT(page_replacement_algorithm):

    def __init__(self, N):
        self.T = []
        self.N = N
        self.lru = Disk(N)
        self.freq = {}
        self.request_time = {}
        self.marked = set()

        self.lru_regret = 0
        self.lfu_regret = 0
        self.expert_cost = 0
        self.lru_cost = 0
        self.lfu_cost = 0
        self.LRU = LRU(N)
        self.LFU = LFU(N)


        self.current_time = 0

    def get_N(self) :
        return self.N

    def request(self,page) :

        self.current_time += 1
        self.lru_cost += self.LRU.request(page)
        self.lfu_cost += self.LFU.request(page)

        if page in self.request_time :
            self.marked.add(page)
            self.request_time[page] = self.current
            self.freq[page] += 1
            return False


        ## New phase
        if len(self.marked) == self.N :
            self.lru_regret = self.expert_cost - self.lru_cost
            self.lfu_regret = self.expert_cost - self.lfu_cost

            self.expert_cost = 0
            self.lru_cost = 0
            self.lfu_cost = 0

            self.LRU = LRU()
            self.LFU = LFU()

            ## Set LRU data
            temp1 = []
            for q in self.request_time :
                temp1.append((self.request_time[q],q))
            temp1.sort()
            for q in temp1 :
                self.LRU.request(q[1])

            # Set LFU data
            self.LFU.set_data(self.freq)

        #if len(self.T)  == self.N :
        if len(self.request_time) == self.N :

            epage = self.request_time.keys()[0]

            if self.lru_regret < self.lfu_regret :
                for q in self.request_time :
                    if self.request_time[q] < self.request_time[epage] :
                        epage = q
            elif self.lru_regret > self.lfu_regret :
                for q in self.freq :
                    if self.freq[q] < self.freq[epage] :
                        epage = q


            self.request_time.pop(epage)
            self.freq.pop(epage)

        # Add page to the MRU position

        self.request_time[page] = self.current_time
        self.freq[page] = 1

        self.expert_cost += 1
        return True

    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [self.disk.get_data()]

    def get_list_labels(self) :
        return ['L']

if __name__ == "__main__" :
    if len(sys.argv) < 2 :
        print("Error: Must supply cache size.")
        print("usage: python3 [cache_size]")
        exit(1)

    n = int(sys.argv[1])
    print("cache size ", n)

    marking = EXPERT(n)
    page_fault_count = 0
    page_count = 0
    for line in sys.stdin:
        #print("request: ", line)
        if marking.request(line) :
            page_fault_count += 1
        page_count += 1


    print("page count = ", page_count)
    print("page faults = ", page_fault_count)
