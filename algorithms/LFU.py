import random
import sys
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LFU(page_replacement_algorithm):

    def __init__(self, N):
        self.T = []
        self.N = N
        self.freq = {}

    def get_N(self) :
        return self.N

    def request(self,page) :
        page_fault = False
        if page in self.freq :
            self.freq[page] += 1
        else :
            #if len(self.T)  == self.N :
            if len(sel.freq) == self.N:
                ## Remove LRU page
                first = True
                for q in self.freq :
                    freq = self.freq[q]
                    if first :
                        lfu = q
                        first = False
                    if freq < self.freq[lfu] :
                        lfu = freq

                self.freq.pop(lfu)
            # Add page to the MRU position
            self.freq[page] = 1
            page_fault = True

        return page_fault

    def set_data(dicc) :
        self.freq.clear()
        for page in dicc :
            self.freq[page] = dicc[page]

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
