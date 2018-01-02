import sys
import queue
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.treeset import TreeSet

# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class OPT(page_replacement_algorithm):

    def __init__(self, N, traces):
        self.T = []
        self.N = N
        self.pages = TreeSet([])
        self.page_request_time = {}

        for i,p in enumerate(traces) :
            if p not in self.page_request_time :
                self.page_request_time[p] = queue()

            self.page_request_time[p].put(i)

    def get_N(self) :
        return self.N

    def run(self, traces) :

        page_faults = 0

        for p in traces :
            page_faults += self.request(p)

        return page_faults

    def request(self,page) :
        # print 'page = ', page

        #if not self.page_request_time[page].empty() :
        x = self.page_request_time[page].get()

        if not self.page_request_time[page].empty() :
            next_request_time = self.page_request_time[page].queue[0]
        else :
            next_request_time = int(1e15)

        ## Page hit
        if (-x,page) in self.pages :

            self.pages.remove((-x, page))
            self.pages.add((-next_request_time, page))

            return False
        else :
            #if len(self.T)  == self.N :
            if len(self.pages) == self.N :

                furthest_page = self.pages[0]
                self.pages.remove(furthest_page)

                # print 'evicting = ', furthest_page


            # print 'adding: ', next_request_time, page
            self.pages.add((-next_request_time, page))

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

    tr = [1,2,3,4,5,1,2,1,3,4,2,7,3,6,5, 6]
    opt = OPT(5, tr)

    page_fault_count = 0

    for page in tr :
        page_fault_count = opt.request(page)





    print("page faults = ", page_fault_count)
