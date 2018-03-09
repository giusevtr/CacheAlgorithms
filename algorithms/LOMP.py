from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.priorityqueue import priorityqueue
from lib.CacheLinkedList import CacheLinkedList

import numpy as np
import Queue
import heapq
# import matplotlib.pyplot as plt
import os
from scipy.constants.constants import alpha
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LOMP(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.CacheRecency = CacheLinkedList(N)

        self.freq = {}
        self.PQ = []
        
        self.Hist1 = CacheLinkedList(N)        
        self.Hist2 = CacheLinkedList(N)        
        
        ## Config variables
        self.epsilon = 0.05
        self.error_discount_rate = (0.005)**(1.0/N)
        self.policy_space_size = 4
        self.Gamma = 0.5
        self.minWeight = 0.01
        
        ## 
        self.evictionTime = {}
        self.policyUsed = {}
        self.weightsUsed = {}
        self.qUsed = {}
        self.freq = {}
        
        ## Accounting variables
        self.time = 0
        self.unif = self.Gamma  * np.ones(self.policy_space_size, dtype=np.float64) / self.policy_space_size
        
        self.W = np.ones(self.policy_space_size, dtype=np.float64) / self.policy_space_size
        
        
        self.X = np.array([],dtype=np.int32)
        self.Y = np.array([])
        
        ###
        self.q = Queue.Queue()
        self.sum = 0
        self.NewPages = []
        
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
#         print(np.min(self.X), np.max(self.X))
        ax = plt.subplot(2,1,1)
        ax.set_xlim(np.min(self.X), np.max(self.X))
        lbl = []
        for i in range(0, self.policy_space_size) :
            l, = plt.plot(self.X,self.Y[:,i], label='W_%d' % i)
            lbl.append(l)
        
        l3, = plt.plot(self.X, self.NewPages, 'g-', label='New Pages', alpha=0.6)
        lbl.append(l3)
        
        return lbl

    ############################################
    ## Choose a page based on the q distribution
    ############################################
    def chooseRandom(self, w):
        tmp = 1.0*w / np.sum(w,dtype=np.float64)
        cdf = np.cumsum(tmp, dtype=np.float64)
        r = np.random.rand()
        
        for policy,pr in enumerate(cdf) :
            if r < pr :
                return policy
        
#         print np.sum(w), w / np.sum(w), cdf
        
        return len(w)-1
    
    ##############################################################
    ## There was a page hit to 'page'. Update the data structures
    ##############################################################
    def pageHitUpdate(self, page):
        assert page in self.CacheRecency and page in self.freq
        self.CacheRecency.moveBack(page)
        self.freq[page] += 1
        heapq.heappush(self.PQ, (self.freq[page],page))
    
    ##########################################
    ## Add a page to cache using policy 'poly'
    ##########################################
    def addToCache(self, page):
        self.CacheRecency.add(page)
        if page not in self.freq :
            self.freq[page] = 0
        self.freq[page] += 1
        heapq.heappush(self.PQ, (self.freq[page],page))
    
    def getHeapMin(self):
        
        if len(self.PQ) < self.N :
            print self.PQ
        
        assert len(self.PQ) >= self.N, 'PQ should be full %d' % len(self.PQ)
        while self.PQ[0][1] not in self.CacheRecency or self.freq[self.PQ[0][1]] != self.PQ[0][0] :
            heapq.heappop(self.PQ) 
        return self.PQ[0][1]
    
    ######################
    ## Get LFU or LFU page
    ######################    
    def selectEvictPage(self, policy):
        if np.random.rand() < 1.0 * policy / (self.policy_space_size-1) :
            return self.CacheRecency.getFront()
        else:
            return self.getHeapMin()
    
    def evictPage(self, pg):
        assert pg in self.CacheRecency
        self.CacheRecency.delete(pg)
        
    def addToHistory(self, cacheevict):
        histevict = None
        if self.Hist1.size() == self.N :
            histevict = self.Hist1.getFront()
            assert histevict in self.Hist1
            self.Hist1.delete(histevict)
        self.Hist1.add(cacheevict)
            
        if histevict is not None :
            del self.evictionTime[histevict]
            del self.policyUsed[histevict]
            del self.freq[histevict]
            
            
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
#         if self.time % self.learning_phase == 0 :
#             self.learning = not self.learning
        
        ###########################
        ## Clean up
        ## In case PQ get too large
        ##########################
        if len(self.PQ) > 2*self.N:
            newpq = []
            for pg in self.CacheRecency :
                newpq.append((self.freq[pg],pg))
            heapq.heapify(newpq)
            self.PQ = newpq
            del newpq
        
        #####################
        ## Visualization data
        #####################
        
        if self.time == 1 :
            self.Y = np.append(self.Y, self.W)
        else:
            self.Y = np.vstack((self.Y, self.W))
        self.X = np.append(self.X, self.time)
        notInHistory = 0
        
        ##########################
        ## Process page request 
        ##########################
        if page in self.CacheRecency:
            page_fault = False
            self.pageHitUpdate(page)
        else :
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
            if page in self.Hist1:
                self.Hist1.delete(page)
                
                et = self.evictionTime[page]
                pu = self.policyUsed[page]
                qu = self.qUsed[page]
                
                cost = np.zeros(self.policy_space_size, dtype=np.float64) 
                cost[pu] = self.error_discount_rate ** (self.time - et)
                cost_hat = cost / qu
                
                #################
                ## Update Weights
                #################
                
                
                self.W = self.W * (1.0 - self.epsilon * cost_hat)
                cost[pu] = np.min(cost[pu], self.minWeight)
                self.W = self.W / np.sum(self.W)
                
                
#                 print np.sum(self.W)
                assert np.sum(self.W) > 0.00000001, 'ERROR: W is zero'
                
            else:
                notInHistory = 1
            
            
            ####################
            ## Remove from Cache
            ####################
            if self.CacheRecency.size() == self.N:
                
                ################
                ## Choose Policy
                ################
                
                q = (1.0-self.Gamma) * self.W +  self.unif 
                
                act = self.chooseRandom(q)
                
                cacheevict = self.selectEvictPage(act)
                
                self.policyUsed[cacheevict] = act
                self.evictionTime[cacheevict] = self.time
                self.qUsed[cacheevict] = q
                
                ###################
                ## Remove from Cache and Add to history
                ###################
                self.evictPage(cacheevict)
                self.addToHistory(cacheevict)
                
            self.addToCache(page)
            
            page_fault = True

        self.q.put(notInHistory)
        self.sum += notInHistory
        if self.q.qsize() > self.N:
            self.sum -= self.q.get()
        
        self.NewPages.append(1.0*self.sum / self.N)
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

