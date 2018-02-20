from lib.disk_struct import Disk
from algorithms.page_replacement_algorithm import  page_replacement_algorithm
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
class BANDIT_WITH_ARC(page_replacement_algorithm):

    def __init__(self, N):
        self.N = N
        self.Cache = Disk(N,name='Cache')
        self.Hist1 = Disk(N,name='Hist1')        
        self.Hist2 = Disk(N,name='Hist2')        
        self.Hist3 = Disk(N,name='Hist3')        
        
        ## Config variables
        self.decayRate = 0.99
        self.epsilon = 0.90     ## Learning rate
        self.lamb = 0.05
        self.learning_phase = 2*N
        self.error_discount_rate = (0.005)**(1.0/N)
        
        ## State Variables
        self.learning = True
        self.policy = 0
        self.accessedTime = {}
        self.frequency = {}
        self.accessedSinceInCache = {}
        self.evictionTime = {}
        self.policyUsed = {}
        self.qUsed = {}
        self.currentPolicy = np.random.randint(0,3)
        self.time = 0
        self.learning = True
        self.leaningPhaseCount = 1
        self.W = np.array([1.0/3,1.0/3,1.0/3], dtype=np.float32)
        self.P = 0
        self.currentQ = np.zeros(3)
        
        self.X = np.array([])
        self.Y1 = np.array([])
        self.Y2 = np.array([])
        self.Y3 = np.array([])
        
    def get_N(self) :
        return self.N
    
    def visualize(self, plt):
        l1, = plt.plot(self.X,self.Y1, 'b-', label='W_lru')
        l2, = plt.plot(self.X,self.Y2, 'r-', label='W_lfu')
        l3, = plt.plot(self.X,self.Y3, 'g-', label='W_arc')
        
        plt.xlabel('time')
        plt.ylabel('Weight')
        plt.legend(handles=[l1,l2,l3])
    
    def getArcCache(self):
        T1,T2 = [],[]
        for pg in self.Cache:
            if self.accessedSinceInCache[pg] == 1:
                T1.append(pg)
            else:
                T2.append(pg)
        return T1,T2
        
    def getArcHist(self):
        B1,B2 = [],[]
        for pg in self.Hist3:
            if self.accessedSinceInCache[pg] == 1:
                B1.append(pg)
            else:
                B2.append(pg)
        return B1,B2

    def getLru(self, L):
        lru = None
        for pg in L :
            if lru is None or self.accessedTime[pg] < self.accessedSinceInCache[lru] :
                lru = pg
        return lru
    
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
    
    def selectEvictPage(self, policy):
        r = self.getMinValueFromCache(self.accessedTime)
        f = self.getMinValueFromCache(self.frequency)
        
#         if r == f :
#             return r,-1
        if policy == 0:
            return r,0
        if policy == 1:
            return f, 1
        
    def getQ(self):
        return (1-self.lamb) * self.W + self.lamb*np.ones(3)/3

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
    
    def __replace(self,T1,T2,B1,B2,x) :
        evict = None
        if len(T1) > 0 and (len(T1) > self.P or  (x in B1 and len(B1) == self.P)):
            evict = self.getLru(T1)
            self.Cache.delete(evict)
            self.Hist3.add(evict)
        else:
            evict = self.getLru(T2)
            self.Cache.delete(evict)
            self.Hist3.add(evict)
        if evict is None :
            print('__replace debug')
        return evict
    
    ########################################################################################################################################
    ####REQUEST#############################################################################################################################
    ########################################################################################################################################
    def request(self,page) :
        page_fault = False
        self.time = self.time + 1
        ############################
        ## Save data for training ##
        ############################

        if self.time % self.learning_phase == 0 :
            lastPolicy = self.currentPolicy
            if np.random.rand() < (0.5 - 0.5/np.sqrt(self.leaningPhaseCount)):
                self.currentPolicy = np.argmax(self.getQ())
                self.learning = False
            else:
                self.currentPolicy = self.chooseRandom()
                self.leaningPhaseCount += 1
                self.learning = True
                self.currentQ = self.getQ()
            
            if self.currentPolicy == 2 and lastPolicy != 2 :
                self.Hist3.clear()
            
        ## Visualization data
        prob = self.getQ()
        self.X = np.append(self.X, self.time)
        self.Y1 = np.append(self.Y1, prob[0])
        self.Y2 = np.append(self.Y2, prob[1])
        self.Y3 = np.append(self.Y3, prob[2])
        

        #########################
        ## Process page reques ##
        #########################
        if page in self.Cache:
            page_fault = False
        else :
            
            #### HISTORY #########################################################################################################
            pageevict = None
            policyUsed = -1
            wasInArcHist = False
            if page in self.Hist1:
                pageevict = page
                policyUsed = 0
                self.Hist1.delete(page)
            elif page in self.Hist2:
                pageevict = page
                policyUsed = 1
                self.Hist2.delete(page)
            elif page in self.Hist3 :
                pageevict = page
                policyUsed = 2
                wasInArcHist = True
                B1,B2 = self.getArcHist()
                if page in B1 :
                    if len(B2) > len(B1) :
                        r = len(B2) / len(B1)
                    else :
                        r = 1
                    self.P = min(self.P + r, self.N)
                if page in B2 :
                    if len(B1) > len(B2) :
                        r = len(B1) / len(B2)
                    else :
                        r = 1
                    self.P = max(self.P - r, 0)
                self.Hist3.delete(page)
                
            if pageevict is not None :
                q = self.qUsed[pageevict]
                err = self.error_discount_rate ** (self.time - self.evictionTime[pageevict])
                reward = np.array([0,0,0], dtype=np.float32)
                if policyUsed == 0:
                    reward[1] = reward[2] = err
                if policyUsed == 1:
                    reward[0] = reward[2] = err
                if policyUsed == 2:
                    reward[0] = reward[1] = err
                
                reward_hat = reward / q
                ## Update Weights
                if self.policyUsed[pageevict] != -1:
                    self.W = self.W * np.exp(self.lamb * reward_hat / 3)
                    self.W = self.W / np.sum(self.W)
            #### END HISTORY ######################################################################################################
            
            #############################################################################################################
            ## Remove from Cache
            if self.Cache.size() == self.N:
                histevict = -1
                
                if self.currentPolicy == 0:
                    cacheevict = self.getMinValueFromCache(self.accessedTime)
                    self.Cache.delete(cacheevict)
                    self.qUsed[cacheevict] = self.currentQ
                    self.evictionTime[cacheevict] = self.time
                    self.policyUsed[cacheevict] = 0 if not self.learning else -1
                    
                    if self.Hist1.size() == self.N :
                        histevict = self.Hist1.getIthPage(0)
                        self.Hist1.delete(histevict)
                    self.Hist1.add(cacheevict)
                    
                if self.currentPolicy == 1:
                    cacheevict = self.getMinValueFromCache(self.frequency)
                    self.Cache.delete(cacheevict)
                    self.qUsed[cacheevict] = self.currentQ
                    self.evictionTime[cacheevict] = self.time
                    self.policyUsed[cacheevict] = 1 if not self.learning else -1
                    
                    if self.Hist2.size() == self.N :
                        histevict = self.Hist2.getIthPage(0)
                        self.Hist2.delete(histevict)
                    self.Hist2.add(cacheevict)
                
                if self.currentPolicy == 2:
                    T1,T2 = self.getArcCache()
                    B1,B2 = self.getArcHist()
                    cacheevict=None
                    if wasInArcHist :
                        cacheevict = self.__replace(T1, T2, B1, B2, page)
                    else:
                        if len(T1) + len(B1) == self.N :
                            if len(T1) < self.N :
                                histevict = self.getLru(B1)
                                self.Hist3.delete(histevict)
                                cacheevict = self.__replace(T1, T2, B1, B2, page)
                            else :
                                histevict = self.getLru(T1)
                                self.Cache.delete(histevict)
                                
                            _T1,_T2 = self.getArcCache()
                            _B1,_B2 = self.getArcHist()
                            
                            if len(_T1) + len(_B1) >= 50 :
                                print('debug: T1+B1 = ', len(_T1) + len(_B1),' T1,B1 = ',len(_T1) , len(_B1))
                            
                        elif len(T1) + len(B1) < self.N :
                            if len(T1) + len(T2) + len(B1) + len(B2) >= self.N :
                                if len(T1) + len(T2) + len(B1) + len(B2) == 2*self.N :
                                    histevict = self.getLru(B2)
                                    self.Hist3.delete(histevict)
                                cacheevict = self.__replace(T1, T2, B1, B2, page)
                        
                    if cacheevict is not None :
                        self.qUsed[cacheevict] = self.currentQ
                        self.evictionTime[cacheevict] = self.time
                        self.policyUsed[cacheevict] = 2 if not self.learning else -1
                    else :
                        print('cacheevict is None', len(T1)+len(B1),len(T1),len(B1), cacheevict)
                        pass
                                
                if histevict != -1 :
                    del self.evictionTime[histevict]
                    del self.accessedTime[histevict]
                    del self.frequency[histevict]
                    del self.accessedSinceInCache[histevict]
                    del self.policyUsed[histevict]
                    del self.qUsed[histevict]
                    
            if page not in self.frequency:
                self.frequency[page] = 0
            
            if page not in self.accessedSinceInCache or not wasInArcHist :
                self.accessedSinceInCache[page] = 0     ## page - is new to cache
            
            self.Cache.add(page)
            page_fault = True

        for q in self.Cache :
            self.frequency[q] *= self.decayRate
        self.frequency[page] += 1
        self.accessedTime[page] = self.time
        self.accessedSinceInCache[page] += 1
        
        return page_fault

    def get_list_labels(self) :
        return ['L']

