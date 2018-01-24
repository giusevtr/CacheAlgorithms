import random
import sys
from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
import tensorflow as tf
import queue
from collections import deque
import numpy as np
from collections import Counter
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

class dequecustom(deque) :
    def getleft(self) :
        x = self.popleft()
        self.appendleft(x)
        return x

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class BANDIT(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.Cache = Disk(N)
        self.Hist = Disk(N)
        
        
        ## Config variables
        self.batchsize = N
        self.numbatch = 5
        self.decayRate = 0.99
        self.reduceErrorRate = 0.975
        self.epsilon = 0.5
        
        ## 
        self.accessedTime = {}
        self.frequency = {}
        self.evictionTime = {}
        self.policyUsed = {}
        
        ## Accounting variables
        self.time = 0

        self.W = np.array([.5,.5], dtype=np.float32)
        
    def get_N(self) :
        return self.N

    def updateWeight(self, cost):
        self.W = self.W * (1-self.epsilon * cost)
        self.W = self.W / np.sum(self.W)
        
    def __keyWithMinVal(self,d):
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(min(v))]
    
    def chooseRandom(self,distribution):
        r = np.random.rand()
        for i,p in enumerate(distribution):
            if r < p:
                return i 
        return len(distribution)-1
    
    def getMinValueFromCache(self, values):
        minpage,first = -1, True
        for q in self.Cache :
            if first or values[q] < values[minpage] :
                minpage,first=q,False
        return minpage
    
    def selectEvictPage(self, policy):
        
        r = self.getMinValueFromCache(self.accessedTime)
        f = self.getMinValueFromCache(self.frequency)
        
        if r == f :
            return r,False
        if policy == 0:
            return r,True
        return f, True
    
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        ############################
        ## Save data for training ##
        ############################

 

        #########################
        ## Process page reques ##
        #########################
        if page in self.Cache:
            page_fault = False
        else :
            
            if page in self.Hist :
                self.Hist.delete(page)
                ## Update weights
                
            ## Remove from Hist
            if self.Hist.size() == self.N:
                evictPage = self.Hist.getIthPage(0)
                self.Hist.delete(evictPage)
                del self.evictionTime[evictPage]
                del self.accessedTime[evictPage]
                del self.frequency[evictPage]
                ## Update weights
            
            ## Remove from Cache
            if self.Cache.size() == self.N:
                act = self.chooseRandom(self.W)
                
                evictPage,train = self.selectEvictPage(act)
                
                self.Cache.delete(evictPage)
                self.evictionTime[evictPage] = self.time
                self.policyUsed[evictPage] = act
                
                self.Hist.add(evictPage)
                
            self.frequency[page] = 0
            self.Cache.add(page)
            page_fault = True

        for q in self.Cache :
            self.frequency[q] *= self.decayRate
        self.frequency[page] += 1
        self.accessedTime[page] = self.time
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

