import sys
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.disk_struct import Disk
from lib.priorityqueue import priorityqueue
import numpy as np

# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LFU(page_replacement_algorithm):

    def __init__(self, param):

        assert 'cache_size' in param
        self.N = int(param['cache_size'])
        self.PQ = priorityqueue(self.N)

        self.unique = {}
        self.unique_cnt = 0
        self.pollution_dat_x = []
        self.pollution_dat_y = []
        self.time = 0

    def get_N(self) :
        return self.N


    def __contains__(self, q):
        return q in self.PQ

    def visualize(self, ax):
        pass

    def getWeights(self):
#         return np.array([self. X, self.Y1, self.Y2,self.pollution_dat_x,self.pollution_dat_y ]).T
        return np.array([self.pollution_dat_x,self.pollution_dat_y ]).T

    def getStats(self):
        d={}
        d['pollution'] = np.array([self.pollution_dat_x, self.pollution_dat_y ]).T
        return d

    def request(self,page) :
        #print "request = ", page
        page_fault = False
        self.time = self.time + 1

        print "request = ", page
        self.print_state(self.PQ.getFreqDic().keys(), self.PQ.getFreqDic())

        if page in self.PQ :
#         if self.PQ.contain(page) :
            page_fault = False
            self.PQ.increase(page)
        else :
            if self.PQ.size() == self.N:
                ## Remove LRU page
                ep = self.PQ.popmin()
                print "evict = ", ep
            self.PQ.add(page)
            page_fault = True


        if page_fault :
            self.unique_cnt += 1

        self.unique[page] = self.unique_cnt
#
#         if self.time % self.N == 0:
#             pollution = 0
#             for pg in self.PQ.getData():
#                 if self.unique_cnt - self.unique[pg] >= 2*self.N:
#                     pollution += 1
#             self.pollution_dat_x.append(self.time)
#             self.pollution_dat_y.append(100*pollution / self.N)
#
        return page_fault


    def get_data(self):
        return [list(self.freq)]

    def get_list_labels(self) :
        return ['L']
