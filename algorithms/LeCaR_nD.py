from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.priorityqueue import priorityqueue
from lib.CacheLinkedList import CacheLinkedList
import time
import numpy as np
import Queue
import heapq
# import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LeCaR_nD(page_replacement_algorithm):

    def __init__(self, N, visualization = True):
        self.N = N
        self.CacheRecency = CacheLinkedList(N)

        self.freq = {}
        self.PQ = []
        
        self.Hist1 = CacheLinkedList(N)        
        self.Hist2 = CacheLinkedList(N)    
        self.Hist3 = CacheLinkedList(N)      
        
        ## Config variables
        self.error_discount_rate = (0.005)**(1.0/N)
        self.learning_rate = 0.5
        self.counter = 0
        
        ## 
        self.evictionTime = {}
        
        ## Accounting variables
        self.time = 0
        self.W = np.array([.33,.33,.33], dtype=np.float32)
        
        self.Visualization = visualization
        self.X = []
        self.Y1 = []
        self.Y2 = []
        self.Y3 = []
        
        self.gamma = 0.05 # uniform distribution mixture parameter
        self.q_used = {}
        self.unique = {}
        self.unique_cnt = 0
        self.pollution_dat_x = []
        self.pollution_dat_y = []
        
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        lbl = []
        if self.Visualization:
            X = np.array(self.X)
            Y1 = np.array(self.Y1)
            Y2 = np.array(self.Y2)
            Y3 = np.array(self.Y3)
            ax = plt.subplot(2,1,1)
            ax.set_xlim(np.min(X), np.max(X))
            
            l3, = plt.plot(self.pollution_dat_x,self.pollution_dat_y, 'g-', label='hoarding',linewidth=3)
            l1, = plt.plot(X,Y1, 'y-', label='W_lru',linewidth=2)
            l2, = plt.plot(X,Y2, 'b-', label='W_lfu',linewidth=1)
            l4, = plt.plot(X,Y3, 'g-', label='W_ncu',linewidth=1)
            
            
            
            lbl.append(l1)
            lbl.append(l2)
            lbl.append(l3)
            lbl.append(l4)
        return lbl
    
    def getWeights(self):
        return np.array([self. X, self.Y1, self.Y2, self.Y3, self.pollution_dat_x, self.pollution_dat_y ]).T
#         return np.array([self.pollution_dat_x,self.pollution_dat_y ]).T
    
    def getStats(self):
        d={}
        d['weights'] = np.array([self. X, self.Y1, self.Y2, self.Y3]).T
        d['pollution'] = np.array([self.pollution_dat_x, self.pollution_dat_y ]).T
        return d
    
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
        while self.PQ[0][1] not in self.CacheRecency or self.freq[self.PQ[0][1]] != self.PQ[0][0] :
            heapq.heappop(self.PQ) 
        return self.PQ[0][1]
    
    ######################
    ## Get LFU or LFU page
    ######################    
    def selectEvictPage(self, policy):
        nd = None
        pageToEvit,policyUsed = None, None
        
        if policy == 2:
            pageToEvit,policyUsed = nd,2
        else:
            r = self.CacheRecency.getFront()
            f = self.getHeapMin()
            if r == f :
                pageToEvit,policyUsed = r,-1
            elif policy == 0:
                pageToEvit,policyUsed = r,0
            elif policy == 1:
                pageToEvit,policyUsed = f,1
            
        
        return pageToEvit,policyUsed
    
    def evictPage(self, pg):
        assert pg in self.CacheRecency
        self.CacheRecency.delete(pg)
        
    
    ############################################
    ## Choose a page based on the q distribution
    ############################################
    def chooseRandom(self, q):
        #r = np.random.rand()
        #if r < q[0] :
        #    return 0
        #elif r < q[1]:
         #   return 1
        #return 2
        if len(q) == 2:
            r = np.random.rand()
            if r < self.W[0] :
                return 0
            return 1
        else: 
            r = np.random.rand()
            if r < self.W[0] :
                return 0
            elif r < self.W[1]:
                return 1
            return 2
            
        #return np.random.choice(range(len(q)), q)
    
    def addToHistory(self, poly, cacheevict):
        histevict = None
        if (poly == 0) or (poly==-1 and np.random.rand() <0.5):
            if self.Hist1.size() == self.N :
                histevict = self.Hist1.getFront()
                assert histevict in self.Hist1
                self.Hist1.delete(histevict)
            self.Hist1.add(cacheevict)
        elif (poly == 1):
            if self.Hist2.size() == self.N :
                histevict = self.Hist2.getFront()
                assert histevict in self.Hist2
                self.Hist2.delete(histevict)
            self.Hist2.add(cacheevict)
        elif (poly == 2):
            if self.Hist3.size() == self.N :
                histevict = self.Hist3.getFront()
                assert histevict in self.Hist3
                self.Hist3.delete(histevict)
            self.Hist3.add(cacheevict)
            #print ('H3', self.time, cacheevict)
            self.evictionTime[cacheevict] = self.time
            
        if histevict is not None :
            if not histevict in self.Hist3:
                del self.evictionTime[histevict]
            del self.freq[histevict]

            
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        
        ###########################
        ## Clean up
        ## In case PQ get too large
        ##########################
        if len(self.PQ) > 2*self.N:
            newpq = []
            for pg in self.CacheRecency:
                newpq.append((self.freq[pg],pg))
            heapq.heapify(newpq)
            self.PQ = newpq
            del newpq
        
        #####################
        ## Visualization data
        #####################
        if self.Visualization:
            self.X.append(self.time)
            self.Y1.append(self.W[0])
            self.Y2.append(self.W[1])
            self.Y3.append(self.W[2])
        
        ##########################
        ## Process page request 
        ##########################
        if page in self.CacheRecency:
            page_fault = False
            self.pageHitUpdate(page)
        else :
            page_fault = True
            for page_lists in (self.Hist1 ,self.Hist2 ,self.Hist3):
                if page in page_lists:
                    self.W[0] = self.W[0]/(self.W[0] + self.W[1])
                    self.W[1] = 1 - self.W[0]
                            
                    ################
                    ## Choose Policy
                    ################
                    #print (q)
                    q = (1-self.gamma) * self.W[0:2] + self.gamma 
                    act = self.chooseRandom(q)
                else:
                    q = (1-self.gamma) * self.W + self.gamma
                    act = self.chooseRandom(q)
     
            
            if act == 2:
                poly = 2
                cacheevict = page
                #print(page)
                self.addToHistory(poly, cacheevict)
                self.counter += 1
                #self.evictionTime[cacheevict] = self.time
                #print (self.evictionTime[cacheevict])
                #print (cacheevict)
                
            if act != 2:       
                #
                #print q
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
                pageevict = None
    
                reward = np.array([0,0,0], dtype=np.float32)
                if page in self.Hist1:
                    pageevict = page
                    self.Hist1.delete(page)
                    reward[1] = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                    reward[2] = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                elif page in self.Hist2:
                    pageevict = page
                    self.Hist2.delete(page)
                    reward[0] = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                    reward[2] = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                elif page in self.Hist3:
                    pageevict = page
                    self.Hist3.delete(page)
                    #print (self.evictionTime[pageevict] , pageevict)
                    reward[0] = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                    reward[1] = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                #################
                ## Update Weights
                #################
                if pageevict is not None  :
                    self.W = self.W * np.exp(self.learning_rate * reward)
                    self.W = self.W / np.sum(self.W)
                    
                ####################
                ## Remove from Cache
                ####################
                if self.CacheRecency.size() == self.N:
                    
                    cacheevict,poly = self.selectEvictPage(act)
                    
                    ###################
                    ## Remove from Cache and Add to history
                    ###################
                    self.evictPage(cacheevict)
                    self.addToHistory(poly, cacheevict)
                    self.evictionTime[cacheevict] = self.time
                   
                self.addToCache(page)
                
            
            ## Count pollution
            
        
        if page_fault:
            self.unique_cnt += 1
        self.unique[page] = self.unique_cnt
        
        if self.time % self.N == 0:
            pollution = 0
            for pg in self.CacheRecency:
                if self.unique_cnt - self.unique[pg] >= 2*self.N:
                    pollution += 1
            
            self.pollution_dat_x.append(self.time)
            self.pollution_dat_y.append(100* pollution / self.N)
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

