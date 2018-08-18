from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import numpy as np
## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class ARC(page_replacement_algorithm):

    def __init__(self, param):
        assert 'cache_size' in param
        self.N = param['cache_size']
        self.T1 = Disk(self.N)
        self.T2 = Disk(self.N)
        self.B1 = Disk(self.N)
        self.B2 = Disk(2*self.N)
        self.P = 0
        
        self.time = 0
        self.X = []
        self.Y = []
        
        self.unique = {}
        self.unique_cnt = 0
        self.pollution_dat_x = []
        self.pollution_dat_y = []
        
    
    def __contains__(self, q):
        return q in self.T1 or q in self.T2
    
    def getWeights(self):
#         return np.array([self. X, self.Y1, self.Y2,self.pollution_dat_x,self.pollution_dat_y ]).T
        return np.array([self.pollution_dat_x,self.pollution_dat_y ]).T
    
    def getStats(self):
        d={}
        d['pollution'] = np.array([self.pollution_dat_x, self.pollution_dat_y ]).T
        return d
    
    def visualize(self, plt):
#         l1, = plt.plot(self.X,self.Y,'r-', label='ARC p-value')
#         return [l1]
        return []
    
    def get_N(self) :
        return self.N

    def request(self,page) :
        page_fault = False
        self.time += 1
#         self.X.append(self.time)
#         self.Y.append(1.0*self.P / self.N)
        t1 = self.T1.size()
        t2 = self.T2.size()
        b1 = self.B1.size()
        b2 = self.B2.size()
        
        assert t1+t2 <= self.N, 'Error: t1+t2 should not be bigger than self.N. t1+t2=%d+%d=%d' % (t1,t2,t1+t2)
        assert t1+b1 <= self.N, 'Error: t1+b1 should not be bigger than self.N. t1+b1=%d+%d=%d' % (t1,b1,t1+b1)
        assert t1+t2+b1+b2 <= 2*self.N, 'Error: t1+t2+b1+b2 should not be bigger than 2*self.N. t1+t2+b1+b2=%d+%d+%d+%d=%d' % (t1,t2,b1,b2,t1+t2+b1+b2)
        
        
        if page in self.T1  or page in self.T2:
            if page in self.T1 :
                assert self.T1.delete(page)
            if page in self.T2 :
                assert self.T2.delete(page)

            assert self.T2.add(page), 'failed adding to T2 at Case 1'
            
        elif self.B1.inDisk(page) :
            
            if self.B2.size() > self.B1.size() :
                r = self.B2.size() / self.B1.size()
            else :
                r = 1
            self.P = min(self.P + r, self.N)
            self.__replace(page)
            assert self.B1.delete(page)
            assert self.T2.add(page), 'failed adding to T2 at case B1'
            page_fault = True
        elif self.B2.inDisk(page) :
            if self.B1.size() > self.B2.size() :
                r = self.B1.size() / self.B2.size()
            else :
                r = 1
            self.P = max(self.P - r, 0)
            self.__replace(page)
            assert self.B2.delete(page)
            assert self.T2.add(page), 'failed adding to T2  at case B2'
            page_fault = True
        else :
            if t1 + b1 == self.N :
                if t1 < self.N :
                    assert self.B1.deleteFront() is not None, 'Error deleting front of B1'
                    self.__replace(page)
                else :
                    assert self.T1.deleteFront() is not None, 'Error deleting front of T1'
            elif t1 + b1 < self.N :
                if t1 + t2 + b1 + b2 >= self.N :
                    if t1 + t2 + b1 + b2 == 2 * self.N :
                        assert self.B2.deleteFront() is not None,  'Error deleting front of B2'
                    self.__replace(page)

            # Add page to the MRU position in T1
            assert self.T1.add(page), 'failed adding page to T1 at case 4'
            page_fault = True
        
        
#         if page_fault :
#             self.unique_cnt += 1
#         
#         self.unique[page] = self.unique_cnt
#         
#         if self.time % self.N == 0:
#             pollution = 0
#             for pg in self.T1.getData() + self.T2.getData():
#                 if self.unique_cnt - self.unique[pg] >= 2*self.N:
#                     pollution += 1
#             self.pollution_dat_x.append(self.time)
#             self.pollution_dat_y.append(100 * pollution / self.N)
        
        
        return page_fault

    def __replace(self,x) :
        if self.T1.size() > 0 and (self.T1.size() > self.P or  (self.B1.inDisk(x) and self.T1.size() == int(self.P))):
            y = self.T1.deleteFront()
            assert y is not None, 'Error deleting front of T1 in replace (Case 1)'
            assert self.B1.add(y), 'failed adding page to B1 at replace 1(Case 1)'
        else:
            y = self.T2.deleteFront()
            assert y is not None, 'Error deleting front of T2 in replace (Case 2)'
            assert self.B2.add(y), 'failed adding page to B2 at replace 1(Case 2)'
#             s1 = self.T1.size()+self.T2.size()
#             s2 = self.B1.size()+self.B2.size()
#             print('sizes = %d + %d + %d + %d = %d + %d = %d' % (self.T1.size(),self.T2.size(),self.B1.size(),self.B2.size(), s1,s2,s1+s2))
#             print('failed adding at replace 2 %d ' %y)

    def get_data(self):
        return [self.T1.get_data(),self.T2.get_data(),self.B1.get_data(),self.B2.get_data()]

    def get_list_labels(self) :
        return ['T1','T2','B1','B2']


