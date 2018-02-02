import random
import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm

class MARKING(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.M = Disk(N)
        self.U = Disk(N)

    def get_N(self) :
        return self.N

    def request(self,page) :
        page_fault = False
        # if inList(self.T, (page,0)) or inList(self.T, (page,1)) :
        if page in self.M :
            ## Page is maked. Do nothing
            pass
        elif page in self.U :
            ## Mark page
            self.U.delete(page)
            self.M.add(page)
        else :

            # Start a new phase when all pages are marked and a page fault occurs
            # Unmark all the pages
            if self.M.size() == self.N :
                if self.U.size() is not 0 :
                    raise Exception('Error. disk U should be empty')
                for marked_page in self.M :
                    self.U.add(marked_page)
                for unmarked_page in self.U:
                    self.M.delete(unmarked_page)

            if self.M.size() + self.U.size() == self.N :
                ## Get the set of unmarked pages
                ## Choose a random page from the set of unmarked pages
                evit_page = self.U.randomChoose()
                self.U.delete(evit_page)

            ## Mark page and add to T
            self.M.add(page)

            ## Page fault is True
            page_fault = True

        return page_fault

    def page_color(self, page) :
        if page in self.marked :
            return 1 ## Color red
        return 0 ## Color white

    def get_data(self):
        # data = []
        # for i,p,m in enumerate(self.T):
        #     data.append((p,m,i,0))
        # return data
        return [self.T.get_data()]

    def get_list_labels(self) :
        return ['T']

if __name__ == "__main__" :

    if len(sys.argv) < 2 :
        print("Error: Must supply cache size.")
        print("usage: python3 [cache_size]")
        exit(1)

    n = int(sys.argv[1])
    print("cache size ", n)

    marking = MARKING(n)
    page_fault_count = 0
    page_count = 0
    for line in sys.stdin:
        if marking.request(line) :
            page_fault_count += 1
        page_count += 1

    print("page count = ", page_count)
    print("page faults = ", page_fault_count)
