from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.priorityqueue import priorityqueue
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class LaCReME_simple(page_replacement_algorithm):
    def __init__(self, N):
        self.N = N
        self.CacheRecency = Disk(N)
        self.CacheFrequecy = priorityqueue(N)
        self.Hist1 = Disk(N)        
        self.Hist2 = priorityqueue(N)        
        
        ## Config variables
        self.decayRate = 1
        self.epsilon = 0.05
        self.learning_phase = N/2
        
        ## 
        self.learning = True
        self.policy = 0
        self.evictionTime = {}
        self.policyUsed = {}
        self.weightsUsed = {}
        self.freq = {}
        
        ## TODO add decay_time and decay_factor
        self.decay_time = N
        self.decay_factor = 1
        
        ## Accounting variables
        self.time = 0
        self.W = np.array([.5,.5], dtype=np.float32)
        
        ## For visualization
        self.X = np.array([],dtype=np.int32)
        self.Y1 = np.array([])
        self.Y2 = np.array([])
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        ax = plt.subplot(2,1,1)
        ax.set_xlim(np.min(self.X), np.max(self.X))
        l1, = plt.plot(self.X,self.Y1, 'b-', label='W_lru')
        l2, = plt.plot(self.X,self.Y2, 'r-', label='W_lfu')
        return [l1,l2]
    
    ##########################################
    ## Add a page to cache using policy 'poly'
    ##########################################
    def addToCache(self, page,pagefreq=0):
        self.CacheRecency.add(page)
        self.CacheFrequecy.add(page)
        self.CacheRecency.increaseCount(page, amount=pagefreq)
        self.CacheFrequecy.increase(page, amount=pagefreq)
        
    ######################
    ## Get LFU or LFU page
    ######################    
    def selectEvictPage(self, policy):
        r = self.CacheRecency.getIthPage(0)
        f = self.CacheFrequecy.peaktop()
        pageToEvit,policyUsed = None, None
        if r == f :
            pageToEvit,policyUsed = r,-1
        elif policy == 0:
            pageToEvit,policyUsed = r,0
        elif policy == 1:
            pageToEvit,policyUsed = f,1
        return pageToEvit,policyUsed
    
    def evictPage(self, pg):
        self.CacheRecency.delete(pg)
        self.CacheFrequecy.delete(pg)
    
    ##############################################################
    ## There was a page hit to 'page'. Update the data structures
    ##############################################################
    def pageHitUpdate(self, page):
        if page in self.CacheRecency and page in self.CacheFrequecy:
            self.CacheRecency.moveBack(page)
            self.CacheRecency.increaseCount(page)
            self.CacheFrequecy.increase(page)
    
    ############################################
    ## Choose a page based on the q distribution
    ############################################
    def chooseRandom(self):
        q = self.getQ()
        r = np.random.rand()
        for i,p in enumerate(q):
            if r < p:
                return i 
        return len(q)-1
    
    ##################
    ####REQUEST#######
    ##################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        
        #####################
        ## Visualization data
        #####################
        self.X = np.append(self.X, self.time)
        self.Y1 = np.append(self.Y1, self.W[0])
        self.Y2 = np.append(self.Y2, self.W[1])

        
        if self.time % self.N == 0 :
            self.CacheFrequecy.decay(self.decay_factor)
            self.Hist2.decay(self.decay_factor)

        ##########################
        ## Process page request 
        ##########################
        if page in self.CacheFrequecy:
            page_fault = False
            self.pageHitUpdate(page)
        else :
            
            #####################################################
            ## Learning step: If there is a page fault in history
            #####################################################
            histpage_freq = 1
            if page in self.Hist1:
                histpage_freq = self.Hist1.getCount(page)
                self.Hist1.delete(page)
                self.W[0] = self.W[0] * (1 - self.epsilon) if self.policyUsed[page] != -1 else self.W[0]
            elif page in self.Hist2:
                histpage_freq = self.Hist2.getCount(page) ## Get the page frequency in history
                self.Hist2.delete(page)
                self.W[1] = self.W[1] * (1 - self.epsilon) if self.policyUsed[page] != -1 else self.W[1]
            
            ####################
            ## Normalize weights
            ####################
            self.W = self.W / np.sum(self.W)
            
            ####################
            ## Remove from Cache
            ####################
            if self.CacheRecency.size() == self.N:
                
                ################################################################
                ## Choose Policy by picking the one with the highest weight
                ################################################################                
                act = np.argmax(self.W)
                
                cacheevict,poly = self.selectEvictPage(act)
                pagefreq = self.CacheFrequecy.getCount(cacheevict)
                
                self.policyUsed[cacheevict] = poly
                self.weightsUsed[cacheevict] = self.W
                self.evictionTime[cacheevict] = self.time
                        
                ###################
                ## Evict to history
                ###################
                histevict = None
                if (poly == 0) or (poly==-1 and np.random.rand() <0.5):
                    if self.Hist1.size() == self.N :
                        histevict = self.Hist1.getIthPage(0)
                        self.Hist1.delete(histevict)
                    self.Hist1.add(cacheevict)
                    self.Hist1.setCount(cacheevict, pagefreq)
                else:
                    if self.Hist2.size() == self.N :
                        histevict = self.Hist2.popmin()
                    self.Hist2.add(cacheevict)
                    self.Hist2.increase(cacheevict, pagefreq-1)
                
                ##################################
                ## Remove histevict from the system
                ###################################
                if histevict is not None :
                    del self.evictionTime[histevict]
                    del self.policyUsed[histevict]
                    del self.weightsUsed[histevict]
                    
                ##############################################
                ## Remove cacheevict from both data structures
                ############################################## 
                self.evictPage(cacheevict)
            
            ###################################
            ## Add page to both data structures
            ###################################
            self.addToCache(page, pagefreq=histpage_freq)
            
            page_fault = True

        return page_fault

    def get_list_labels(self) :
        return ['L']

