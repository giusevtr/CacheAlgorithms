from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
from lib.priorityqueue import priorityqueue
import numpy as np
# import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# sys.path.append(os.path.abspath("/home/giuseppe/))

## Keep a LRU list.
## Page hits:
##      Every time we get a page hit, mark the page and also move it to the MRU position
## Page faults:
##      Evict an unmark page with the probability proportional to its position in the LRU list.
class LaCrema(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.CacheRecency = Disk(N)
        self.CacheFrequecy = priorityqueue(N)
        
        self.Hist1 = Disk(N)        
        self.Hist2 = priorityqueue(N)        
        
        ## Config variables
        self.decayRate = 1
        self.epsilon = 0.95
        self.lamb = 0.05
        self.learning_phase = N/2
        self.error_discount_rate = (0.005)**(1.0/N)
        ## 
        self.learning = True
        self.policy = 0
        self.evictionTime = {}
        self.policyUsed = {}
        self.qUsed = {}
        self.freq = {}
        ## Accounting variables
        self.time = 0
        
        self.W = np.array([.5,.5], dtype=np.float32)
        
        self.X = np.array([])
        self.Y1 = np.array([])
        self.Y2 = np.array([])
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        l1, = plt.plot(self.X,self.Y1, 'b-', label='W_lru')
        l2, = plt.plot(self.X,self.Y2, 'r-', label='W_lfu')
        plt.xlabel('time')
        plt.ylabel('Weight')
        plt.legend(handles=[l1,l2])
        
    def __keyWithMinVal(self,d):
        v=list(d.values())
        k=list(d.keys())
        return k[v.index(min(v))]
    
    def getMinValueFromCache(self, values):
        minpage,first = -1, True
        for q in self.Cache :
            if first or values[q] < values[minpage] :
                minpage,first=q,False
        return minpage
    
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
    
    #########################
    ## Get the Q distribution
    #########################
    def getQ(self):
        return (1-self.lamb) * self.W + self.lamb*np.ones(2)/2
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
    def updateWeight(self, cost):
        self.W = self.W * (1-self.epsilon * cost)
        self.W = self.W / np.sum(self.W)
    
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        if self.time % self.learning_phase == 0 :
            self.learning = not self.learning
        
        #####################
        ## Visualization data
        #####################
        prob = self.getQ()
        self.X = np.append(self.X, self.time)
        self.Y1 = np.append(self.Y1, prob[0])
        self.Y2 = np.append(self.Y2, prob[1])

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
            pageevict, histpage_freq = None,1
            policyUsed = -1
            if page in self.Hist1:
                pageevict = page
                histpage_freq = self.Hist1.getCount(page)
                self.Hist1.delete(page)
                policyUsed = 0
            elif page in self.Hist2:
                pageevict = page
                histpage_freq = self.Hist2.getFreq(page) ## Get the page frequency in history
                self.Hist2.delete(page)
                policyUsed = 1
            if pageevict is not None :
                q = self.qUsed[pageevict]
                err = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                reward = np.array([0,0], dtype=np.float32)
                if policyUsed == 0 : # LRU
                    reward[1] = err
                if policyUsed == 1:
                    reward[0] = err
                reward_hat = reward / q
                
                #################
                ## Update Weights
                #################
                if self.policyUsed[pageevict] != -1 :
                    self.W = self.W * np.exp(self.lamb * reward_hat / 2)
                    self.W = self.W / np.sum(self.W)
            
            ####################
            ## Remove from Cache
            ####################
            if self.CacheRecency.size() == self.N:
                
                ################
                ## Choose Policy
                ################
                if  not self.learning :
                    act = np.argmax(self.getQ())
                else :
                    act = self.chooseRandom()
                
                cacheevict,poly = self.selectEvictPage(act)
                pagefreq = self.CacheRecency.getCount(cacheevict) if cacheevict in self.CacheRecency else self.CacheFrequecy.getFreq(cacheevict)
                
                self.policyUsed[cacheevict] = poly
                self.qUsed[cacheevict] = self.getQ()
                self.evictionTime[cacheevict] = self.time
                        
                if not self.learning :
                    self.policyUsed[cacheevict] = -1
                
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
                
                if histevict is not None :
                    del self.evictionTime[histevict]
                    del self.policyUsed[histevict]
                    del self.qUsed[histevict]
                
                self.evictPage(cacheevict)
                
            self.addToCache(page, pagefreq=histpage_freq)
            
            page_fault = True

        return page_fault

    def get_list_labels(self) :
        return ['L']

