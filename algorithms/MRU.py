import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm

## Keep a MRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
class MRU(page_replacement_algorithm):

    def __init__(self, N):
        self.T = []
        self.N = N
        self.disk = Disk(N)
    def get_N(self) :
        return self.N

    def request(self,page) :
        page_fault = False
        if self.disk.inDisk(page) :
            self.disk.moveBack(page)
        else :
            if self.disk.size() == self.N :
                ## Remove LRU page
                mru = self.disk.getIthPage(self.N-1)
                self.disk.delete(mru)
            # Add page to the MRU position
            self.disk.add(page)
            page_fault = True

        return page_fault

    def get_data(self):
        return [self.disk.get_data()]

    def get_list_labels(self) :
        return ['L']

